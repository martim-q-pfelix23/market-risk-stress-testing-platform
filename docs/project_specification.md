# End-to-End Market Risk and Stress Testing Platform

## 1. Project Overview

This project aims to develop an end-to-end Market Risk and Stress Testing Platform that reproduces selected components of a real-world financial risk analytics workflow.

Rather than attempting to predict the future price or direction of individual financial assets, the platform focuses on measuring, evaluating, validating and communicating the market risk associated with an investment portfolio using established quantitative finance methodologies.

The application will enable users to construct and analyse portfolios based on historical market data. It will provide a clear set of portfolio performance and risk indicators, including historical returns, volatility, Value at Risk (VaR), Expected Shortfall (ES), drawdown analysis and losses under adverse market scenarios.

Multiple risk estimation methodologies will be implemented and compared, allowing users to understand the assumptions, strengths and limitations of each approach.

The platform will combine a modular Python analytical engine, a REST API, an interactive dashboard, automated testing, continuous integration and containerised deployment. The objective is to demonstrate how quantitative financial analysis can be transformed into a reproducible, maintainable and product-oriented software application.

This project is designed as a technical and educational demonstration of a modern financial risk analytics system. It is not intended to provide investment advice, execute trades or replace the risk infrastructure used by regulated financial institutions.

---

## 2. Problem Statement

Investment portfolios are exposed to changes in asset prices, volatility and correlations between financial instruments. Measuring this exposure requires more than observing historical returns or calculating a single risk indicator.

A complete market risk workflow should be able to:

* construct and validate a portfolio;
* retrieve and process historical market data;
* calculate portfolio-level performance and risk measures;
* estimate potential losses using different methodologies;
* evaluate the reliability of those risk estimates;
* simulate adverse market conditions;
* communicate the results clearly to users.

Many educational financial projects concentrate on asset-price prediction or implement isolated risk calculations in notebooks. This project instead focuses on integrating the principal stages of a market risk workflow into a single modular and testable application.

---

## 3. Key Objectives

The main objectives of the project are to:

* Develop a modular platform for market risk analysis using Python.
* Construct and evaluate investment portfolios based on historical market data.
* Calculate portfolio performance and risk indicators.
* Implement multiple Value at Risk methodologies, including:

  * Historical Simulation;
  * Parametric or Variance-Covariance VaR;
  * Monte Carlo Simulation.
* Estimate Expected Shortfall and complementary risk measures.
* Perform stress testing under predefined adverse market scenarios.
* Validate VaR estimates through rolling backtesting and statistical tests.
* Provide an interactive dashboard for portfolio monitoring and risk visualisation.
* Expose the analytical functionality through a documented REST API.
* Apply software engineering best practices, including testing, type annotations, logging, continuous integration, documentation and containerisation.
* Deliver a complete and publicly demonstrable version of the platform during the summer development period.

---

## 4. Target Users

The platform is primarily designed for the following users:

### 4.1 Financial Risk and Portfolio Analysts

Users who need to examine the historical behaviour, risk exposure and sensitivity of a portfolio under different market conditions.

### 4.2 Data Science and Quantitative Finance Students

Users interested in understanding how market risk methodologies can be implemented, compared and validated within a reproducible software system.

### 4.3 Technical Reviewers and Recruiters

Data science, financial technology and software engineering professionals evaluating the architecture, analytical methodology and engineering quality of the project.

The platform is not intended for retail investors seeking personalised investment recommendations.

---

## 5. Functional Requirements

### FR-01 - Market Data Acquisition

The system shall retrieve historical daily market data for a user-selected set of financial assets from a public market-data provider.

The data layer shall:

* retrieve adjusted historical prices;
* support a configurable date range;
* detect missing or invalid observations;
* align asset time series by trading date;
* provide clear errors when requested data cannot be obtained.

### FR-02 - Portfolio Construction

The system shall allow the user to define a portfolio by specifying:

* asset identifiers;
* portfolio weights;
* analysis period;
* initial portfolio value;
* optional benchmark.

The system shall validate that:

$\sum_{i=1}^{n} w_i = 1$


where ($w_i$) represents the weight of asset ($i$).

Invalid portfolios, including portfolios with missing assets or incorrectly specified weights, shall be rejected with an informative error message.

### FR-03 - Return Calculation

The system shall calculate individual asset returns and aggregate portfolio returns.

The default return definition shall be the logarithmic return:


$r_{i,t} = \ln\left(\frac{P_{i,t}}{P_{i,t-1}}\right)$


The portfolio return shall be calculated as:


$r_{p,t} = \sum_{i=1}^{n} w_i r_{i,t}$


### FR-04 - Portfolio Performance Analysis

The platform shall calculate and display:

* cumulative return;
* annualised return;
* annualised volatility;
* Sharpe ratio;
* maximum drawdown;
* rolling volatility;
* asset correlation matrix;
* portfolio value over time.

### FR-05 - Value at Risk Estimation

The platform shall estimate Value at Risk using:

* Historical Simulation;
* Parametric Variance-Covariance;
* Monte Carlo Simulation.

The methods shall support, at minimum:

* 95% confidence level;
* 99% confidence level;
* one-day risk horizon.

The system shall report both percentage and monetary VaR values.

### FR-06 - Expected Shortfall Estimation

The system shall estimate Expected Shortfall for the supported confidence levels.

Expected Shortfall shall represent the expected loss conditional on the portfolio loss exceeding the corresponding VaR threshold:


$-\mathbb{E}
\left[
r_p
\mid
r_p \leq q_{1-\alpha}(r_p)
\right]$

### FR-07 - VaR Backtesting

The platform shall perform rolling backtesting of VaR estimates by comparing predicted loss thresholds with realised portfolio returns.

A VaR exception shall be defined as:

$
I_t =
\mathbb{1}
\left(
r_{p,t} < -VaR_{\alpha,t}
\right)
$

The backtesting component shall include:

* number of VaR exceptions;
* observed exception rate;
* expected exception rate;
* visual identification of exceptions;
* Kupiec Proportion of Failures test.

### FR-08 - Stress Testing

The platform shall evaluate the effect of predefined adverse scenarios on the portfolio.

The initial version shall support deterministic scenarios such as:

* broad equity market decline;
* technology-sector decline;
* banking-sector shock;
* cryptocurrency market decline;
* volatility increase;
* simultaneous cross-asset risk-off scenario.

Each scenario shall specify explicit shocks by asset or asset category.

The platform shall report:

* total portfolio loss;
* percentage portfolio loss;
* loss contribution by asset;
* portfolio value before and after the scenario.

### FR-09 - Interactive Dashboard

The system shall provide an interactive dashboard containing:

* portfolio configuration;
* portfolio overview;
* historical performance;
* risk metrics;
* VaR and Expected Shortfall results;
* VaR backtesting results;
* stress-testing results;
* portfolio composition;
* asset correlations;
* drawdown visualisation.

### FR-10 - REST API

The analytical engine shall be accessible through a REST API.

The API shall expose endpoints for:

* system health;
* portfolio validation;
* portfolio performance metrics;
* VaR and Expected Shortfall estimation;
* stress testing;
* backtesting.

The API shall provide automatically generated OpenAPI documentation.

### FR-11 - Result Export

The platform should allow relevant analytical results to be exported in a structured format such as JSON or CSV.

---

## 6. Non-Functional Requirements

### NFR-01 - Modularity

The analytical engine, data-access layer, API and dashboard shall be separated into distinct modules.

Financial calculations shall not be implemented directly inside dashboard or API components.

### NFR-02 - Reproducibility

The project shall define its dependencies and runtime configuration explicitly.

Monte Carlo simulations shall support a configurable random seed so that results can be reproduced.

### NFR-03 - Testability

Core financial calculations shall be covered by automated unit tests.

Tests shall include:

* normal input cases;
* invalid input cases;
* numerical edge cases;
* deterministic reference examples.

Integration tests shall verify communication between the analytical engine and REST API.

### NFR-04 - Maintainability

The codebase shall use:

* clear module boundaries;
* descriptive naming;
* type annotations;
* docstrings;
* centralised configuration;
* structured logging;
* consistent formatting and linting rules.

### NFR-05 - Performance

The platform shall provide interactive response times for normal demonstration workloads, such as portfolios containing up to 20 assets and approximately 10 years of daily observations.

Computationally intensive operations, particularly Monte Carlo simulation, shall be implemented efficiently using vectorised numerical operations where appropriate.

### NFR-06 - Reliability

The platform shall handle:

* unavailable assets;
* missing observations;
* inconsistent date ranges;
* invalid portfolio weights;
* insufficient historical data;
* numerical calculation failures.

Errors shall be communicated through informative messages rather than unhandled exceptions.

### NFR-07 - Portability

The complete application shall be executable through a containerised environment.

A new user should be able to run the platform using documented setup commands without manually configuring the internal Python modules.

### NFR-08 - Continuous Integration

Every relevant code change shall be automatically checked through a continuous integration workflow containing, at minimum:

* automated tests;
* linting;
* code-format validation.

### NFR-09 - Documentation

The repository shall include:

* project overview;
* installation instructions;
* usage instructions;
* architecture documentation;
* methodological explanations;
* API documentation;
* limitations;
* dashboard screenshots;
* project roadmap.

---

## 7. Risk and Performance Metrics

The first complete release shall implement the following metrics.

### Portfolio Performance

* Cumulative return
* Annualised return
* Annualised volatility
* Sharpe ratio
* Maximum drawdown
* Rolling volatility

### Market Risk

* Historical VaR
* Parametric VaR
* Monte Carlo VaR
* Historical Expected Shortfall
* Parametric Expected Shortfall, where applicable
* Monetary and percentage loss estimates

### Portfolio Structure

* Asset weights
* Correlation matrix
* Asset-level performance
* Loss contribution under stress scenarios

### Model Validation

* VaR exception count
* VaR exception rate
* Kupiec Proportion of Failures test
* Backtesting visualisation

Additional measures may be included after the mandatory version 1.0 scope has been completed.

---

## 8. Data Requirements

The platform shall use publicly accessible historical market data.

The primary dataset shall contain:

* trading date;
* adjusted closing price;
* asset identifier;
* sufficient historical observations for the requested analysis.

Adjusted prices shall be preferred because they account for events such as stock splits and dividend distributions.

The initial version shall use daily observations. Intraday market data is outside the scope of version 1.0.

The data layer shall be designed so that the external data provider can be replaced without changing the portfolio and risk calculation modules.

The project shall not permanently redistribute large quantities of externally sourced market data. Locally cached or sample datasets may be included only when legally and technically appropriate.

---

## 9. Scope Exclusions

The following features are outside the scope of version 1.0:

* future asset-price prediction;
* automated trading;
* portfolio optimisation;
* personalised investment advice;
* broker integration;
* order execution;
* real-time or intraday market data;
* credit risk modelling;
* fraud detection;
* derivative pricing;
* regulatory capital calculation;
* multi-user authentication;
* cloud-scale deployment;
* production use by a regulated financial institution.

These exclusions prevent unnecessary expansion of the project and preserve a realistic summer development scope.

---

## 10. Assumptions and Limitations

The project is subject to the following assumptions and limitations:

* Historical market behaviour does not guarantee future outcomes.
* Historical Simulation assumes that past return observations are representative of possible future losses.
* Parametric VaR may rely on distributional assumptions that do not adequately represent skewness, heavy tails or extreme market events.
* Monte Carlo results depend on the selected return model, estimated parameters and number of simulations.
* Correlations and volatility may change significantly during periods of market stress.
* Deterministic stress scenarios simplify the complex interactions that occur during real financial crises.
* Liquidity risk, transaction costs, taxes and market impact are not modelled in version 1.0.
* Data quality and availability depend on the selected external market-data provider.
* The platform is an educational and portfolio project and is not validated for regulatory or commercial use.

---

## 11. Version 1.0 Completion Criteria

Version 1.0 shall be considered complete when all of the following conditions are satisfied:

* A portfolio can be created and validated using multiple financial assets.
* Historical data can be retrieved and processed through the data layer.
* All mandatory portfolio performance metrics are available.
* Historical, Parametric and Monte Carlo VaR are implemented.
* Expected Shortfall is implemented.
* Rolling VaR backtesting and the Kupiec test are implemented.
* At least five documented stress scenarios are available.
* The analytical engine is accessible through a REST API.
* The principal results are available through an interactive dashboard.
* Invalid inputs and common data failures are handled appropriately.
* Core financial calculations are covered by automated tests.
* Continuous integration successfully executes the project quality checks.
* The application can be executed through a documented containerised setup.
* The README contains installation, execution and usage instructions.
* Architecture and methodology documentation are complete.
* Dashboard screenshots or a short demonstration are included.
* The repository contains no unfinished mandatory functionality.
* A tagged GitHub release named `v1.0.0` is published.

---

## 12. Skills Demonstrated

The project combines quantitative finance, data analysis and software engineering in a single application.

It is intended to demonstrate competencies in:

* Quantitative Finance
* Financial Risk Management
* Python Software Development
* Statistical Modelling
* Financial Data Analysis
* REST API Development
* Interactive Data Visualisation
* Modular Software Architecture
* Automated Testing
* Continuous Integration
* Containerisation
* Technical Documentation
* Reproducible Analytical and Data Pipelines

---

## 13. Disclaimer

This project is developed exclusively for educational and portfolio purposes.

The calculations, simulations and outputs produced by the platform do not constitute financial advice, investment recommendations or guarantees regarding future financial performance.
