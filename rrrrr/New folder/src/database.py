from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from typing import List

Base = declarative_base()

class TrainingData(Base):
    __tablename__ = 'training'
    X = Column(Float, primary_key=True)
    Y1 = Column(Float)
    Y2 = Column(Float)
    Y3 = Column(Float)
    Y4 = Column(Float)

class IdealFunction(Base):
    __tablename__ = 'ideal'
    X = Column(Float, primary_key=True)

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    X = Column(Float)
    Y = Column(Float)
    delta_y = Column(Float)
    ideal_func = Column(String(10))

class DatabaseManager:
    def __init__(self, db_path='sqlite:///assignment.db'):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def load_training(self, file):
        """Load training data from a single CSV file with multiple Y columns"""
        df = pd.read_csv(file)
        # Standardize column names to uppercase
        df.columns = df.columns.str.upper()
        df.to_sql('training', self.engine, if_exists='replace', index=False)

    def load_ideal(self, file):
        """Load ideal functions from CSV file"""
        df = pd.read_csv(file)
        # Standardize column names to uppercase
        df.columns = df.columns.str.upper()
        df.to_sql('ideal', self.engine, if_exists='replace', index=False)

    def save_results(self, results_df):
        results_df.to_sql('test_results', self.engine, if_exists='replace', index=False)
