# Script to create all necessary source files for the project

import os

# Ensure src directory exists
os.makedirs('src', exist_ok=True)

# database.py
database_py = """from sqlalchemy import create_engine, Column, Float, String, Integer
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

    def load_training(self, files):
        dfs = [pd.read_csv(f) for f in files]
        merged = pd.DataFrame({'X': dfs[0]['X']})
        for i, df in enumerate(dfs, 1):
            merged[f'Y{i}'] = df['Y']
        merged.to_sql('training', self.engine, if_exists='replace', index=False)

    def load_ideal(self, file):
        df = pd.read_csv(file)
        df.to_sql('ideal', self.engine, if_exists='replace', index=False)

    def save_results(self, results_df):
        results_df.to_sql('test_results', self.engine, if_exists='replace', index=False)
"""

# fitting.py
fitting_py = """import pandas as pd
import numpy as np
from database import DatabaseManager
import math

class DataLoadError(Exception): pass

class FunctionFitter:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.best_fits = {}

    def select_best_ideals(self):
        train_df = pd.read_sql('training', self.db.engine)
        ideal_df = pd.read_sql('ideal', self.db.engine)

        for i in range(1, 5):
            train_y = train_df[f'Y{i}']
            min_ssd = float('inf')
            best_col = None
            max_dev = 0

            for col in [c for c in ideal_df.columns if c.startswith('Y')]:
                ideal_y = ideal_df[col]
                ssd = np.sum((train_y - ideal_y) ** 2)
                if ssd < min_ssd:
                    min_ssd = ssd
                    best_col = col
                    max_dev = np.max(np.abs(train_y - ideal_y))

            self.best_fits[f'Y{i}'] = {
                'col': best_col,
                'ssd': min_ssd,
                'max_dev': max_dev
            }
        return self.best_fits

    def map_test_data(self, test_file: str):
        test_df = pd.read_csv(test_file)
        ideal_df = pd.read_sql('ideal', self.db.engine)
        results = []

        for _, row in test_df.iterrows():
            x, y = row['X'], row['Y']
            assigned = None
            delta = None

            for train_key, info in self.best_fits.items():
                col = info['col']
                ideal_y = ideal_df.loc[ideal_df['X'] == x, col]
                if ideal_y.empty:
                    continue
                ideal_val = ideal_y.values[0]
                dev = abs(y - ideal_val)
                threshold = info['max_dev'] * math.sqrt(2)
                if dev <= threshold:
                    if assigned is None or dev < delta:
                        assigned = col
                        delta = dev

            results.append({
                'X': x, 'Y': y, 'Delta Y': delta, 'No. of ideal func': assigned
            })

        results_df = pd.DataFrame(results)
        self.db.save_results(results_df)
        return results_df
"""

# visualizer.py
visualizer_py = """from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import HoverTool
import pandas as pd

class Visualizer:
    def __init__(self, db_engine):
        self.engine = db_engine

    def plot_all(self):
        output_file("visualization.html")
        
        train = pd.read_sql('training', self.engine)
        ideal = pd.read_sql('ideal', self.engine)
        test = pd.read_sql('test_results', self.engine)

        p1 = figure(title="Training Data with Best Ideal Functions", 
                   width=800, height=400,
                   x_axis_label='X', y_axis_label='Y')
        
        colors = ['blue', 'red', 'green', 'orange']
        for i in range(1, 5):
            p1.circle(train['X'], train[f'Y{i}'], 
                     legend_label=f'Train Y{i}', 
                     color=colors[i-1], size=5, alpha=0.6)

        p2 = figure(title="Test Points Mapping", 
                   width=800, height=400,
                   x_axis_label='X', y_axis_label='Y')
        
        mapped = test[test['ideal_func'].notna()]
        unmapped = test[test['ideal_func'].isna()]
        
        if not mapped.empty:
            p2.circle(mapped['X'], mapped['Y'], 
                     size=6, color='green', legend_label='Mapped', alpha=0.7)
        
        if not unmapped.empty:
            p2.circle(unmapped['X'], unmapped['Y'], 
                     size=6, color='red', legend_label='Unmapped', alpha=0.7)

        hover1 = HoverTool(tooltips=[("X", "@x"), ("Y", "@y")])
        hover2 = HoverTool(tooltips=[("X", "@x"), ("Y", "@y")])
        p1.add_tools(hover1)
        p2.add_tools(hover2)

        layout = column(p1, p2)
        save(layout)
        print("Visualization saved to visualization.html")
"""

# main.py
main_py = """from database import DatabaseManager
from fitting import FunctionFitter
from visualizer import Visualizer

def main():
    db = DatabaseManager()
    db.load_training([
        'data/train1.csv', 'data/train2.csv',
        'data/train3.csv', 'data/train4.csv'
    ])
    db.load_ideal('data/ideal_functions.csv')

    fitter = FunctionFitter(db)
    best = fitter.select_best_ideals()
    print("Best fits:", best)

    results = fitter.map_test_data('data/test.csv')
    print(f"Mapped {results['No. of ideal func'].notna().sum()} test points")

    viz = Visualizer(db.engine)
    viz.plot_all()

if __name__ == "__main__":
    main()
"""

# Write files
files = {
    'src/database.py': database_py,
    'src/fitting.py': fitting_py,
    'src/visualizer.py': visualizer_py,
    'src/main.py': main_py
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filepath}")

print("\nAll source files created successfully!")
