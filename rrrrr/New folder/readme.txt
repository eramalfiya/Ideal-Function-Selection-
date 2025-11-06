# 1. Navigate to project directory
cd "where you download this project"

# 2. Install dependencies
python -m pip install pandas sqlalchemy bokeh numpy pytest

# 3. Run main analysis
python src/main.py

# 4. Run tests
pytest -v

# 5. View database results
python view_db.py

# 6. Open visualization
start visualization.html