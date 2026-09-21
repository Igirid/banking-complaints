from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

# default SQLite engine for development
engine = create_engine('sqlite:///banking_complaints.db', future=True)

from .User import User  # keep existing model import
from .legacy_models import ComplaintIssue, SocialPost, AlertRecord
