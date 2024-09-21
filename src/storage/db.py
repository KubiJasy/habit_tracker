from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base


# Database connection setup
DATABASE_URL = "sqlite:///habit_tracker.sqlite3"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to initialize the database (create tables)


def init_db():
    Base.metadata.create_all(engine)
