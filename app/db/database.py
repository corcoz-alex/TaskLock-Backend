from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Initialize the SQLAlchemy engine with our secure URL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # Verifies connections are alive before using them
    pool_size=5,        # Standard pool size for an MVP
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to be injected into our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()