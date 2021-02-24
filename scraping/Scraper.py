from Page import *
#Create a list, probably a CSV of the players names. Find a pattern in the URL and manipulate that here. Can read through a txt file with all URL and then perform async operation on that players stats.

url = "https://www.pro-football-reference.com/players/S/SharSh00.htm"

##while("file isn't empty"): while this loop runs keep obtaining URL and making a Page object with URL.

currentPlayer = WR(url)
currentPlayer.ping()

"""
print("TARGETS: " + currentPlayer.get_targets())
print("RECEPTIONS: " + currentPlayer.get_receptions())
print("YARDS: " + currentPlayer.get_yards_received())
print("TD: " + currentPlayer.get_td())
print("Y/G: " + currentPlayer.get_avg_yards_per_game())

"""
"""
print("RUSHES: " + currentPlayer.get_rushes())
print("YARDS: " + currentPlayer.get_yards_rushed())
print("AVG: " + currentPlayer.get_avg_yards_per_rush())
print("TD: " + currentPlayer.get_td())
print("Y/G: " + currentPlayer.get_avg_yards_per_game())

"""
"""
print("COMPLETIONS: " + currentPlayer.get_completions())
print("ATTEMPTS: " + currentPlayer.get_attempts())
print("CMP PCT: " + str(currentPlayer.get_completion_pct()))
print("YARDS: " + currentPlayer.get_yards_passed())
print("TD: " + currentPlayer.get_td())
print("INT: " + currentPlayer.get_interceptions())
print("Y/A: " + currentPlayer.get_avg_yards_per_pass())
print("Y/Game: " + currentPlayer.get_avg_yards_per_game())

"""