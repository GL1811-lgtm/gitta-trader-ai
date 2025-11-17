# backend/database/research_strategies_model.py

"""
Database model for storing researched trading strategies.
This schema defines the structure for the 'research_strategies' table.
"""

# Using SQLAlchemy as an example for the ORM
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ResearchStrategy(Base):
    """
    Represents a trading strategy found by a Collector Agent.
    """
    __tablename__ = 'research_strategies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_name = Column(String(255), nullable=False)
    entry_rules = Column(Text, nullable=False)
    exit_rules = Column(Text, nullable=False)
    indicators = Column(String(255))
    timeframe = Column(String(50))
    risk_reward = Column(String(50))
    example = Column(Text)
    source_url = Column(String(512), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ResearchStrategy(name='{self.strategy_name}', source='{self.source_url}')>"

# --- Example of how to set up the database engine ---
# This part would typically be in a central database configuration file.

# DATABASE_URL = "sqlite:///./gitta_trader.db" # Example using SQLite
# engine = create_engine(DATABASE_URL)

# def init_db():
#     """
#     Creates the database table.
#     """
#     Base.metadata.create_all(bind=engine)

# if __name__ == '__main__':
#     # This allows creating the table directly for setup.
#     print("Initializing database and creating 'research_strategies' table...")
#     init_db()
#     print("Table created.")
