from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email="admin@example.com").first()
        if admin:
            print("Admin already exists!")
        else:
            admin = User(
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("admin123"),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")

if __name__ == "__main__":
    create_admin()
