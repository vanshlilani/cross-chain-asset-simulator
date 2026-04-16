# 🚀 Cross-Chain Asset Simulator + Alerts System

## 📌 Overview

This project is a **backend-focused REST API system** that simulates a cross-chain asset platform inspired by modern DeFi protocols.

It allows users to:

* Wrap assets (BTC → kBTC)
* Enable cross-chain transfers
* Track portfolio balances
* **Fetch live crypto prices**
* **Set and trigger price alerts**

---
### Note

Frontend was not implemented due to time constraints.
However, all APIs are fully tested via Postman collection.
---

## Backend is Live Hosted on - https://cross-chain-asset-simulator.onrender.com
---

##  Key Features

### 1. Authentication & Authorization

* JWT-based authentication
* User registration & login
* Role-based access (`admin`, `user`)

---

### 2. Asset & Portfolio Management

* Deposit assets (simulated wrapping)
* Maintain wallet balances
* View portfolio holdings

---

### 3. Cross-Chain Transfer Simulation

* Simulate asset transfer between chains (Ethereum, BSC, etc.)
* Deduct balance and record transaction history

---

### 4. External API Integration

* Live crypto prices using CoinGecko API
* Retry & timeout handling implemented

---

### 5. Alerts System

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
git clone https://github.com/vanshlilani/cross-chain-asset-simulator
cd cross-chain-asset-simulator
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
cd core/
pip install -r requirements.txt
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

## 📦 Postman Collection

The Postman collection included in repositoryas a JSON format and automatically stores JWT token after login covering all endpoints

---