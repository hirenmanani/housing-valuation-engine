Mumbai Housing Valuation Engine (MHVE) 🏠📊

🚀 Strategic Overview
The Mumbai Housing Valuation Engine (MHVE) is a professional-grade Data Engineering pipeline designed to identify undervalued 2BHK properties. In a market as opaque as Mumbai's, this engine democratizes data by calculating "Fair Value" metrics, helping families make data-backed investment decisions.

> Business Value:** Automatically flags properties priced 15%+ below suburb averages, significantly reducing manual research time.


## 🏗️ System Architecture
The project follows a modular ETL (Extract, Transform, Load pattern:

1. Extraction: Python scripts ingest raw property data (Price, Locality, Sq Ft) from market datasets.
2. Transformation: Data cleaning using `Pandas` to handle nulls and normalize price metrics (Cr to INR).
3. Loading: Structured data is pushed into a **PostgreSQL** instance for analytical querying.
4. Orchestration: (Planned) Integration with **Apache Airflow** for daily automated runs.

---

🛠️ Tech Stack
- Languages: Python 3.11+, SQL (PostgreSQL)
- Data Engineering: SQLAlchemy, Pandas, Numpy
- Environment: Docker (Planned for Phase 2)
- Version Control: Git/GitHub

---

## 📊 Data Dictionary
| Field | Type | Description |
| :--- | :--- | :--- |
| `property_id` | UUID | Unique identifier for each listing. |
| `price_cr` | Float | Price in Crores (normalized for analysis). |
| `sq_ft` | Int | Total carpet area in square feet. |
| `price_per_sqft` | Float | Key metric: (Price * 1e7) / sq_ft. |
| `suburb_rank` | Int | Calculated rank based on price deviation from locality mean. |

---

💡 Engineering Highlights (SQL Logic)
To identify "Gains," I utilize Window Functions to rank properties within their specific localities without collapsing the dataset:

- sql
Calculating price deviation from suburb average to find outliers
SELECT 
    locality, 
    price_cr,
    AVG(price_cr) OVER(PARTITION BY locality) as avg_locality_price,
    (price_cr - AVG(price_cr) OVER(PARTITION BY locality)) as deviation
FROM mumbai_properties
WHERE bhk = 2
ORDER BY deviation ASC;

---

⚙️ Installation & Setup

Clone the repo: git clone https://github.com/yourusername/mumbai-housing-valuation-engine.git

Install dependencies: pip install -r requirements.txt

Configure Database: Update main.py with your PostgreSQL credentials.

Run Pipeline: python main.py

---

📅 Roadmap to Production

[x] Phase 1: Core ETL Logic & SQL Schema (Current)

[ ] Phase 2: Containerization with Docker for environment parity.

[ ] Phase 3: Automated Data Validation (Great Expectations).

[ ] Phase 4: Price Prediction Engine (Linear Regression).

---

👤 Author

Hiren Manani | Data Engineering Candidate | Graduating May 2026
