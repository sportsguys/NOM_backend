from scraping.page import Page

class PlayerIndex(Page):
    def __init__(self, url=None, cutoff_year='2000'):
        if url:
            self.load_page(url)
            self.players = self.bs.select('#div_players')
            self.cutoff = cutoff_year

    def scrape_players(self):
        """ returns list of PFR-relative player urls that meet the cutoff requirement
        """
        url_list = []
        for item in self.players[0].contents[1:-1]: #skip first and last <p> becuase theyre newlines
            try:
                career_start = str(item.contents[1]).split(' ')[2].split('-')[0]
            except: # active players are wrapped in a <b> that changes contents
                career_start = str(item.contents[1]).split(' ')[1].split('-')[0] 
            if career_start < self.cutoff:
                continue
            try:
                pos = item.contents[1].split('(')[1].split(')')[0]
                url_list.append((item.contents[0].attrs['href'], pos))
            except: # active players are wrapped in a <b> that changes contents
                pos = item.contents[0].contents[1].split('(')[1].split(')')[0]
                url_list.append((item.contents[0].contents[0].attrs['href'], pos))
        return url_list
    
    


