from werkzeug.security import generate_password_hash
from models import db, User
from app import app

def create_users():
    users = [
        {'username': 'abc', 'password': '123'},
        {'username': 'admin', 'password': 'admin'},
    ]
    
    with app.app_context():
        for user_data in users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                hashed_password = generate_password_hash(user_data['password'])
                new_user = User(username=user_data['username'], password=hashed_password)
                db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    create_users()