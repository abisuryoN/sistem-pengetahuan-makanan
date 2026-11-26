import bcrypt
from database.connection import SessionLocal
from database.models import Admin

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def init_admin():
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not admin:
            new_admin = Admin(username="admin", password=hash_password("admin123"))
            db.add(new_admin)
            db.commit()
    finally:
        db.close()

def authenticate_user(username: str, password: str):
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == username).first()
        if admin and check_password(password, admin.password):
            return admin
        return None
    finally:
        db.close()

import bcrypt
from database.connection import SessionLocal
from database.models import Admin

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def init_admin():
    db = SessionLocal()
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin:
        new_admin = Admin(username="admin", password=hash_password("admin123"))
        db.add(new_admin)
        db.commit()
    db.close()

