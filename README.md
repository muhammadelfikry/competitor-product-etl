# ETL Competitor Fashion Products Pipeline 👕

An ETL pipeline for scraping, transforming, and storing competitor product data from **Fashion Studio**. 
The collected data includes product name, price, rating, colors, sizes, and gender.
The results are loaded into **CSV**, **PostgreSQL**, and **Google Spreadsheet**, making them ready for use by the Data Science team.

## 🚀 Background
In today’s highly competitive fashion industry, analyzing competitor prices and product trends is essential to support business decision-making. 
This project builds an **ETL (Extract, Transform, Load) pipeline** to automate the collection and preparation of product data from [Fashion Studio](https://fashion-studio.dicoding.dev), 
which offers a wide range of fashion products such as t-shirts, pants, jackets, and outerwear.

The data produced by this pipeline can be used by the Data Science team for further analysis, such as:
- Comparing competitor prices.  
- Exploring product variations based on gender, colors, and sizes.  
- Observing product ratings that reflect popularity.  

## 🎯 Project Objectives
1. **Extract**: Scrape product data from the competitor’s website.  
2. **Transform**: Clean and standardize the data to ensure consistency and readiness for analysis.  
3. **Load**: Store the processed data into multiple destinations:  
   - **CSV** file for documentation and portable dataset.  
   - **PostgreSQL Database** for querying and system integration.  
   - **Google Spreadsheet** for easy access by non-technical teams.  

## ⚙️ ETL Pipeline Workflow
1. **Extract**  
   - Technique: Web scraping using `BeautifulSoup`.  
   - Extracted fields:  
     - `title`  
     - `price`  
     - `rating`  
     - `colors`  
     - `size`  
     - `gender`  

2. **Transform**  
   - Convert prices to numeric values.  
   - Extract ratings into decimal numbers.  
   - Standardize colors and sizes.  
   - Add a `Timestamp` column to record scraping time.  

3. **Load**  
   - Save to `products.csv`.  
   - Insert into the `competitor_products` table in PostgreSQL.  
   - Upload to Google Spreadsheet.  

## 🛠️ Technologies Used
- **Python**
- **Libraries**:
  - `requests`, `BeautifulSoup` → Scraping product data  
  - `pandas` → Data transformation  
  - `sqlalchemy`, `psycopg2` → PostgreSQL integration  
  - `google-auth`, `google-api-python-client` → Google Spreadsheet integration  
- **PostgreSQL** → Relational database  
- **Google Spreadsheet** → Easy data access for non-technical teams  

## 📊 Sample Data

| Title     | Price  | Rating | Colors | Size | Gender | Timestamp           |
|-----------|--------|--------|--------|------|--------|---------------------|
| T-Shirt A | 150000 | 4.5    | 3      | M    | Men    | 2025-09-13 15:32:10 |
| Jacket B  | 350000 | 4.8    | 3      | L    | Women  | 2025-09-13 15:32:10 |
| Pants C   | 220000 | 4.2    | 3      | L    | Unisex | 2025-09-13 15:32:10 |

## 🌟 Project Benefits
- **Data Science Team**: Gains access to a clean, ready-to-use dataset.  
- **Management Team**: Easy access via Google Spreadsheet.  
- **Scalability**: The pipeline can be extended to other competitors or integrated into BI dashboards.  

## ✅ Conclusion
This project successfully built an end-to-end ETL pipeline capable of automating the extraction, transformation, and loading of competitor product data. 
With this pipeline, the team gains consistent, structured, and easily accessible competitor product data, accelerating the analysis process and supporting data-driven decision-making.
