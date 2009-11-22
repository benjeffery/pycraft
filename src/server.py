import yaml
import SocketServer

from game import Game

config = yaml.load(open('../cfg/server.yml'))


class AITCPServer(SocketServer.BaseRequestHandler):
    
    #Generator to yield lines from a buffer
    def readlines(self):
        socket = self.request
        buffer = socket.recv(4096)
        done = False
        while not done:
            if '\n' in buffer:
                (line, buffer) = buffer.split('\n', 1)
                yield line
            else:
                more = socket.recv(4096)
                if not more:
                    done = True
                else:
                    buffer = buffer + more
        if buffer:
            yield buffer
            
    def handle(self):
        print 'Connection Recieved'
        lines = self.readlines()
        game = Game()
        game.set_player_info(lines.next())
        #Config reply
        options = ['allow_user_control', 
                   'complete_information',
                   'log_commands',
                   'terrain_analysis']
        options = ''.join(str(int(config[option])) for option in options)
        self.request.send(options)
        
        game.set_start_locations(lines.next())
        game.set_map_data(lines.next())
        
        if config['terrain_analysis']:
            game.set_choke_data(lines.next())
            game.set_bases_data(lines.next())
    
        for line in self.readlines():
            line = line.split(':')
            status, units = line[0], line[1:]
            game.set_my_status(status)
            
            self.request.send('commands')
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    print 'Creating server at',config['bind_ip']+':'+str(config['port'])
    server = ThreadedTCPServer((config['bind_ip'],config['port']), AITCPServer)
    server.allow_reuse_address = True
    server.serve_forever()
