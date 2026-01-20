Mumbai Housing Valuation Engine (MHVE) 🦁

A production-grade Data Engineering and Machine Learning pipeline for real estate arbitrage analysis.

🚀 Live Demo
https://housing-valuation-engine-zdm6p4rhehytc6cxjgmgsf.streamlit.app/ 

## 🏗️ System Architecture
The MHVE is built on a modular ETL (Extract, Transform, Load) architecture:
- Ingestion: Synthetic data generation engine producing 10k logical records.
- Storage: ACID-compliant SQLite relational database with optimized indexing.
- Intelligence: Scikit-Learn Linear Regression model with 95.49% R² accuracy.
- Observability: Centralized logging framework for pipeline health monitoring.

🛠️ Engineering Highlights
- Schema Evolution: Executed a database migration to include BHK features, resolving an initial 24% model accuracy bottleneck.
- One-Hot Encoding: Implemented categorical vectorization for high-variance locality data.
- Environment Parity: Managed cross-platform dependency pinning for seamless Linux/macOS deployment.

🚀 Strategic Overview
The Mumbai Housing Valuation Engine (MHVE) is a professional-grade Data Engineering pipeline designed to identify undervalued 2BHK properties. In a market as opaque as Mumbai's, this engine democratizes data by calculating "Fair Value" metrics, helping families make data-backed investment decisions.

> Business Value: Automatically flags properties priced 15%+ below suburb averages, significantly reducing manual research time.

---

🛠️ Tech Stack
- Languages: Python 3.11+, SQL (PostgreSQL)
- Data Engineering: SQLAlchemy, Pandas, Numpy
- Environment: Docker (Planned for Phase 2)
- Version Control: Git/GitHub

---

📊 Data Dictionary
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
```
SELECT 
    locality, 
    price_cr,
    AVG(price_cr) OVER(PARTITION BY locality) as avg_locality_price,
    (price_cr - AVG(price_cr) OVER(PARTITION BY locality)) as deviation
FROM mumbai_properties
WHERE bhk = 2
ORDER BY deviation ASC;
```
---

⚙️ Installation & Setup

Clone the repo: git clone https://github.com/hirenmanani/housing-valuation-engine.git

Install dependencies: pip install -r requirements.txt

Configure Database: Update main.py with your PostgreSQL credentials.

Run Pipeline: python main.py

---

📅 Roadmap to Production

[x] Phase 1: Core ETL Logic & SQL Schema (Completed)

[x] Phase 2: Containerization with Docker for environment parity (Current)

[ ] Phase 3: Automated Data Validation (Great Expectations).

[ ] Phase 4: Price Prediction Engine (Linear Regression).

---

👤 Author

Hiren Manani | Data Engineering Candidate | Graduating May 2026
