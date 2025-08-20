# Flask E-Commerce Web Application

A functional E-Commerce web application built using **Flask**, **Bootstrap**, and **SQLAlchemy**, allowing users to browse products, register/login, add items to cart, and manage their profile.

## Features

- **User Authentication:** Sign up, login, logout with secure password hashing.
- **Admin Panel:** Admin can add, update, or delete products.
- **Product Management:** View all products with details, images, and pricing.
- **Shopping Cart:** Add products to cart and manage cart items.
- **Profile Management:** Users can upload profile pictures and view their information.
- **Responsive Design:** Built with **Bootstrap 5** for mobile-friendly UI.
- **Flask-WTF Forms:** Secure form handling and validation.

## Project Structure

```
flask_ecommerce/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── products.html
│   │   ├── profile.html
│   │   └── ...
│   └── static/
│       ├── css/
│       └── uploads/
│
├── venv/
├── config.py
├── requirements.txt
└── run.py
```

## Installation

1. **Clone the repository**

```bash
git clone git@github.com:vishnu-R2005/Flask_E-Commerce_web.git
cd Flask_E-Commerce_web
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the application**

```bash
python run.py
```

The app will run at `http://127.0.0.1:5000/`.

## Technologies Used

- **Backend:** Flask, Flask-WTF, Flask-Login, SQLAlchemy
- **Frontend:** Bootstrap 5, HTML5, CSS3, Jinja2 templates
- **Database:** SQLite (default) or can be configured for MySQL/PostgreSQL
- **Others:** Werkzeug for password hashing, Flask-Migrate for database migrations

## Usage

- Admin can log in with special credentials and manage products.
- Users can sign up, log in, browse products, add them to cart, and manage their profile.

## License

This project is licensed under the MIT License.

