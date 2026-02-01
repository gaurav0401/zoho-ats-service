## 🚀 Zoho Recruit ATS Integration Microservice
### Python • Serverless Framework • AWS Lambda • serverless-offline

---

### 📌 Overview
This project is a backend microservice that integrates with **Zoho Recruit (ATS)**  
and exposes a unified REST API for jobs, candidates, and applications.

Built as part of an ATS Integration assignment using:
- Python
- Serverless Framework
- AWS Lambda (local via serverless-offline)

---

### 🧩 Features
- OAuth2 authentication (Refresh Token based)
- Zoho Recruit API v2 integration
- Serverless & stateless architecture
- Local development using serverless-offline
- Defensive error handling for ATS quirks
- Standardized JSON responses

---

### 🔗 API Endpoints

    GET /jobs
    POST /candidates
    GET /applications?job_id=<JOB_ID>

---

### 📦 Tech Stack
- Python 3.9+
- AWS Lambda
- Serverless Framework
- Zoho Recruit API v2
- serverless-offline

---

### ⚙️ Prerequisites
```bash
# Node.js (v16+)
# https://nodejs.org/

# Python (v3.9+)
# https://www.python.org/
```
### Project Setup 

    npm install -g serverless
    cd zoho-ats-integration
    pip install -r requirements.txt
    
