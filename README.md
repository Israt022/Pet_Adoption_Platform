# 🐾 PetBond BD - Pet Adoption Platform

**PetBond BD** is a full-featured pet adoption platform built with Django and Django REST Framework (DRF). The platform supports both Admins and Customers, providing functionality to add pets, adopt pets, deposit funds, view adoption history, and leave reviews.

---

## 🚀 Features

### 1. User Registration and Authentication
- Two roles: **Admin** and **Customer**.
- Registration, login, logout with JWT authentication.
- Email verification is required to activate user accounts.

### 2. Add and Manage Pets
- Admin and customers can add pets.
- Admin can update and delete pet listings.
- Pet model includes: `name`, `category`, `breed`, `age`, `description`, `availability` (public/private).

### 3. Customer Profile
- Customers can view profile details.
- Profile includes: username, account balance, and adoption history.
- Password change functionality.

### 4. Filter and Deposit
- Filter pets by category (e.g., dog, cat, bird).
- Customers can deposit money for future adoptions.

### 5. Pet Adoption
- Customers can adopt pets if they have enough balance.
- Adopted pets are linked to the customer profile.

### 6. Pet Reviews
- Customers can review pets they've adopted.
- Reviews are publicly visible per pet.

### 7. Deployment
- Fully deployable Django application with Swagger documentation.

---

## 🛠 Technologies Used

- **Django** - Web framework
- **Django REST Framework** - API development
- **JWT Authentication** - User auth system
- **Swagger (drf_yasg)** - API documentation
- **PostgreSQL / SQLite** - Database

---

## ⚙️ Installation Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/petbondbd.git
cd petbondbd
```

2. **Create and activate virtual environment:**
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create a superuser:**
```bash
python manage.py createsuperuser
```

6. **Run the server:**
```bash
python manage.py runserver
```

---

## 📄 API Documentation

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

---

## 🔐 Environment Variables

Create a `.env` file with the following keys:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
EMAIL_HOST=your_email_host
```

---

## 💡 Future Enhancements

- Integrate payment gateway for real-time transactions.
- Track payment/adoption transaction history.
- Add push notifications for adoption status and updates.

---

## 🧑‍💻 Author
[Your Name](https://github.com/yourusername)

---

## 📄 License
This project is licensed under the MIT License.

