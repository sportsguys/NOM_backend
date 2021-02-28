from db.models import qb, wr, rb

class QB(qb):
    def __init__(self, name):
        self.name = name # the foreign key to players

    def ping(self, row):
        self.year = row.contents[0].attrs['csk']
        self.games = row.contents[5].next
        self.completions = row.contents[8].next
        self.attempts = row.contents[9].next
        self.completion_pct = row.contents[10].next
        self.yards_passed = row.contents[11].next
        self.interceptions = row.contents[14].next
        self.avg_yards_per_pass = row.contents[19].next


class WR(wr):
    def __init__(self):
        pass

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

class RB(rb):
    def __init__(self):
        pass

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
