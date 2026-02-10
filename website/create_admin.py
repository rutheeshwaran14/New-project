# website/create_admin.py

from website.database import SessionLocal
from website.models.user import User
from website.auth import hash_password

def create_admin():
    db = SessionLocal()
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        print(f"Admin already exists: {existing_admin.username} ({existing_admin.email})")
        db.close()
        return

    # Create new admin
    admin_user = User(
        username="rutheesh",           # change username as needed
        email="rutheesh@gmail.com",       # change email as needed
        password=hash_password("rutheesh"),  # strong password
        role="admin"
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    db.close()
    print(f"Admin created successfully! Username: {admin_user.username}, Email: {admin_user.email}")

if __name__ == "__main__":
    create_admin()
