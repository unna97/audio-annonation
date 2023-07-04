import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'waveform_audio')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
