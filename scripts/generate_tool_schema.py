"""Introspect src/pm and emit a machine-readable schema of every public
function - name, module path, parameters, and docstring - for use as an
agent tool catalog. See reference/concepts/agentic_pm_analytics.md.

Run: python scripts/generate_tool_schema.py > docs/tool_schema.json
"""

import inspect
import json
import pkgutil

import pm


def iter_modules():
    yield pm
    for info in pkgutil.walk_packages(pm.__path__, prefix="pm."):
        # Skip private modules (e.g. pm._solver) - internal helpers, not
        # analytics functions an agent should call directly.
        if info.name.rsplit(".", 1)[-1].startswith("_"):
            continue
        yield __import__(info.name, fromlist=["_"])


def describe_function(name, func, module_name):
    sig = inspect.signature(func)
    params = [
        {
            "name": p.name,
            "default": None if p.default is inspect.Parameter.empty else repr(p.default),
        }
        for p in sig.parameters.values()
    ]
    doc = inspect.getdoc(func) or ""
    return {
        "name": name,
        "module": module_name,
        "parameters": params,
        "description": doc.splitlines()[0] if doc else "",
    }


def main():
    seen = set()
    tools = []
    for module in iter_modules():
        for name, obj in sorted(vars(module).items()):
            if not inspect.isfunction(obj):
                continue
            if name.startswith("_"):
                continue
            if obj.__module__ != module.__name__:
                continue  # skip re-exports, only describe where a function is defined
            key = (obj.__module__, name)
            if key in seen:
                continue
            seen.add(key)
            tools.append(describe_function(name, obj, obj.__module__))

    tools.sort(key=lambda t: (t["module"], t["name"]))
    print(json.dumps({"tools": tools}, indent=2))


if __name__ == "__main__":
    main()
