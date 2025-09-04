# Sales Incentive Analytics Pipeline

## 📌 Overview

**Sales Incentive Analytics** is an end-to-end **Data Engineering project** that automates the processing of raw sales data from

**AWS S3 → Spark ETL → MySQL Data Marts → S3 Reporting Zones.**

It simulates a real-world data pipeline for **retail sales and incentive calculation**:

- Ingest raw sales data from **AWS S3**
- Perform **data quality checks** (schema validation, error handling, staging table updates)
- Transform sales data using **PySpark (ETL)**
- Enrich with **dimension tables** (customer, store, product, sales_team)
- Generate two data marts:
  - 🧑‍🤝‍🧑 **Customer Data Mart** → monthly purchase behavior
  - 👨‍💼 **Sales Team Data Mart** → sales performance + incentives
- Write processed data to **S3 (Parquet)** and **MySQL tables**
- Move files to **processed/error folders** and clean up local staging

---

## 🎯 Project Highlights

This project demonstrates:

✅ Data Ingestion  
✅ Data Transformation  
✅ Data Quality  
✅ Data Marts  
✅ Cloud Storage  
✅ Incentive Analytics

---

## 🛠️ Tech Stack

- **Programming:** Python 3, PySpark
- **Data Storage:** AWS S3 (raw, processed, error zones), MySQL (data marts)
- **ETL:** PySpark DataFrames, SQL transformations
- **Workflow:** Boto3 (S3), Spark Session, Custom Utility Modules
- **Logging:** Python logging
- **Deployment:** Local / Cloud-ready

---

```


## Project Architecture
![Pipeline Architecture](docs/Pipeline_Architecture.png)

## Database ER Diagram
![Database ER Diagram](docs/database_schema.drawio.png)



```

```plaintext
Project structure:-
SALES_INCENTIVE_ANALYTICS/
├── docs/
│   └── readme.md
├── resources/
│   ├── __init__.py
│   ├── dev/
│   │    ├── config.py
│   │    └── requirement.txt
│   └── qa/
│   │    ├── config.py
│   │    └── requirement.txt
│   └── prod/
│   │    ├── config.py
│   │    └── requirement.txt
│   ├── sql_scripts/
│   │    └── table_scripts.sql
├── src/
│   ├── main/
│   │    ├── __init__.py
│   │    └── delete/
│   │    │      ├── aws_delete.py
│   │    │      ├── database_delete.py
│   │    │      └── local_file_delete.py
│   │    └── download/
│   │    │      └── aws_file_download.py
│   │    └── move/
│   │    │      └── move_files.py
│   │    └── read/
│   │    │      ├── aws_read.py
│   │    │      └── database_read.py
│   │    └── transformations/
│   │    │      └── jobs/
│   │    │      │     ├── customer_mart_sql_transform_write.py
│   │    │      │     ├── dimension_tables_join.py
│   │    │      │     ├── main.py
│   │    │      │     └──sales_mart_sql_transform_write.py
│   │    └── upload/
│   │    │      └── upload_to_s3.py
│   │    └── utility/
│   │    │      ├── encrypt_decrypt.py
│   │    │      ├── logging_config.py
│   │    │      ├── s3_client_object.py
│   │    │      ├── spark_session.py
│   │    │      └── my_sql_session.py
│   │    └── write/
│   │    │      ├── database_write.py
│   │    │      └── parquet_write.py
│   ├── test/
│   │    ├── scratch_pad.py.py
│   │    └── generate_csv_data.py
```

## ⚙️ How the Pipeline Works

### 🔹 Step 0: Data Generation (Simulation)

Since real retail sales data is not readily available, this project **generates synthetic sales data** using custom Python scripts.

- Generates randomized Customer, Store, Product, and Sales Team data
- Creates transactional sales CSV files (with realistic schema)
- Uploads generated files to **AWS S3 (raw zone)**  
  👉 This simulates a real-world system continuously pushing sales data into S3.

---

### 🔹 Step 1: S3 → Local (Ingestion)

- Connects to AWS S3 (via Boto3)
- Lists and downloads sales CSVs
- Validates mandatory schema columns

### 🔹 Step 2: Data Quality & Staging

- Moves bad files to `error/` folder (locally + S3)
- Updates MySQL staging table with file status (Active/Inactive)

### 🔹 Step 3: Transformation (PySpark)

- Cleans extra columns → consolidates into `additional_column`
- Joins with dimension tables (Customer, Store, Product, Sales Team)
- Produces **Fact Table** of enriched sales transactions

### 🔹 Step 4: Data Marts

- **Customer Data Mart** → monthly purchase summary per customer
- **Sales Team Data Mart** → monthly sales per person + incentive calculation (top performers get 1% of sales)

### 🔹 Step 5: Write to Storage

- Local Parquet → Upload to S3 (processed zone)
- Partitioned data by `sales_month` & `store_id` for efficient querying
- Insert results into MySQL Data Mart tables

### 🔹 Step 6: Cleanup

- Moves raw files → `processed/` S3 folder
- Deletes temporary local files

---

````
## 🧑‍💻 Setup & Run

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/sales-incentive-analytics.git
cd sales-incentive-analytics
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure `resources/dev/config.py`

Update values for:

- AWS credentials (encrypted)
- MySQL connection (url, user, password)
- Bucket names, folder paths
- Mandatory schema columns

### 4️⃣ Run pipeline

```bash
python src/main/main.py
```

---

## ✅ Features

- Automated ETL pipeline (**raw → processed → marts**)
- Data quality checks (missing schema, bad files segregation)
- Encrypted AWS credentials
- Parquet + partitioned storage for scalability
- MySQL integration for analytics & reporting

---

## 🚀 Future Enhancements

- Orchestrate with **Apache Airflow**
- Store marts in **Snowflake / Redshift**
- Add **Power BI / Tableau dashboards**
- Implement **CI/CD (GitHub Actions)**
- Add **unit tests (pytest)**

---

## 📄 License

MIT License

---

## 🙌 Author

👤Yashwant Yadav
📧 \[[yashwantyadav2003@gmail.com]]
🔗 [LinkedIn](https://www.linkedin.com/in/yashwant-yadav14) | [GitHub](https://github.com/Yashwant-14)
