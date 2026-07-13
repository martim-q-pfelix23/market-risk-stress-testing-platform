# Project Structure

## 1. Overview

This document defines the planned repository structure of the Market Risk and Stress Testing Platform.

The repository uses a `src` layout to separate the installable Python package from application interfaces, tests, documentation and development resources.

The structure may evolve during development, but changes should preserve the separation between analytical logic, external interfaces and infrastructure.

---

## 2. Repository Tree

```text
market-risk-stress-testing-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── exception_handlers.py
│   ├── routers/
│   └── schemas/
│
├── configs/
│   ├── default.yaml
│   └── stress_scenarios.yaml
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   └── components/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── docs/
│   ├── project_specification.md
│   ├── roadmap.md
│   ├── architecture.md
│   ├── project_structure.md
│   └── methodology/
│
├── notebooks/
│   ├── 01_market_data_exploration.ipynb
│   ├── 02_portfolio_analytics.ipynb
│   └── 03_risk_method_validation.ipynb
│
├── reports/
│   ├── figures/
│   └── methodology_note.md
│
├── src/
│   └── market_risk/
│       ├── __init__.py
│       ├── application/
│       ├── data/
│       ├── portfolio/
│       ├── risk/
│       ├── backtesting/
│       ├── stress_testing/
│       ├── models/
│       ├── exceptions.py
│       ├── logging_config.py
│       └── settings.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── conftest.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 3. Directory Responsibilities

### `.github/workflows/`

Contains GitHub Actions workflows.

The continuous integration workflow will run automated checks such as:

* unit and integration tests;
* linting;
* formatting validation;
* static type checking.

---

### `api/`

Contains the FastAPI application and HTTP-specific logic.

This directory is responsible for:

* API startup;
* endpoint routing;
* request and response schemas;
* dependency injection;
* HTTP exception handling;
* OpenAPI exposure.

Financial calculations must not be implemented directly in this directory.

---

### `configs/`

Contains configuration files that do not include secrets.

Examples include:

* default confidence levels;
* simulation parameters;
* annualisation settings;
* predefined stress scenarios.

Secrets or credentials must be supplied through environment variables and must not be committed to the repository.

---

### `dashboard/`

Contains the Streamlit application.

This directory is responsible for:

* user inputs;
* navigation;
* result presentation;
* charts and tables;
* communication with the REST API.

The dashboard must not duplicate calculations implemented in the analytical package.

---

### `data/`

Contains local data used during development.

* `raw/`: unmodified locally retrieved data;
* `processed/`: transformed or aligned datasets;
* `sample/`: small reproducible datasets suitable for tests or demonstrations.

Large external datasets and generated cache files should normally be excluded through `.gitignore`.

---

### `docs/`

Contains the technical and methodological documentation.

It includes:

* project specification;
* development roadmap;
* system architecture;
* repository structure;
* detailed descriptions of financial methodologies.

---

### `notebooks/`

Contains exploratory and validation notebooks.

Notebooks may be used for:

* market-data exploration;
* methodology prototyping;
* comparison with reference calculations;
* visual investigation.

Production functionality must be moved into `src/market_risk/` and must not depend on notebook execution.

---

### `reports/`

Contains final figures and presentation-oriented outputs.

It may include:

* dashboard screenshots;
* architecture images;
* methodology notes;
* final analytical figures.

---

### `src/market_risk/`

Contains the installable core Python package.

#### `application/`

Coordinates application use cases and communication between the analytical modules.

#### `data/`

Implements market-data retrieval, validation, transformation and caching.

#### `portfolio/`

Implements portfolio construction, return calculation and performance analytics.

#### `risk/`

Implements VaR, Expected Shortfall and shared risk calculations.

#### `backtesting/`

Implements rolling VaR validation and statistical backtesting.

#### `stress_testing/`

Implements deterministic market-shock scenarios and loss calculations.

#### `models/`

Contains shared domain and result models used by multiple modules.

#### `exceptions.py`

Defines explicit project-specific exception types.

#### `logging_config.py`

Defines centralised application logging.

#### `settings.py`

Loads and validates platform configuration.

---

### `tests/`

Contains the automated test suite.

* `unit/`: isolated tests for individual functions and classes;
* `integration/`: tests covering communication between components;
* `fixtures/`: reusable deterministic test datasets;
* `conftest.py`: shared pytest configuration and fixtures.

Tests must not rely unnecessarily on live external market-data services.

---

## 4. Root Files

### `README.md`

Provides the primary project overview, installation instructions, usage examples and links to detailed documentation.

### `pyproject.toml`

Defines:

* project metadata;
* Python dependencies;
* optional development dependencies;
* test configuration;
* formatting and linting configuration;
* package build settings.

### `Dockerfile`

Defines the container image used to execute the application.

### `docker-compose.yml`

Coordinates the dashboard and API containers for local execution.

### `Makefile`

Provides convenient commands for common development operations, such as:

```text
make install
make test
make lint
make format
make run-api
make run-dashboard
```

### `.env.example`

Documents the environment variables supported by the platform without exposing actual secret values.

### `CHANGELOG.md`

Records the principal changes introduced in each project version.

### `CONTRIBUTING.md`

Describes development conventions, code-quality expectations and contribution procedures.

### `LICENSE`

Defines the repository licence. The project uses the MIT License.

---

## 5. Repository Rules

The project shall follow these structural rules:

1. Financial calculations belong inside `src/market_risk/`.
2. API routes and dashboard pages must call the analytical package rather than duplicate its logic.
3. Notebooks are used for exploration and validation, not as production dependencies.
4. External-provider formats must not propagate beyond the data layer.
5. Tests should use deterministic local fixtures whenever possible.
6. Generated files, caches, credentials and large external datasets must not be committed.
7. Every new module should have a clear responsibility and corresponding tests.
