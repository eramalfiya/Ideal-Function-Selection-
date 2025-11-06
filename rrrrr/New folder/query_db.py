"""
Interactive Database Query Tool
Run this script to query the assignment.db interactively
"""
import pandas as pd
import sqlite3

def query_db(query):
    """Execute a SQL query and display results"""
    conn = sqlite3.connect('assignment.db')
    try:
        result = pd.read_sql(query, conn)
        print(result)
        print(f"\nRows returned: {len(result)}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def show_menu():
    print("\n" + "="*70)
    print("ASSIGNMENT.DB - INTERACTIVE QUERY TOOL")
    print("="*70)
    print("\nPre-defined Queries:")
    print("1. Show all training data")
    print("2. Show all ideal functions (first 10 columns)")
    print("3. Show all test results")
    print("4. Show only mapped test points")
    print("5. Show only unmapped test points")
    print("6. Show mapping statistics")
    print("7. Show best fit mappings (Y1→Y42, Y2→Y41, Y3→Y11, Y4→Y48)")
    print("8. Custom SQL query")
    print("0. Exit")
    print("="*70)

def main():
    queries = {
        '1': "SELECT * FROM training",
        '2': "SELECT X, Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, Y10 FROM ideal",
        '3': "SELECT * FROM test_results",
        '4': "SELECT * FROM test_results WHERE [No. of ideal func] IS NOT NULL",
        '5': "SELECT * FROM test_results WHERE [No. of ideal func] IS NULL",
        '6': """
            SELECT 
                [No. of ideal func], 
                COUNT(*) as count,
                ROUND(AVG([Delta Y]), 4) as avg_deviation,
                ROUND(MAX([Delta Y]), 4) as max_deviation
            FROM test_results 
            WHERE [No. of ideal func] IS NOT NULL 
            GROUP BY [No. of ideal func]
            ORDER BY count DESC
        """,
        '7': """
            SELECT 
                'Y1 → Y42' as mapping, COUNT(*) as points 
            FROM test_results WHERE [No. of ideal func] = 'Y42'
            UNION ALL
            SELECT 
                'Y2 → Y41' as mapping, COUNT(*) as points 
            FROM test_results WHERE [No. of ideal func] = 'Y41'
            UNION ALL
            SELECT 
                'Y3 → Y11' as mapping, COUNT(*) as points 
            FROM test_results WHERE [No. of ideal func] = 'Y11'
            UNION ALL
            SELECT 
                'Y4 → Y48' as mapping, COUNT(*) as points 
            FROM test_results WHERE [No. of ideal func] = 'Y48'
        """
    }
    
    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '0':
            print("\nGoodbye!")
            break
        elif choice == '8':
            print("\nEnter your SQL query (press Enter twice to execute):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            custom_query = " ".join(lines)
            if custom_query:
                query_db(custom_query)
        elif choice in queries:
            print(f"\nExecuting query {choice}...")
            query_db(queries[choice])
        else:
            print("\nInvalid choice! Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
