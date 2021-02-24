import requests
import mysql.connector as msc
from bs4 import BeautifulSoup

class Page:

    def __init__(self, url):
        response = requests.get(url)
        self.bs = BeautifulSoup(response.text, 'html.parser')
        #The main data table is the same all the way down in the HTML regardless of position. Search for that pages main table and link it to this class. Every Page needs a main table for it to be valid.
        #This code traverses down html tree until we are at the table necessary to do our work.
        element = self.bs.body
        element = element.contents[1]
        element = element.contents[13]
        element = element.contents[5]
        element = element.contents[3]
        self.mainTable = element.contents[1]
        self.careerTable = self.mainTable.contents[8].contents[0]
        self.yearsPlayed = 0
        self.td = 0
        self.avgYardsPerGame = 0

    def set_years_played(self):
        #The code below this gets you to the yearly passing stats table. In order to get to the career stats you must use a different child of the previosu element.
        element = self.mainTable.contents[7]
        self.yearsPlayed = int(len(element.contents)/2)

    def get_years_played(self):
        return self.yearsPlayed

    def establish_mysql_connection():
        mydb = msc.connect(
            host="capstone-db.cuchsam9yjhs.us-east-1.rds.amazonaws.com",
            user="",
            password=""
        )
        print(mydb.is_connected())
        print("MYSQL CONNECTED")

    #Make this an abstract method since the SQL Query will differ depending on position, although connection is the same across all.
    ##def send_mysql_data(self):
        ##raise NotImplementedError("Please Implement This Method!")

    #This is an abstract method being added to all subclasses because it is how we update all of the stats at once for that particular position.
    def ping(self):
        raise NotImplementedError("Please Implement This Method")

    def set_td(self):
        raise NotImplementedError("Please Implement This Method!")

    def set_avg_yards_per_game(self):
        raise NotImplementedError("Please Implement This Method!")

    def get_td(self):
        return self.td

    def get_avg_yards_per_game(self):
        return self.avgYardsPerGame

class QB(Page):

    def __init__(self, url):
        super().__init__(url)
        self.completions = 0
        self.attempts = 0
        self.completion_pct = 0
        self.yardsPassed = 0
        self.interceptions = 0
        self.avgYardsPerPass = 0

    #CLASS IS DONE.
    def set_completions(self):
        self.completions = self.careerTable.contents[7].string

    def get_completions(self):
        return self.completions

    def set_attempts(self):
        self.attempts = self.careerTable.contents[8].string

    def get_attempts(self):
        return self.attempts

    def set_completion_pct(self):
        self.completion_pct = float(self.completions)/float(self.attempts)

    def get_completion_pct(self):
        return self.completion_pct

    def set_td(self):
        self.td = self.careerTable.contents[11].string
    
    def set_yards_passed(self):
        self.yardsPassed = self.careerTable.contents[10].string

    def get_yards_passed(self):
        return self.yardsPassed

    def set_interceptions(self):
        self.interceptions = self.careerTable.contents[13].string

    def get_interceptions(self):
        return self.interceptions

    def set_avg_yards_per_pass(self):
        self.avgYardsPerPass = self.careerTable.contents[17].string

    def get_avg_yards_per_pass(self):
        return self.avgYardsPerPass

    def set_avg_yards_per_game(self):
        self.avgYardsPerGame = self.careerTable.contents[20].string

    def ping(self):
        self.set_years_played()
        self.set_completions()
        self.set_attempts()
        self.set_completion_pct()
        self.set_yards_passed()
        self.set_td()
        self.set_interceptions()
        self.set_avg_yards_per_game()
        self.set_avg_yards_per_pass()

class RB(Page):

    def __init__(self, url):
        super().__init__(url)
        self.rushes = 0
        self.yardsRushed = 0
        self.avgYardsPerRush = 0

    def set_rushes(self):
        self.rushes = self.careerTable.contents[6].string

    def get_rushes(self):
        return self.rushes

    def set_yards_rushed(self):
        self.yardsRushed = self.careerTable.contents[7].string

    def get_yards_rushed(self):
        return self.yardsRushed

    def set_avg_yards_per_rush(self):
        self.avgYardsPerRush = str(float(self.yardsRushed)/float(self.rushes))

    def get_avg_yards_per_rush(self):
        return self.avgYardsPerRush

    def set_td(self):
        self.td = self.careerTable.contents[8].string

    def set_avg_yards_per_game(self):
        self.avgYardsPerGame = self.careerTable.contents[12].string

    def ping(self):
        self.set_rushes()
        self.set_yards_rushed()
        self.set_avg_yards_per_rush()
        self.set_td()
        self.set_avg_yards_per_game()

class WR(Page):

    def __init__(self, url):
        super().__init__(url)
        self.targets = 0
        self.receptions = 0
        self.yardsReceived = 0

    def set_targets(self):
        self.targets = self.careerTable.contents[6].string

    def get_targets(self):
        return self.targets 

    def set_receptions(self):
        self.receptions = self.careerTable.contents[7].string

    def get_receptions(self):
        return self.receptions

    def set_yards_received(self):
        self.yardsReceived = self.careerTable.contents[8].string

    def get_yards_received(self):
        return self.yardsReceived

    def set_td(self):
        self.td = self.careerTable.contents[10].string

    def set_avg_yards_per_game(self):
        self.avgYardsPerGame = self.careerTable.contents[14].string

    def ping(self):
        self.set_targets()
        self.set_receptions()
        self.set_yards_received()
        self.set_td()
        self.set_avg_yards_per_game()

    


