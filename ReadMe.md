# 🚀 Cross-Chain Asset Simulator + Alerts System

## 📌 Overview

This project is a **backend-focused REST API system** that simulates a cross-chain asset platform inspired by modern DeFi protocols.

It allows users to:

* Wrap assets (BTC → kBTC)
* Simulate cross-chain transfers
* Track portfolio balances
* Fetch live crypto prices
* Set and trigger price alerts

---
### NOTE
Frontend was not implemented due to time constraints.
However, all APIs are fully tested via Postman collection.

---

## 🧠 Key Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* User registration & login
* Role-based access (`admin`, `user`)

---

### 💰 Asset & Portfolio Management

* Deposit assets (simulated wrapping)
* Maintain wallet balances
* View portfolio holdings

---

### 🔁 Cross-Chain Transfer Simulation

* Simulate asset transfer between chains (Ethereum, BSC, etc.)
* Deduct balance and record transaction history

---

### 🌐 External API Integration

* Live crypto prices using CoinGecko API
* Retry & timeout handling implemented

---

### 🔔 Alerts System

* Set price alerts (e.g., BTC > 70,000)
* Trigger alerts via API check

---

### 📜 Transactions

* Transaction history with:

  * Pagination
  * Filtering (deposit / transfer)

---

### 🛡️ Logging

* Logs stored in `app.log`
* Tracks:

  * User actions
  * Errors
  * System events

---

## 🧱 Tech Stack

* Backend: Django, Django REST Framework
* Database: PostgreSQL
* Auth: JWT (SimpleJWT)
* External API: CoinGecko
* Testing: Postman

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt not present:

```bash
pip install django djangorestframework psycopg2-binary requests python-dotenv djangorestframework-simplejwt
```

---

## 🐘 PostgreSQL Setup

### Install PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

---

### Start PostgreSQL

```bash
sudo service postgresql start
```

---

### Open PostgreSQL shell

```bash
sudo -u postgres psql
```

---

### Create Database

```sql
CREATE DATABASE crypto_db;
```

---

### Set Password

```sql
ALTER USER postgres PASSWORD 'yourpassword';
```

---

### Exit

```sql
\q
```

---

## ⚙️ Configure Django Database

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crypto_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🔁 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## ▶️ Run Server

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000/
```

---

## 🧪 API Endpoints

Base URL:

```
http://127.0.0.1:8000/api/
```

---

### 🔐 Authentication

| Method | Endpoint          | Description      |
| ------ | ----------------- | ---------------- |
| POST   | `/register/`      | Register user    |
| POST   | `/login/`         | Get JWT token    |
| POST   | `/token/refresh/` | Refresh token    |
| GET    | `/me/`            | Get current user |

---

### 💰 Assets & Portfolio

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| POST   | `/deposit/`   | Deposit asset |
| GET    | `/portfolio/` | View balances |

---

### 🔁 Transfers

| Method | Endpoint     | Description       |
| ------ | ------------ | ----------------- |
| POST   | `/transfer/` | Simulate transfer |

---

### 🌐 Price

| Method | Endpoint            | Description    |
| ------ | ------------------- | -------------- |
| GET    | `/price/?asset=BTC` | Get live price |

---

### 🔔 Alerts

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| POST   | `/alerts/`       | Create alert           |
| GET    | `/alerts/check/` | Check triggered alerts |

---

### 📜 Transactions

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| GET    | `/transactions/` | Transaction history |

Query params:

```
?type=deposit
?page=1
```

---

## 🔑 Authentication Usage

Add header in requests:

```
Authorization: Bearer <your_token>
```

---

## 📦 Postman Collection

* Postman collection included in repository
* Automatically stores JWT token after login
* Covers all endpoints

---

## 🧠 Design Decisions

* Used **Asset model instead of choices** for scalability
* Wallet tracks balances per user & asset
* Transactions store chain info as metadata (simplified simulation)
* External API handled via service layer

---

## 🚧 Future Improvements

* Chain-level wallet tracking (user + asset + chain)
* Background job for alerts (Celery/Redis)
* Caching for price API
* Docker deployment
* Rate limiting

---

## 👨‍💻 Author

Built as part of Backend Developer Internship Assignment.

---