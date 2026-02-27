Mumbai Housing Valuation Engine (MHVE) 🦁

A Production-style, end-to-end Data Engineering pipeline built while learning Spark, SQL, and Docker, designed for real estate arbitrage analysis using distributed computing and containerized microservices.

🚀 Live Demo: [View Dashboard](https://housing-valuation-engine-zdm6p4rhehytc6cxjgmgsf.streamlit.app/)

---

## 🏗️ System Architecture
The MHVE is built on a modular, decoupled ETL (Extract, Transform, Load) architecture:
- Orchestration: Docker & Docker Compose** managing isolated services (App, DB, Spark) for environment parity.
- Processing: Apache Spark engine for distributed data enrichment and feature engineering.
- Storage: PostgreSQL relational database (replacing initial SQLite) for persistent, ACID-compliant data storage.
- Intelligence: Scikit-Learn Linear Regression model with 95.49% R² accuracy.

---

🛠️ Engineering Highlights
- Distributed ETL: Scaled processing logic using Spark to handle complex joins and calculate luxury indices across 2,400+ listings.
- Schema Evolution: Executed a full-stack migration from raw CSV sources through a JDBC bridge to a normalized Postgres schema.
- One-Hot Encoding: Implemented categorical vectorization for high-variance locality data to optimize model training.
- Environment Parity: Leveraged Docker to eliminate "it works on my machine" issues, ensuring seamless deployment across macOS and Linux.

---

🚀 Strategic Overview
The MHVE democratizes real estate data by calculating "Fair Value" metrics in Mumbai's opaque market. By identifying properties priced significantly below neighborhood averages, it enables data-backed investment decisions.

> Business Value: Automatically flags properties priced 15%+ below suburb averages, reducing manual market research time by ~80%.

---

🛠️ Tech Stack
- Languages: Python 3.11, SQL (PostgreSQL)
- Data Engineering: Apache Spark, SQLAlchemy, Pandas, JDBC
- Environment: Docker, Docker Compose
- Visualization: Streamlit, Plotly Express

---

## 📊 Data Dictionary
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | BigInt | Unique identifier for each listing. |
| `locality` | Text | The specific neighborhood in Mumbai. |
| `price_cr` | Float | Price in Crores (normalized). |
| `sqft` | Int | Total carpet area in square feet. |
| `luxury_index` | Float | Calculated metric (0-1) based on price deviation from locality mean. |

---

💡 SQL Logic: Identifying Market "Steals"
To detect arbitrage opportunities, I utilize **Window Functions** to rank properties within specific localities without collapsing the record-level granularity:

```sql
SELECT 
    locality, 
    price_cr,
    AVG(price_cr) OVER(PARTITION BY locality) as avg_locality_price,
    (price_cr - AVG(price_cr) OVER(PARTITION BY locality)) as deviation
FROM enriched_properties
ORDER BY deviation ASC
LIMIT 5;
```

⚙️ Installation & Setup (Dockerized)

Clone the repo:

git clone [https://github.com/hirenmanani/housing-valuation-engine.git](https://github.com/hirenmanani/housing-valuation-engine.git)
cd housing-valuation-engine
Create a .env file with your DB credentials

Launch the Stack:    
docker-compose up --build

Access the Dashboard: Navigate to http://localhost:8501 in your browser.

---

📅 Roadmap to Production

[x] Phase 1: Core ETL Logic & SQL Schema.

[x] Phase 2: Containerization with Docker & Multi-service Orchestration.

[x] Phase 3: Distributed Processing with Apache Spark.

[x] Phase 4: Price Prediction Engine (Linear Regression).

[ ] Phase 5: Automated Data Validation (Great Expectations).

---

What I Learned Building This
- Why distributed processing (Spark) matters and when it does NOT
- How schema design impacts downstream analytics
- Tradeoffs between SQLite and Postgres
- How Docker simplifies environment reproducibility
- How SQL window functions enable advanced analytics without aggregation loss

---

👤 Author

Hiren Manani | M.S. in Computer Science, Syracuse University (Expected May 2026) 
Specialization: Data Engineering & Distributed Systems

![Python](https://img.shields.io/badge/python-3.11-blue)
![Docker](https://img.shields.io/badge/docker-ready-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

