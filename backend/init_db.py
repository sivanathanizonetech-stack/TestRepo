from passlib.context import CryptContext

from app.db.session import SessionLocal, engine
from app.models import AdminUser, Base, Department

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_db():
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if admin user already exists
    admin_user = db.query(AdminUser).filter(AdminUser.username == "admin").first()
    if not admin_user:
        # Create default admin user
        hashed_password = get_password_hash("admin")
        admin = AdminUser(username="admin", hashed_password=hashed_password, role="admin")
        db.add(admin)
        print("Default admin user created: admin / admin")
    
    # Check if departments exist
    if db.query(Department).count() == 0:
        # Create default departments
        departments = [
            {"name": "Revenue Department", "name_ta": "வருவாய் துறை", "description": "Land records, patta and other revenue matters"},
            {"name": "Police Department", "name_ta": "காவல் துறை", "description": "Law and order, safety and security"},
            {"name": "Electricity Board", "name_ta": "மின்சார வாரியம்", "description": "Electricity and power related issues"},
            {"name": "Water Supply", "name_ta": "குடிநீர் வழங்கல்", "description": "Water supply and irrigation related matters"},
            {"name": "Municipal Administration", "name_ta": "நகராட்சி நிர்வாகம்", "description": "Urban governance and services"},
            {"name": "Transport Department", "name_ta": "போக்குவரத்து துறை", "description": "Public and private transport matters"},
            {"name": "Health Department", "name_ta": "சுகாதாரத் துறை", "description": "Hospital services and public health matters"},
            {"name": "Agriculture Department", "name_ta": "வேளாண்மைத் துறை", "description": "Farmer support and agriculture related schemes"},
        ]
        
        for dept in departments:
            db_dept = Department(
                name=dept["name"], 
                name_ta=dept["name_ta"], 
                description=dept["description"]
            )
            db.add(db_dept)
        print(f"{len(departments)} initial departments created.")
    
    db.commit()
    db.close()
    print("Database initialization complete!")

if __name__ == "__main__":
    init_db()
