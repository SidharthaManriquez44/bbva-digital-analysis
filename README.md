# BBVA Digital Banking Analytics Project

End-to-End Analytical Layer built on top of a Dimensional Data Warehouse to analyze banking performance, digital transformation, and financial growth trends.

--- 
This project simulates a real-world banking analytics environment using a layered architecture:
```text
RAW → STAGING → CORE → MART → ANALYSIS
```
It demonstrates data modeling, ETL orchestration, analytical SQL, and KPI-driven decision-making.

## Business Objective

Transform regulatory banking reports (annual CNBV reports) into an executive-ready analytics layer capable of measuring:

* Financial performance
* Digital adoption
* Operational efficiency
* Year-over-year growth

Designed as if it were serving executive dashboards.

## Architecture
### Data Warehouse (separate repository)
* Star Schema (Dimensional Modeling)
* Surrogate keys in CORE
* Grain: bank + year + channel

### MART Layer
Consolidated annual metrics:
* bank_financial_year
* bank_digital_year
* bank_efficiency_year
* bank_growth_year
* v_bank_executive_dashboard

Growth metrics calculated using SQL window functions (LAG).

This repository consumes only the MART layer.

## Analytical Capabilities
### Financial
* Total Loans
* Total Deposits
* Net Income
* YoY Growth %
### Digital Transformation
* Digital Clients
* Digital Penetration Rate
### Structural Efficiency
* Clients per Branch
* Loans per Branch
* Deposits per Branch
* Profit per Branch
---
## Key Insights
* Post-pandemic contraction detected in 2020
* Strong rebound in 2021 across loans and deposits
* Major efficiency improvement in 2023 (Net Income +25% YoY despite flat asset growth)
* Increasing digital penetration trend

The architecture enables automated KPI validation and reproducible analysis.

## Project Structure
```text
bbva-digital-analysis/
│
├── src/
│   ├── analysis/
│   ├── analytics/
│   ├── data_access/
│   │   └── bank_repository.py
│   ├── config/
│   ├── extract/
│   ├── load/
│   └── pipeline.py
│
├── tests/
├── .env
├── requirements.txt
└── README.md
```
## Design Principles
* Strict separation of DW and Analytics layers
* Fact tables store surrogate keys only
* Business keys exposed in MART only
* Idempotent full refresh strategy
* Analytical SQL using window functions
* Reproducible environment configuration

## Tech Stack
* Python
* PostgreSQL
* SQLAlchemy
* Pandas
* Docker (DW environment)
* Dimensional Modeling
* Window Functions (SQL Analytics)

## How to Run
```bash
pip install -r requirements.txt
python src/run_analysis.py
```
Database credentials must be configured in .env.

---
## What This Project Demonstrates
    ✔ Dimensional modeling fundamentals
    ✔ ETL orchestration with Python
    ✔ Analytical SQL proficiency
    ✔ Window functions for growth calculations
    ✔ KPI-driven thinking
    ✔ End-to-end data architecture understanding
---
## Related Project
bbva-digital-dw (Data Warehouse Layer)

---

## About Me
Data professional focused on building structured, scalable analytical systems.

