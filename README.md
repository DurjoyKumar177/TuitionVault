# TuitionsVault Backend

TuitionsVault is a **Django Rest Framework (DRF) backend** that powers the TuitionsVault web application, designed to help students, graduates, and teachers find tuition opportunities in an organized and secure manner. This backend provides a robust API for user authentication, tuition posts, applications, and reviews.

---

## 🚀 Features
- **User Authentication & Management** (Registration, Login, Logout, Profile, Password Reset)
- **Tuition Posts Management** (Listing, Filtering, Searching, Applying)
- **Applications Tracking** (View Applications, Approved Tuitions, History)
- **Review System** (Submit and View Reviews)

---

## 🛠️ Technologies Used
- **Django Rest Framework (DRF)**
- **PostgreSQL / SQLite**
- **JWT Authentication**
- **Django ORM**

---

## 📂 Project Setup

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/DurjoyKumar177/TuitionVault
 cd TuitionVault
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 5️⃣ Create Superuser (For Admin Panel)
```bash
python manage.py createsuperuser
```

### 6️⃣ Run Development Server
```bash
python manage.py runserver
```
Access the API at: **http://127.0.0.1:8000/**

---

## 📬 API Endpoints

### 🔐 Authentication (Accounts)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/accounts/register/` | Register a new user |
| POST   | `/accounts/login/` | Authenticate user |
| POST   | `/accounts/logout/` | Logout user |
| GET    | `/accounts/profile/` | Get user profile |
| PATCH  | `/accounts/profile/update/` | Update user profile |
| POST   | `/accounts/change-password/` | Change password |
| POST   | `/accounts/forgot-password/` | Request password reset |
| POST   | `/accounts/reset-password/<uid>/<token>/` | Reset password |
| GET    | `/accounts/verify/<uid>/<token>/` | Verify account activation |

### 📌 Tuition Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/tutions/posts/` | Retrieve all tuition posts |
| GET    | `/tutions/posts_details/<int:pk>/` | Get details of a specific tuition post |
| GET    | `/tutions/filter_by_class/` | Filter tuition posts by class |
| GET    | `/tutions/filter_by_location/` | Filter tuition posts by location |
| GET    | `/tutions/filter_by_payment/` | Filter tuition posts by payment |
| GET    | `/tutions/search_by_title/` | Search tuition posts by title |
| GET    | `/tutions/dropdown_options/<str:field>/` | Get dropdown options for filters |
| POST   | `/tutions/apply/<int:tuition_post_id>/` | Apply for a tuition |

### 📩 Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/applications/my-applications/` | Get user's pending applications |
| GET    | `/applications/my-approved-tuitions/` | Get user's approved tuitions |
| GET    | `/applications/history/` | Get user's application history |

### ⭐ Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/reviews/give-review/<int:tuition_post_id>/` | Submit a review for a tuition |
| GET    | `/reviews/view-reviews/<int:tuition_post_id>/` | View reviews for a tuition |

---

## 🎯 Contributing
Contributions are welcome! If you'd like to improve the project, please:
1. **Fork** the repository.
2. **Create a new branch** for your feature.
3. **Submit a pull request** with a detailed explanation.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 📞 Contact
For inquiries or support, feel free to reach out via the **Contact Us** page in the application.

---

🚀 **TuitionsVault Backend – Powering Secure & Efficient Tuition Matching!**

