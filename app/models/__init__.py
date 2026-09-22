from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

# SQLAlchemy base must be defined before importing models that use it
Base = declarative_base()

# default SQLite engine for development
engine = create_engine('sqlite:///banking_complaints.db', future=True)

# Note: avoid importing model classes here to prevent circular imports.
# Import model classes directly from their modules when needed, e.g.:
# from app.models.legacy_models import ComplaintIssue
