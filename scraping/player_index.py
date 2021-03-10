from scraping.Page import Page
from scraping.player import switch

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
            career_start = item.text.split(' ')[3].split('-')[0]
            if career_start < self.cutoff:
                continue

            pos = item.text.split('(')[1].split(')')[0]
            if '-' in pos: #only get first/primary position
                pos = pos.split('-')[0]
            if pos not in switch:
                continue
            
            name = item.select_one('a').text
            url = item.select_one('a').attrs['href']
            
            player_list.append((name, url, pos))
        
        return player_list
    