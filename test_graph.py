import unittest
import graph
from pathlib import Path
'''
Basic testing of the data visualization functions in graph.py.
This code checks if the graphs were sucessfully outputted (testing
should be done for the data since the plotting libraries are accurate).
You can also look at the generated graphs.
'''
class TestScrape(unittest.TestCase):
    #Tests that the bar graph was created
    def test_bar(self):
        graph.create_bar("processed_df.json")
        my_file = Path("bar_graph.png")
        self.assertTrue(my_file.is_file())
    
    #Tests that the pie chart was created
    def test_pie(self):
        graph.create_pie("processed_df.json")
        my_file = Path("pie_chart.png")
        self.assertTrue(my_file.is_file())

    #Tests that the scatter plot was created
    def test_scatter(self):
        graph.create_scatter('processed_df.json')
        my_file = Path("scatter_plot.png")
        self.assertTrue(my_file.is_file())

if __name__ == '__main__':
    unittest.main()