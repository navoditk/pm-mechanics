# Roadmap

This file is the long-range view for the repository. The canonical docs hub is [docs/README.md](docs/README.md).

## Phase 0 — Repository foundation
- repo conventions
- resource curation
- notebook pattern
- reference-page pattern
- agent operating rules
- test strategy

## Phase 1 — Portfolio foundations
- returns and compounding
- volatility
- covariance/correlation
- diversification
- risk contribution
- Sharpe ratio
- drawdown
- benchmark basics

## Phase 2 — Portfolio theory and optimization
- opportunity set
- efficient frontier
- global minimum variance
- tangency portfolio
- risk aversion
- mean–variance optimization
- constraints
- transaction costs
- estimation error
- covariance shrinkage
- robust optimization
- Black–Litterman

## Phase 3 — Active portfolio management
- benchmark-relative return/risk
- active weights
- tracking error
- information ratio
- IC
- breadth
- transfer coefficient
- Fundamental Law
- risk budgeting
- active constraints

## Phase 4 — Risk models
- factor models
- systematic vs specific risk
- factor covariance
- factor contribution
- marginal/component risk
- VaR / ES
- stress testing
- scenario design
- backtesting biases: look-ahead, survivorship, stale data, point-in-time vintage

## Phase 5 — Fixed-income foundations
- bond cash flows
- clean/dirty price
- accrued interest
- yield measures
- duration
- DV01
- convexity
- key-rate duration
- carry and roll
- accrued interest, clean vs dirty price, day-count conventions, settlement

## Phase 6 — Rates portfolio management
- curve construction
- forwards
- curve trades
- steepeners/flatteners
- butterflies
- Treasury futures
- swaps
- swap DV01
- hedging
- swap spreads
- basis
- scenario analysis

## Phase 7 — Credit portfolio management
- spread measures
- Z-spread
- OAS
- spread duration
- default/recovery
- credit curves
- IG/HY
- CDS
- basis
- migration/default risk
- portfolio credit scenarios

## Phase 8 — Securitized / mortgages
- agency MBS
- pass-throughs
- prepayment
- extension/contraction
- negative convexity
- effective duration
- OAS
- non-agency / ABS / CMBS overview

## Phase 9 — FX and commodities
- spot/forward
- covered interest parity
- FX carry
- hedging
- cross-currency basis
- commodity futures curves
- contango/backwardation
- roll yield

## Phase 10 — Attribution and implementation
- performance measurement
- Brinson intuition
- fixed-income attribution
- carry/curve/spread decomposition
- transaction costs
- liquidity
- rebalancing

## Phase 11 — Advanced portfolio construction
- robust covariance
- Bayesian views
- Black–Litterman
- risk parity
- hierarchical methods
- regime-aware allocation
- scenario optimization
- multi-period optimization

## Phase 12 — Agentic PM analytics
- deterministic analytics tools
- natural-language query layer
- tool schemas
- grounding
- guardrails
- evals
- explainability
- observability
- tutor agents

In this repo, Phase 12 is scoped to what serves the curriculum: `/pm-query`,
`/tutor`, and `/master`. The full version of this phase — governed multi-agent
workflows, Cedar authorization, evaluation suites, OpenTelemetry, MCP, and an
AWS Bedrock AgentCore deployment path — is built out as a separate repository,
[agentic-pm-lab](https://github.com/navoditk/agentic-pm-lab). It is kept
separate deliberately: the agent stack carries a much heavier dependency set
than this repo's numpy/scipy/cvxpy core, and the two have different audiences.

## Phase 13 — Equity portfolio management
- dividend discount model (Gordon growth, two-stage)
- relative valuation multiples (justified P/E, PEG)
- CAPM, beta, equity risk premium, Jensen's alpha
- equity factor investing (value/size/momentum/quality/low-vol tilts)
- active share
- shareholder yield, buybacks, total shareholder return

## Phase 14 — Derivatives and options
- Black-Scholes pricing (call, put)
- the Greeks (delta, gamma, vega, theta, rho)
- put-call parity
- implied volatility
- Black-76 (options on forwards/futures)
- swaptions, caps, floors (conceptual)
- option strategies: covered call, protective put, collar (conceptual)

## Phase 15 — Asset allocation and performance measurement
- time-weighted return (TWR)
- money-weighted return (MWR / IRR)
- GIPS and composite construction (conceptual)
- liability-driven investing: funded ratio, surplus
- duration/PV01 matching for liabilities (reuses existing duration tools)
- strategic vs. tactical asset allocation (conceptual - reuses existing
  optimization tools)

## Phase 16 — Wider investable universe
- municipal bonds: tax-equivalent yield
- convertible bonds: conversion value, conversion premium
- preferred securities: perpetuity valuation (reuses gordon_growth_value)
- sovereign and EM debt: hard vs. local currency (conceptual)
- alternative investments overview: private equity, hedge funds, real
  assets, private debt (conceptual)
- ESG and sustainable investing: screening, integration, engagement,
  impact investing (conceptual)

## Definition of done

This repository is never permanently done. Each real PM question should become one of:
- a new reference page,
- a new lab,
- a new test,
- a new use case,
- a new curated resource,
- or an extension of the analytics library.
