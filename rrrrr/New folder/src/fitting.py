import pandas as pd
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

        # Get the number of training columns dynamically
        train_cols = [col for col in train_df.columns if col.startswith('Y')]
        
        for col_name in train_cols:
            train_y = train_df[col_name]
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

            self.best_fits[col_name] = {
                'col': best_col,
                'ssd': min_ssd,
                'max_dev': max_dev
            }
        return self.best_fits

    def map_test_data(self, test_file: str):
        test_df = pd.read_csv(test_file)
        # Standardize column names to uppercase
        test_df.columns = test_df.columns.str.upper()
        
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
