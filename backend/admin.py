import sys

from passlib.context import CryptContext

from app.db.session import SessionLocal, engine
from app.models import AdminUser, Base

# Hash setup (matching routes/auth.py)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin(username, password):
    db = SessionLocal()
    try:
        # Check if user exists
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        hashed_password = pwd_context.hash(password)
        
        if user:
            print(f"Updating existing admin: {username}")
            user.hashed_password = hashed_password
        else:
            print(f"Creating new admin: {username}")
            user = AdminUser(
                username=username,
                hashed_password=hashed_password,
                role="admin"
            )
            db.add(user)
        
        db.commit()
        print("Admin user saved successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    if len(sys.argv) >= 3:
        user = sys.argv[1]
        pw = sys.argv[2]
        create_admin(user, pw)
    else:
        # Default for first setup
        print("Usage: python admin.py <username> <password>")
        print("Running default setup: admin / admin")
        create_admin("admin", "admin")
