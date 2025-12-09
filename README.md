
# **Country GDP Data Pipeline**

This project implements a complete ETL pipeline designed to extract, transform, and load country-level GDP data retrieved from an IMF-referenced webpage. The workflow includes HTML table extraction, numeric standardization, structured storage, and validation through SQL querying. A full logging system captures each execution step to support automation, auditing, and reproducibility.

---

## **1. Purpose**

This module provides an automated ETL workflow that retrieves GDP data from an external webpage, converts the GDP values from USD millions to USD billions (rounded to two decimals), and stores the processed dataset in both CSV and SQLite formats.

To validate successful ingestion, an SQL query is executed to return only countries with economies exceeding 100 billion USD. All operations are logged with timestamped entries for transparency and debugging.

---

## **2. Key Concepts**

This project demonstrates core Data Engineering skills:

* Extraction of structured tabular data from HTML pages.
* Parsing and selection of relevant web-based datasets.
* Numeric cleaning, normalization, and unit conversion.
* Creation of standardized economic metrics.
* Generation of CSV outputs for interoperability.
* Loading structured data into a SQLite relational database.
* Execution of SQL statements for analytical validation.
* End-to-end logging of ETL pipeline operations.

---

## **3. Practical Use**

This pipeline operates as a standalone solution suitable for automated GDP-data retrieval workflows.

It is designed for environments where economic indicators require periodic updates and can be integrated into:

* Data engineering orchestration tools
* Batch or scheduled workflows
* Business intelligence and analytics platforms

The modular structure allows easy extension to additional data sources or transformations.

---

## **4. Project Files**

The repository includes the following components:

* **`etl_project_gdp.py`** — Main ETL pipeline implementation
* **`Countries_by_GDP.csv`** — Processed GDP dataset in CSV format
* **`World_Economies.db`** — SQLite database containing the GDP table
* **`logs/etl_project_log.txt`** — Execution log with timestamped entries

---

## **5. Summary**

This project demonstrates a functional ETL pipeline for processing GDP data sourced from an IMF-referenced dataset. It separates responsibilities into extraction, transformation, loading, querying, and logging stages, delivering a clean, reusable framework for handling country-level economic information in both file-based and relational formats.

---

**Author:** *Daniel Jane Garcia (danij4ne)*
