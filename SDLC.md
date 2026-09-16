# SDLC and workflow

This repo follows a lightweight but disciplined development lifecycle.

## Lifecycle

```text
Learning objective
        ↓
Short-lived branch
        ↓
Manual derivation and concept review
        ↓
Notebook implementation
        ↓
Checkpoint commit + push
        ↓
Reusable `src/pm/` implementation
        ↓
Tests
        ↓
Reference and documentation updates
        ↓
Pull request review
        ↓
Merge to `main`
        ↓
Update progress and roadmap
```

## Work item types

### Learning unit
Examples:
- covariance
- duration
- spread duration

Produces:
- notebook update
- reference page update
- code implementation if needed
- tests
- progress note

### Feature
Examples:
- scenario engine
- optimizer constraints
- Treasury curve loader

### Use case
Examples:
- duration hedge
- curve steepener
- credit spread shock

### Reference enhancement
Example:
- OAS vs Z-spread comparison

## Definition of ready

Before implementing a topic:
- the objective is clear,
- the concept is identified,
- the required references are known,
- the expected output is understood.

## Definition of done

A concept is done when:
- the manual exercise has been attempted,
- the formula and units are written down,
- the notebook contains a worked example,
- the reusable code is in `src/pm/` if appropriate,
- the deterministic tests pass,
- limitations and approximation assumptions are stated,
- the progress file is updated,
- the PR is reviewed and merged.

## Checkpoint policy

Commit logical states, not every keystroke.

Typical sequence:
1. `learn:` manual lab complete
2. `feat:` reusable implementation + tests
3. `docs:` reference/progress complete

## Main branch policy

`main` should remain:
- runnable,
- test-passing,
- documented,
- suitable as a quick-reference version of the repository.

Do experimental learning on short-lived branches.

## Releases

Suggested milestone pattern:

```text
v0.1-foundations
v0.2-fixed-income-foundations
v0.3-rates
v0.4-credit
v0.5-ficc-risk
v0.6-attribution
v0.7-use-cases
v0.8-tutors
v1.0-pm-mechanics
```

Create annotated releases after meaningful roadmap phases, not after each notebook.
