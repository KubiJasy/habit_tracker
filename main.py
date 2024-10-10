from src.db import initialize_db
from src.data_generator.load_data import load_data
from src.cli import HabitTrackerCLI
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

# set up database
initialize_db()

# load sample habit data
load_data() if bool(os.getenv("LOAD_DATA")) else None

# run the cli
cli = HabitTrackerCLI()
cli.run()
