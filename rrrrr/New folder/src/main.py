from database import DatabaseManager
from fitting import FunctionFitter
from visualizer import Visualizer

def main():
    db = DatabaseManager()
    
    # Load training data (single file with multiple Y columns)
    db.load_training('data/train.csv')
    
    # Load ideal functions
    db.load_ideal('data/ideal.csv')

    # Find best fitting ideal functions
    fitter = FunctionFitter(db)
    best = fitter.select_best_ideals()
    print("\n=== Best Fitting Ideal Functions ===")
    for train_col, info in best.items():
        print(f"{train_col} -> {info['col']} (SSD: {info['ssd']:.6f}, Max Dev: {info['max_dev']:.6f})")

    # Map test data to ideal functions
    results = fitter.map_test_data('data/test.csv')
    mapped_count = results['No. of ideal func'].notna().sum()
    print(f"\n=== Test Data Mapping ===")
    print(f"Total test points: {len(results)}")
    print(f"Mapped points: {mapped_count}")
    print(f"Unmapped points: {len(results) - mapped_count}")

    # Generate visualization
    viz = Visualizer(db.engine)
    viz.plot_all()
    print("\n=== Visualization ===")
    print("Saved to visualization.html")

if __name__ == "__main__":
    main()
