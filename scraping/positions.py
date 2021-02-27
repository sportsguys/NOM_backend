from scraping.player_season import PlayerSeason
from db.models import qb, wr, te, rb

class QB(PlayerSeason, qb):
    def __init__(self, url=None):
        super().__init__(url)

    def set_completions(self):
        self.completions = self.careerTable.contents[7].string

    def set_attempts(self):
        self.attempts = self.careerTable.contents[8].string

    def set_completion_pct(self):
        self.completion_pct = float(self.completions)/float(self.attempts)

    def set_td(self):
        self.td = self.careerTable.contents[11].string
    
    def set_yards_passed(self):
        self.yardsPassed = self.careerTable.contents[10].string

    def set_interceptions(self):
        self.interceptions = self.careerTable.contents[13].string

    def set_avg_yards_per_pass(self):
        self.avgYardsPerPass = self.careerTable.contents[17].string

    def set_avg_yards_per_game(self):
        self.avgYardsPerGame = self.careerTable.contents[20].string

    def ping(self):
        #super().ping()
        self.set_completions()
        self.set_attempts()
        self.set_completion_pct()
        self.set_yards_passed()
        self.set_interceptions()
        self.set_avg_yards_per_pass()


class WR(PlayerSeason, wr):
    def __init__(self, url=None):
        super().__init__(url)

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
        #super().ping()
        self.set_targets()
        self.set_receptions()
        self.set_yards_received()

class RB(PlayerSeason, rb):
    def __init__(self, url=None):
        super().__init__(url)

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

    def ping(self):
        #super().ping()
        self.set_rushes()
        self.set_yards_rushed()
        self.set_avg_yards_per_rush()

class TE(PlayerSeason, te):
    pass
