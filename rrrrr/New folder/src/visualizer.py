from bokeh.plotting import figure, output_file, save
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
        
        mapped = test[test['No. of ideal func'].notna()]
        unmapped = test[test['No. of ideal func'].isna()]
        
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
