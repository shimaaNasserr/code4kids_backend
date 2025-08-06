# 🧠 Code4Kids - Backend

A user registration and login system built with **Django REST Framework** and **JWT Authentication**.  
Users can register as either **"Kid"** or **"Parent"**, and access role-specific endpoints.

---

## 📌 Features

✅ User Registration with:
- Username  
- Email  
- Password + Password Confirmation  
- Egyptian Phone Number  
- Role (`Kid` or `Parent`)  

✅ User Login using **email** and **password**

✅ Full **Data Validation** for all fields

✅ **JWT Token Generation** (access & refresh) on login

✅ **Role-Based Access Control**:
- `Parent`-only view (Parent Dashboard)  
- `Kid`-only view (Kid Zone)

---

## 🛠️ Tech Stack

- Python 3  
- Django  
- Django REST Framework  
- Simple JWT  
- PostgreSQL or SQLite

---

## 🚀 Installation Guide

```bash
# Clone the repository
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate
| Method | Endpoint             | Description           |
| ------ | -------------------- | --------------------- |
| POST   | `/register/`         | Register a new user   |
| POST   | `/login/`            | Login and get tokens  |
| GET    | `/parent-only/` | Accessible by Parents |
| GET    | `/kid-only/`    | Accessible by Kids    |
| GET    | `/admin-only/`    | Accessible by Admin    |
| GET    | `/profile/`    | user profile   |




# Start the development server
python manage.py runserver
