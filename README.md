# Modular Python Data Processing Pipeline

A configurable, production-grade ETL pipeline built in Python to ingest, clean, transform, and output structured data from CSV files, JSON documents, or HTTP REST APIs.

## Key Features

- **Multi-Source Ingestion**: Load raw data seamlessly from standard CSVs, JSON arrays/objects, or external REST endpoints.
- **Config-Driven Cleaning**: Modify missing data strategies, coercion types, and output targets directly via `config/pipeline_config.yaml` without editing python code.
- **Robust Type Handling**: Automatic conversion of integers, floats, datetimes, and boolean flags with coercion edge-case guards.
- **Structured Operations**: Handles deduplication, string imputation, numerical median/mean backfilling, and null handling.
- **Logging & Verification**: Console and file-level logging tracking record count transformations.

## Quick Start Setup

### 1. Prerequisites & Environment
Ensure you have Python 3.9+ installed. Clone the repository and navigate into the folder:

```bash
git clone [https://github.com/your-username/python-data-pipeline.git](https://github.com/your-username/python-data-pipeline.git)
cd python-data-pipeline