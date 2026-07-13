# Project Roadmap

This document defines the planned development stages of the Market Risk and Stress Testing Platform.

The project follows an incremental versioning strategy. Each version introduces a coherent set of capabilities and must satisfy its completion criteria before development proceeds to the next stage.

## Status Legend

* `[ ]` Not started
* `[~]` In progress
* `[x]` Completed

---

## v0.1 — Planning and Repository Setup

**Status:** `[x]`

### Objectives

* Define the project scope and objectives.
* Establish the system architecture.
* Define the repository structure.
* Configure the initial development environment.

### Deliverables

* [x] Project specification
* [x] Initial roadmap
* [x] Architecture design
* [x] Repository structure
* [x] Initial professional README
* [x] Python project configuration
* [x] Development dependency configuration
* [x] Initial continuous integration workflow
* [x] Code formatting and linting configuration

### Completion Criteria

Version `v0.1` is complete when the project scope, architecture and repository structure are documented and the development environment can be installed successfully.

---

## v0.2 — Market Data Layer

**Status:** `[~]`

### Objectives

* Retrieve historical market data from an external provider.
* Validate and standardise the collected data.
* Isolate external data dependencies from the analytical modules.

### Deliverables

* [x] Market data provider interface
* [x] Historical adjusted-price retrieval
* [x] Date-range validation
* [ ] Missing-data detection
* [ ] Asset time-series alignment
* [x] Local data caching
* [x] Data-layer error handling
* [x] Unit tests for data validation and transformation

### Completion Criteria

Version `v0.2` is complete when valid historical data can be retrieved, processed and returned in a standard internal format for multiple assets.

---

## v0.3 — Portfolio Analytics Engine

**Status:** `[ ]`

### Objectives

* Create and validate investment portfolios.
* Calculate asset and portfolio returns.
* Produce the core portfolio performance indicators.

### Deliverables

* [ ] Portfolio input model
* [ ] Portfolio-weight validation
* [ ] Simple and logarithmic return calculations
* [ ] Portfolio return aggregation
* [ ] Portfolio value time series
* [ ] Cumulative return
* [ ] Annualised return
* [ ] Annualised volatility
* [ ] Sharpe ratio
* [ ] Maximum drawdown
* [ ] Correlation matrix
* [ ] Unit tests using deterministic examples

### Completion Criteria

Version `v0.3` is complete when a valid multi-asset portfolio can be constructed and its principal performance metrics can be calculated reliably.

---

## v0.4 — Risk Metrics

**Status:** `[ ]`

### Objectives

* Implement the general portfolio risk measures required by the platform.
* Establish reusable conventions for confidence levels, horizons and monetary risk values.

### Deliverables

* [ ] Rolling volatility
* [ ] Percentage and monetary loss conversion
* [ ] Configurable confidence levels
* [ ] Configurable risk horizons
* [ ] Risk-metric result models
* [ ] Numerical validation tests

### Completion Criteria

Version `v0.4` is complete when the shared risk-measurement infrastructure is stable and ready to support VaR and Expected Shortfall methodologies.

---

## v0.5 — Value at Risk and Expected Shortfall

**Status:** `[ ]`

### Objectives

* Implement and compare multiple VaR methodologies.
* Estimate Expected Shortfall for the supported approaches.

### Deliverables

* [ ] Historical Simulation VaR
* [ ] Parametric Variance-Covariance VaR
* [ ] Monte Carlo VaR
* [ ] Historical Expected Shortfall
* [ ] Parametric Expected Shortfall, where applicable
* [ ] Configurable Monte Carlo random seed
* [ ] Method-comparison output
* [ ] Mathematical documentation
* [ ] Unit tests against reference calculations

### Completion Criteria

Version `v0.5` is complete when all mandatory VaR and Expected Shortfall methods produce reproducible and validated results.

---

## v0.6 — VaR Backtesting

**Status:** `[ ]`

### Objectives

* Evaluate whether VaR estimates are consistent with realised portfolio losses.
* Provide statistical and visual validation outputs.

### Deliverables

* [ ] Rolling VaR estimation
* [ ] VaR exception identification
* [ ] Expected and observed exception rates
* [ ] Kupiec Proportion of Failures test
* [ ] Backtesting result model
* [ ] Exception visualisation
* [ ] Tests using synthetic return sequences

### Completion Criteria

Version `v0.6` is complete when the platform can perform rolling VaR backtesting and statistically evaluate the observed exception frequency.

---

## v0.7 — Stress Testing

**Status:** `[ ]`

### Objectives

* Measure portfolio sensitivity to adverse market scenarios.
* Explain portfolio-level and asset-level stress losses.

### Deliverables

* [ ] Stress-scenario data model
* [ ] Broad equity market decline scenario
* [ ] Technology-sector decline scenario
* [ ] Banking-sector shock scenario
* [ ] Cryptocurrency market decline scenario
* [ ] Cross-asset risk-off scenario
* [ ] Portfolio loss calculation
* [ ] Asset-level loss contribution
* [ ] Scenario comparison
* [ ] Unit tests for deterministic shocks

### Completion Criteria

Version `v0.7` is complete when at least five documented stress scenarios can be applied consistently to a portfolio.

---

## v0.8 — REST API and Interactive Dashboard

**Status:** `[ ]`

### Objectives

* Expose the analytical engine through a documented REST API.
* Provide an interactive interface for portfolio configuration and risk analysis.

### Deliverables

* [ ] FastAPI application
* [ ] Health endpoint
* [ ] Portfolio-validation endpoint
* [ ] Performance-metrics endpoint
* [ ] VaR and Expected Shortfall endpoint
* [ ] Backtesting endpoint
* [ ] Stress-testing endpoint
* [ ] OpenAPI documentation
* [ ] Streamlit dashboard
* [ ] Portfolio overview page
* [ ] Risk-analysis page
* [ ] Backtesting page
* [ ] Stress-testing page
* [ ] API integration tests

### Completion Criteria

Version `v0.8` is complete when users can configure and analyse a portfolio through the dashboard and all analytical operations are accessible through the API.

---

## v0.9 — Quality Assurance, Docker and Continuous Integration

**Status:** `[ ]`

### Objectives

* Harden the application for reproducible execution.
* Validate the integration between all platform components.
* Automate code-quality checks.

### Deliverables

* [ ] Expanded unit-test suite
* [ ] Integration tests
* [ ] Test coverage report
* [ ] Linting
* [ ] Automated formatting checks
* [ ] Static type checking
* [ ] Structured logging
* [ ] Dockerfile
* [ ] Docker Compose configuration
* [ ] GitHub Actions workflow
* [ ] End-to-end execution test

### Completion Criteria

Version `v0.9` is complete when the complete platform can be executed in containers and all automated quality checks pass successfully.

---

## v1.0 — Documentation and Public Release

**Status:** `[ ]`

### Objectives

* Finalise the platform as a complete professional portfolio project.
* Publish a reproducible and well-documented public release.

### Deliverables

* [ ] Final README
* [ ] Installation and execution instructions
* [ ] Architecture documentation
* [ ] Methodology documentation
* [ ] API usage examples
* [ ] Dashboard screenshots
* [ ] Short demonstration video or GIF
* [ ] Limitations and assumptions
* [ ] Final repository cleanup
* [ ] Changelog
* [ ] Version tag `v1.0.0`
* [ ] GitHub release

### Completion Criteria

Version `v1.0` is complete when all mandatory requirements defined in the project specification are implemented, tested, documented and publicly demonstrable.

---

## Post-v1.0 Possibilities

The following features are intentionally excluded from the summer scope and may be considered after version `v1.0`:

* GARCH-based volatility and VaR
* Additional VaR backtesting tests
* Historical crisis replay scenarios
* Risk contribution and component VaR
* Portfolio optimisation
* Additional market-data providers
* Cloud deployment
* User authentication
* Persistent portfolio storage
