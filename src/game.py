class Game:
    def __init__(self):
        self.other_players = []
        self.me = {}
        self.players_by_id = {}
        pass
    
    def set_player_info(self,line):
        raw_players = line.split(':')
        rubbish, my_id = raw_players[0].split(';')
        for raw_player in raw_players[1:]:
            player = dict(zip(['id',
                               'race',
                               'name',
                               'type',
                               'ally'], raw_player.split(';')))
            player['ally'] = player['ally'] == '1'
            if player['id'] == my_id:
                self.me.update(player)
            else:
                self.other_players.append(player)
        print 'I am', self.me
        print 'Other players', self.other_players
        for player in self.other_players:
            self.players_by_id[player['id']] = player
            self.players_by_id[self.me['id']] = self.me
        
    def set_start_locations(self, line):
        pass
    
    def set_map_data(self, line):
        pass
    
    def set_choke_data(self, line):
        pass
    
    def set_bases_data(self, line):
        pass
    
    def set_my_status(self, line):
        status = dict(zip(['minerals', 
                           'gas', 
                           'supply_used', 
                           'supply', 
                           'tech_status', 
                           'upgrade_status'], line.split(';')[1:]))
        for data in ['minerals', 
                     'gas', 
                     'supply_used', 
                     'supply']:
            status[data] = int(status[data])
        del status['tech_status']
        del status['upgrade_status']
        print status
    
