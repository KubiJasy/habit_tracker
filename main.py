from src.db import initialize_db
from src.data_generator.load_data import load_data
from src.cli import HabitTrackerCLI
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

# set up database
initialize_db()

# print(type(os.getenv("LOAD_DATA")))

# load sample habit data
load_data() if os.getenv("LOAD_DATA") == "True" else None

# run the cli
cli = HabitTrackerCLI()
cli.run()
