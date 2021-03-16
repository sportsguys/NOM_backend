from scraping.Page import Page
import re

class PlayerIndex(Page):
    def __init__(self, url=None, cutoff_year='2000'):
        if url:
            self.load_page(url)
            self.players = self.bs.select('#div_players')
            self.cutoff = cutoff_year

    def scrape_players(self):
        """ returns list of PFR-relative player tuples that meet the cutoff requirement
        """
        player_list = []
        for item in self.players[0].contents[1:-1]: #skip first and last <p> becuase theyre newlines
            
            career_end = re.search('-[0-9]{4}', item.text).group()[1:]
            if int(career_end) < 2000:
                continue

            name = item.select_one('a').text
            if str(name).endswith(' '):
                name = name[:-1]
            
            pos = item.text.split('(')[1].split(')')[0]
            if '-' in pos: #only get first/primary position
                pos = pos.split('-')[0]
            
            url = item.select_one('a').attrs['href']

            player_list.append((name, url, pos))
        
        return player_list
    