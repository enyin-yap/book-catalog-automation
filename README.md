# 📚 Book Catalog Metadata Pipeline

A data pipeline that processes ISBN-based book catalogs by aggregating metadata from multiple sources and exporting structured Excel reports.

---

## 🚀 Features

- 📥 CSV input with ISBN data
- 🌐 Metadata enrichment via Google Books & Open Library
- 🏷️ Price scraping for Chinese book listings
- 🧠 Data merging across multiple sources
- 📊 Data quality handling (missing fields, fallback logic)
- 📤 Excel output generation
- 💻 Dual interface:
  - CLI (command-line)
  - Streamlit web UI

---

## 🎬 Demo

A short video demonstration of the system showing the full workflow from uploading an ISBN CSV (or running the CLI), through metadata aggregation and processing, to generating a structured multi-sheet Excel output with data quality insights.

▶️ Watch Demo: [link here]

---

## 🧠 Project Motivation

Many book catalogs contain incomplete or inconsistent metadata across different sources, making it difficult to maintain reliable records.
This project automates the aggregation of book information from multiple APIs, applying fallback logic, data standardization to improve data consistency, and evaluates data quality using a completeness score across key fields. It focuses on handling real-world incomplete data and quantifying metadata quality rather than assuming full coverage.

---

## ⚙️ How It Works

1. Load ISBN data from CSV  
2. Fetch metadata from:
   - Google Books API (primary)
   - Open Library (fallback)
   - Mandarin source (price scraping)
3. Merge results with priority logic  
4. Clean and normalize fields  
5. Export structured Excel output  

---

## 💻 Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run CLI version

```bash
python main.py --input data/test.csv
```
Output will be saved in the /output folder.

### 3. Run Streamlit UI

```bash
streamlit run app.py
```

Then:
- Upload CSV file
- Click Run Pipeline
- Download Excel output
---

## 📊 Example Input

The input consists of a CSV file containing ISBN-based book records. Each row typically includes a product ID, categories, ISBN number, quantity, and conditions. This format allows the pipeline to process multiple book entries in batch for metadata aggregation.

Example input:

```csv
product_id,categories,isbn,quantity,conditions
40044,70,9789814266727,1,Condition A
40045,70,9789670960968,1,Condition A
40046,70,9789863429487,1,Condition A
```

## 📈 Output

The final output is an Excel file containing multiple sheets that combine aggregated book metadata with data quality analysis.

The main sheet (books_info) contains standardized book records with fields such as title, author, publisher, publication date, pages, price, and description. Each record includes a data completeness score representing the proportion of successfully retrieved metadata fields.

Additional analytical sheets include:

- Insights Sheet: Dataset-level summary including total books, missing field rates, API success rates, average price, and overall data quality distribution, with bar chart of missing data overview.
- Data Issues Sheet: A per-ISBN breakdown of missing fields, showing exactly which metadata attributes are unavailable for each record.
- Quality Ranking Sheet: Books ranked by data completeness score, grouped into Top 10 and Bottom 10 categories for quick identification of high- and low-quality records.

---

## ⚠️ Limitations

This system depends on external APIs and web scraping sources, which means data completeness and accuracy are influenced by source availability and coverage. Some ISBNs may return partial or missing metadata due to API limitations or regional data gaps. In addition, processing time may vary depending on network latency and external service response times.

---

## 🚀 Future Improvements
- introduce parallel API requests to improve processing speed
- expand support for more reliable Chinese book data sources
- implement real-time per-ISBN progress tracking
- introduce caching mechanisms to reduce repeated API calls and improve performance

---

## 👤 Author

Yap En Yin

---

## 📄 License

This project is licensed under the MIT License.






