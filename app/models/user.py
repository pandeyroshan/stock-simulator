from attr import dataclass
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session

from app.db.connection import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def create_user(db: Session, username: str, balance: float):
    """
    Create a new user to the database
    """
    try:
        new_user = User(username=username, balance=balance)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f'Created new user: {new_user}')
        return new_user
    except Exception as e:
        print(e)
        db.rollback()
        raise e

def get_user(db: Session, username: str):
    """
    Get a user by username from the database
    """
    return db.query(User).filter(User.username == username).first()

# Get User by ID
def get_user_by_id(db: Session, user_id: int):
    """
    Get a user by user_id from the database
    """
    return db.query(User).filter(User.user_id == user_id).first()

def update_user_balance(db: Session, username: str, new_balance: float) -> User:
    user = get_user(db, username)
    if user:
        user.balance = new_balance
        db.commit()
        db.refresh(user)
        return user
    return None
