import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager
from fitting import FunctionFitter


class TestDatabaseManager:
    '''Test DatabaseManager functionality'''
    
    def test_database_creation(self):
        '''Test that database and tables are created'''
        db = DatabaseManager('sqlite:///:memory:')
        assert db.engine is not None
        assert db.Session is not None


class TestFunctionFitter:
    '''Test FunctionFitter functionality'''
    
    def test_select_best_ideals(self):
        '''Test selection of best fitting ideal functions'''
        db = DatabaseManager('sqlite:///:memory:')
        
        train = pd.DataFrame({
            'X': [1.0, 2.0, 3.0, 4.0],
            'Y1': [1.0, 2.0, 3.0, 4.0]
        })
        
        ideal = pd.DataFrame({
            'X': [1.0, 2.0, 3.0, 4.0],
            'Y1': [1.0, 2.0, 3.0, 4.0],
            'Y2': [10.0, 20.0, 30.0, 40.0]
        })
        
        train.to_sql('training', db.engine, if_exists='replace', index=False)
        ideal.to_sql('ideal', db.engine, if_exists='replace', index=False)
        
        fitter = FunctionFitter(db)
        best = fitter.select_best_ideals()
        
        assert best['Y1']['col'] == 'Y1'
        assert best['Y1']['ssd'] < 0.01
    
    def test_map_test_data(self):
        '''Test mapping test data to ideal functions'''
        db = DatabaseManager('sqlite:///:memory:')
        
        train = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y1': [1.0, 2.0, 3.0]
        })
        
        ideal = pd.DataFrame({
            'X': [1.0, 2.0, 3.0],
            'Y1': [1.0, 2.0, 3.0]
        })
        
        train.to_sql('training', db.engine, if_exists='replace', index=False)
        ideal.to_sql('ideal', db.engine, if_exists='replace', index=False)
        
        test_data = pd.DataFrame({
            'X': [1.0, 2.0],
            'Y': [1.0, 2.0]  # Exact match with ideal
        })
        test_data.to_csv('temp_test.csv', index=False)
        
        try:
            fitter = FunctionFitter(db)
            fitter.select_best_ideals()
            results = fitter.map_test_data('temp_test.csv')
            
            assert len(results) == 2
            assert 'No. of ideal func' in results.columns
            mapped_count = results['No. of ideal func'].notna().sum()
            assert mapped_count > 0
        finally:
            if os.path.exists('temp_test.csv'):
                os.remove('temp_test.csv')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
