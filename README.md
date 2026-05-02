# 🚀 SkillBridge Attendance Management API

A role-based attendance management backend system built using FastAPI.  
Supports multiple user roles with strict RBAC and a secure dual-token system for monitoring access.

---

## 🌐 Live API

https://project0105.onrender.com  


---

## 📌 Features

- Role-Based Access Control (RBAC)
- JWT Authentication (24-hour expiry)
- Monitoring Officer dual-token security (1-hour scoped token)
- Batch & session management
- Attendance marking and tracking
- Summary endpoints for institutions and programme managers
- Fully tested with pytest

---

## ⚙️ Local Setup

```bash
git clone https://github.com/jayeshpatil11/Project0105.git 
cd Project0105

pip install -r requirements.txt

uvicorn src.main:app --reload
