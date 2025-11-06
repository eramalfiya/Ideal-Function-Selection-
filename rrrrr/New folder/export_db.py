"""
Export Database Tables to Excel/CSV
"""
import pandas as pd
import sqlite3

print("Exporting database tables...")

conn = sqlite3.connect('assignment.db')

# Export training data
training = pd.read_sql("SELECT * FROM training", conn)
training.to_csv('export_training.csv', index=False)
print(f"✓ Exported training data: export_training.csv ({len(training)} rows)")

# Export ideal functions
ideal = pd.read_sql("SELECT * FROM ideal", conn)
ideal.to_csv('export_ideal.csv', index=False)
print(f"✓ Exported ideal functions: export_ideal.csv ({len(ideal)} rows)")

# Export test results
test = pd.read_sql("SELECT * FROM test_results", conn)
test.to_csv('export_test_results.csv', index=False)
print(f"✓ Exported test results: export_test_results.csv ({len(test)} rows)")

# Export mapped points only
mapped = pd.read_sql("SELECT * FROM test_results WHERE [No. of ideal func] IS NOT NULL", conn)
mapped.to_csv('export_mapped_points.csv', index=False)
print(f"✓ Exported mapped points: export_mapped_points.csv ({len(mapped)} rows)")

# Export summary
summary = pd.read_sql("""
    SELECT 
        [No. of ideal func] as Ideal_Function,
        COUNT(*) as Mapped_Points,
        ROUND(AVG([Delta Y]), 4) as Avg_Deviation,
        ROUND(MAX([Delta Y]), 4) as Max_Deviation,
        ROUND(MIN([Delta Y]), 4) as Min_Deviation
    FROM test_results 
    WHERE [No. of ideal func] IS NOT NULL 
    GROUP BY [No. of ideal func]
    ORDER BY Mapped_Points DESC
""", conn)
summary.to_csv('export_summary.csv', index=False)
print(f"✓ Exported summary statistics: export_summary.csv")

# Try to create Excel file if openpyxl is available
try:
    with pd.ExcelWriter('assignment_results.xlsx', engine='openpyxl') as writer:
        training.to_excel(writer, sheet_name='Training', index=False)
        ideal.to_excel(writer, sheet_name='Ideal Functions', index=False)
        test.to_excel(writer, sheet_name='Test Results', index=False)
        mapped.to_excel(writer, sheet_name='Mapped Points', index=False)
        summary.to_excel(writer, sheet_name='Summary', index=False)
    print(f"\n✓ Created Excel workbook: assignment_results.xlsx")
except ImportError:
    print("\n⚠ Excel export skipped (install openpyxl: pip install openpyxl)")

conn.close()
print("\n✅ Export complete! You can now open these files in Excel or any spreadsheet app.")
