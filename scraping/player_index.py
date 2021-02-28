from scraping.Page import Page

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
            try:
                career_end = str(item.contents[1]).split(' ')[2].split('-')[1]
            except: # active players are wrapped in a <b> that changes contents
                career_end = str(item.contents[1]).split(' ')[1].split('-')[1] 

            if career_end < self.cutoff:
                continue

            try:
                pos = item.contents[1].split('(')[1].split(')')[0]
                name = item.next.next
                if name == 'Anthony Adams':
                    print('w')
                url = item.contents[0].attrs['href']
            except: # active players are wrapped in a <b> that changes contents
                pos = item.contents[0].contents[1].split('(')[1].split(')')[0]
                name = item.next.next.next
                url = item.contents[0].contents[0].attrs['href']

            player_list.append((name, url, pos))
        
        return player_list
    