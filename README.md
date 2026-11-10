# Real-Time Fraud Detection & Velocity Engine

A lightweight, high-performance real-time fraud detection simulation engine built with **MySQL** and **Python**. This project demonstrates how to model transactional data, optimize complex queries with advanced indexing and database views, stream mock traffic (including card-testing attacks), and monitor alerts live via an interactive terminal dashboard.

---

## 🚀 Features

- **Relational Schema**: Core tables for `users`, `devices` (IP tracking & fingerprinting), `orders`, and `payments` (status tracking & card details) with foreign key constraints.
- **Velocity Check Engine**: Database views and analytical queries designed to flag rapid-fire suspicious activities (default: $\ge 3$ failed payment attempts in $< 60$ seconds).
- **Performance Optimized**: Built-in indexing on high-frequency filter columns (`payment_status`) and composite time window indexes.
- **Data Generator Simulation**: A Python-powered stream generator using `Faker` to continuously ingest legitimate traffic and simulated card-testing fraud attacks.
- **Live Terminal UI Dashboard**: Real-time monitoring dashboard built with `rich` that updates in-place to display active fraud alerts and metrics.

---

## 📂 Project Structure

```text
├── database_setup.sql        # Core DDL for creating database and tables
├── 5.indexing.sql            # Performance indexes for foreign keys and velocity checks
├── 6_power_run.sql           # SQL view (vw_fraud_velocity_alerts) for live fraud detection
├── analytix.sql              # Ad-hoc analytical query for ranked fraud reports
├── data_generator_engine.py  # Python script simulating real-time user traffic & attacks
└── dashboard.py              # Rich-powered terminal live dashboard
```

---

## 🛠️ Prerequisites & Requirements

- **MySQL Server** (v8.0+ recommended)
- **Python** (v3.8+)
- Python Packages:
  - `mysql-connector-python`
  - `faker`
  - `rich`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fraud-detection-engine.git
cd fraud-detection-engine
```

### 2. Set Up the Database
Execute the SQL scripts in order in your MySQL client or command line:
```sql
SOURCE database_setup.sql;
SOURCE 5.indexing.sql;
SOURCE 6_power_run.sql;
```

### 3. Install Python Dependencies
```bash
pip install mysql-connector-python faker rich
```

### 4. Configure Database Credentials
Update the database connection settings (`host`, `user`, `password`, `database`) inside both `data_generator_engine.py` and `dashboard.py` to match your local MySQL configuration.

---

## 🖥️ Running the Simulation

To see the engine in action, run the data generator and the dashboard concurrently in two separate terminal windows:

### Terminal 1: Start the Ingestion Engine
```bash
python data_generator_engine.py
```
*(This simulates normal user transactions mixed with burst fraud attacks).*

### Terminal 2: Launch the Live Monitoring Dashboard
```bash
python dashboard.py
```
*(This displays a live, refreshing terminal UI showing real-time fraud alerts and blocked statistics).*

---

## 📊 How Velocity Rules Work
The core detection logic groups transactions by device IP and user email within sliding time windows. If a device triggers multiple failed payment attempts within a short interval, it surfaces instantly on the monitoring dashboard for security review.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
