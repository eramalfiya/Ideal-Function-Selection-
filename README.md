Course:Programming with Python 
Program:MSc Computer Science – On Campus
Author:Alfiya Eram 

Overview

This project identifies the most suitable **ideal functions** for training data using the **Least Squares Deviation (LSD)** method, then maps **test data** to these functions based on a deviation threshold.



Tools & Libraries

Python 3.12 | NumPy | Pandas | SQLAlchemy | SQLite | Bokeh | Pytest



 Main Files

| File              | Description                         |
| ----------------- | ----------------------------------- |
| `Main.py`         | Runs full analysis workflow         |
| `Fitting.py`      | Calculates least-squares deviations |
| `Database.py`     | Creates and manages SQLite database |
| `Visualizer.py`   | Generates interactive plots         |
| `Test_fitting.py` | Unit tests using Pytest             |



 Method

1. Load `train.csv`, `ideal.csv`, and `test.csv`.
2. Find best-fit ideal functions via minimum SSD.
3. Map test data using threshold = √2 × (max training deviation).
4. Save results to `assignment.db` and visualize in Bokeh.



Results
Best fit: **Y3 → Y11**
Avg SSD: 32.9 | Max Deviation: 0.5
Mapped test points: ≈48%



How to Run

```bash
pip install pandas numpy sqlalchemy bokeh pytest
python Main.py
pytest -v
```

Open generated HTML plots for results.

Notes

Follow APA 7 citation format (see report).
Attach signed anti-plagiarism declaration.
Submit via Turnitin.


Would you like me to format this as a **README.md** file for you to include in your submission zip?
