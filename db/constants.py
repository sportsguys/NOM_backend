yearly_caps = {
    2011: 120375000,
    2012: 120600000,
    2013: 123600000,
    2014: 133000000,
    2015: 143280000,
    2016: 155270000,
    2017: 167000000,
    2018: 177200000,
    2019: 188200000,
    2020: 198200000
}

min_roster_dist = {
    'QB': 2,
    'RB': 4,
    'TE': 3,
    'WR': 5,
    #'OL': 8,
    'DL': 8,
    'LB': 7,
    'DB': 9,
    'K' : 2
}

position_map = {
    'QB': ['QB', 'QB/TE'],
    'RB': ['RB', 'HB', 'FB'],
    'TE': ['TE'],
    'WR': ['WR'],
    'OL': ['G', 'T', 'LT', 'RT', 'C', 'RG', 'LG', 'OG', 'NT', 'OT', 'OL', 'G,T', 'C,G', 'G,C', 'T,G'],
    'DL': ['DT', 'DE', 'DL'],
    'LB': ['OLB', 'ILB', 'LB', 'EDGE'],
    'DB': ['CB', 'FS', 'S', 'SS', 'DB'],
    'K' : ['K', 'P', 'LS']
}

roles = {
    'offense': ['QB', 'RB', 'TE', 'WR'],
    'defense': ['DL', 'LB', 'DB'],
    'kicker': ['K']
}
