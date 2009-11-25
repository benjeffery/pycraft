import yaml
import SocketServer
import threading
import sys

from agents import econ_agent
from detect_src_change import execute_on_change
import command
from game import Game

config = yaml.load(open('cfg/server.yml'))

def reload_modules():
    import game
    reload(game)
    import agents.econ_agent
    reload(agents.econ_agent)
    import command
    reload(command)

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
        game.active = True
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
    
        if 'speed' in config:
            command.game_speed(int(config['speed']))

        if config['restart_on_change']:
            def reload_and_restart():
                reload_modules()
                command.restart_game()
                
            t = threading.Thread(target=execute_on_change, args=(reload_and_restart,))
            t.start()
             
        n = 0
        try:
            for line in self.readlines():
                line = line.split(':')
                status, units = line[0], line[1:]
                game.set_my_status(status)
                game.set_units(units)
                if n == 0:
                    print "Launching Agent"
                    t = threading.Thread(target=econ_agent.loop, args=(game,command))
                    t.start()
                n += 1
                commands = 'commands'
                if not command.queue.empty():
                    commands += command.queue.get()
                    print commands
                self.request.send(commands)
        finally:
            print "Client Disconnected"
            game.active = False
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

