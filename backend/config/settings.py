import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
SKILL_STORAGE_PATH = os.getenv('SKILL_STORAGE_PATH', 'data/skills')

# Swarm settings
MAX_AGENTS = 10

# Task settings
MAX_TASKS_PER_AGENT = 5
TASK_TIMEOUT_SECONDS = 300

# Communication settings
COMMUNICATION_INTERVAL_SECONDS = 5

# Database settings (for future implementation)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///swarm_ai.db')

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/swarm_ai.log'

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'