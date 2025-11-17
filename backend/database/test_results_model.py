# backend/database/test_results_model.py

"""
Database model for storing paper trading test results.
This schema defines the structure for the 'test_results' table.
"""

from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        DateTime, Boolean, Text, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class TestResult(Base):
    """
    Represents the outcome of a single paper trade simulation
    conducted by a Tester Agent.
    """
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, ForeignKey('research_strategies.id'), nullable=False)
    test_id = Column(String(255), nullable=False, unique=True)
    instrument = Column(String(50), nullable=False)
    entry_time = Column(DateTime(timezone=True), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=False)
    pnl = Column(Float, nullable=False)
    win_flag = Column(Boolean, nullable=False)
    notes = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TestResult(test_id='{self.test_id}', pnl='{self.pnl}')>"

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
#     print("Initializing database and creating 'test_results' table...")
#     init_db()
#     print("Table created.")
