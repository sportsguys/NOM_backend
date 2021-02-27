from abc import abstractclassmethod
from scraping.page import Page

class PlayerSeason(Page):
    def __init__(self, url=None):
        # The main data table is the same all the way down in the HTML regardless of position. 
        # Search for that pages main table and link it to this class. Every Page needs a main table for it to be valid.
        # This code traverses down html tree until we are at the table necessary to do our work.
        if url:
            self.load_page(url)
            self.mainTable = self.bs.body.contents[1].contents[13].contents[5].contents[3].contents[1]
            self.careerTable = self.mainTable.contents[8].contents[0]

    def set_years_played(self):
        element = self.mainTable.contents[7]
        self.yearsPlayed = int(len(element.contents)/2)

    def get_years_played(self):
        return self.yearsPlayed
        
    def ping(self):
        self.set_years_played()
        self.set_td()
        self.set_avg_yards_per_game()

    def set_td(self):
        raise NotImplementedError("Please Implement This Method!")

    def set_avg_yards_per_game(self):
        raise NotImplementedError("Please Implement This Method!")

    def get_td(self):
        return self.td

    def get_avg_yards_per_game(self):
        return self.avgYardsPerGame