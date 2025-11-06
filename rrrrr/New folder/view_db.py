import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('assignment.db')

print("="*70)
print("DATABASE TABLES")
print("="*70)
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(tables.to_string(index=False))

print("\n" + "="*70)
print("TRAINING DATA (First 10 rows)")
print("="*70)
training = pd.read_sql("SELECT * FROM training LIMIT 10", conn)
print(training.to_string(index=False))
print(f"\nTotal rows: {pd.read_sql('SELECT COUNT(*) as count FROM training', conn)['count'][0]}")

print("\n" + "="*70)
print("IDEAL FUNCTIONS (First 5 rows, first 10 columns)")
print("="*70)
ideal = pd.read_sql("SELECT * FROM ideal LIMIT 5", conn)
print(ideal.iloc[:, :10].to_string(index=False))
print(f"\nTotal rows: {pd.read_sql('SELECT COUNT(*) as count FROM ideal', conn)['count'][0]}")
print(f"Total columns: {len(ideal.columns)}")

print("\n" + "="*70)
print("TEST RESULTS - Mapped Points (First 15)")
print("="*70)
test_mapped = pd.read_sql("SELECT * FROM test_results WHERE [No. of ideal func] IS NOT NULL LIMIT 15", conn)
print(test_mapped.to_string(index=False))

print("\n" + "="*70)
print("TEST RESULTS - Unmapped Points (First 10)")
print("="*70)
test_unmapped = pd.read_sql("SELECT * FROM test_results WHERE [No. of ideal func] IS NULL LIMIT 10", conn)
print(test_unmapped.to_string(index=False))

print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
total = pd.read_sql("SELECT COUNT(*) as count FROM test_results", conn)['count'][0]
mapped = pd.read_sql("SELECT COUNT(*) as count FROM test_results WHERE [No. of ideal func] IS NOT NULL", conn)['count'][0]
unmapped = total - mapped

print(f"Total test points: {total}")
print(f"Mapped points: {mapped} ({mapped/total*100:.1f}%)")
print(f"Unmapped points: {unmapped} ({unmapped/total*100:.1f}%)")

print("\n" + "="*70)
print("MAPPING DISTRIBUTION BY IDEAL FUNCTION")
print("="*70)
distribution = pd.read_sql("""
    SELECT [No. of ideal func], COUNT(*) as count 
    FROM test_results 
    WHERE [No. of ideal func] IS NOT NULL 
    GROUP BY [No. of ideal func]
    ORDER BY count DESC
""", conn)
print(distribution.to_string(index=False))

conn.close()
print("\n" + "="*70)
print("View complete! Use 'python view_db.py' to run this again.")
print("="*70)
