from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


DATABASE_URL = "sqlite:///habit_tracker.sqlite3"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def initialize_db():
    """
    Initialize the database schema.
    This method should handle creating all necessary tables and setting up the schema.
    """
    Base.metadata.create_all(engine)


class StorageComponent:
    """
    Storage component responsible for managing database interactions.
    """
    def __init__(self):
        self.engine = engine
        self.session = session

    def load_habits(self):
        """
        Load habits from the database.
        This method will query the database and return all habit records.
        """
        # TODO: Add code to load habits from the database
        pass

    def load_tasks(self):
        """
        Load tasks from the database.
        This method will query the database and return all task records.
        """
        # TODO: Add code to load tasks from the database
        pass

    def save_habit(self, habit):
        """
        Save a habit to the database.
        :param habit: The habit object to be saved.
        """
        # TODO: Add code to save a habit to the database
        pass

    def save_task(self, task):
        """
        Save a task to the database.
        :param task: The task object to be saved.
        """
        # TODO: Add code to save a task to the database
        pass
