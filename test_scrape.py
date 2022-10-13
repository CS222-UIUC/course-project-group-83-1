import unittest
import scrape
import pandas as pd
import os 
class TestScrape(unittest.TestCase):
    def setUp(self):
        scrape.scrape_test(["HI", "we"], '2021-10-05', '2021-11-05')
        self.df = pd.read_json("tweets.json")
    def tearDown(self):
        os.remove("tweets.json")
    def test_correctdates(self):
        for i, row in self.df.iterrows():
            self.assertTrue(row["Date"] >= pd.Timestamp(year=2021, month=10, day=5) 
            and row["Date"] <= pd.Timestamp(year=2021, month=11, day=5))
    def test_uniqueuser(self):
        set_users = set()
        for i, row in self.df.iterrows():
            self.assertFalse(row['User'] in set_users)
            set_users.add(row['User'])

if __name__ == '__main__':
    unittest.main()