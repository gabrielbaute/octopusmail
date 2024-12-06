from .models import Role, User
from .db import session
from werkzeug.security import generate_password_hash

def create_initial_roles():
    roles=['Admin', 'User']
    for role_name in roles:
        role=session.query(Role).filter_by(name=role_name).first()
        if not role:
            new_role=Role(name=role_name)
            session.add(new_role)
    session.commit()

def create_initial_admin():
    admin_role=session.query(Role).filter_by(name='Admin').first()
    if not admin_role:
        print("Error: Admin role not found. Ensure roles are initialized first.")
        return

    admin_user=session.query(User).filter_by(username='admin').first()
    if not admin_user:
        new_admin=User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('adminpassword'),
            role_id=admin_role.id
        )
        session.add(new_admin)
        session.commit()
        print("Admin user created.")
