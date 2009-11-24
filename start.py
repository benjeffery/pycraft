import yaml
import src.server

config = yaml.load(open('cfg/server.yml'))

print 'Creating server at',config['bind_ip']+':'+str(config['port'])
server = src.server.ThreadedTCPServer((config['bind_ip'],config['port']), src.server.AITCPServer)
server.allow_reuse_address = True
server.serve_forever()
