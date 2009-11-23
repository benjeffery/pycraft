import yaml
import Queue
import game

commands = yaml.load(open('../cfg/commands.yml'))
names = yaml.load(open('../cfg/id_names.yml'))

queue = Queue.Queue()

#Check that none of the strings overlap so we can look up a sting regardless of its type
a = sum(len(dict_) for dict_ in names.values())
id_of = {}
for dict_ in names.values():
    id_of.update(dict_)
assert(a == len(id_of))

def add_command_to_queue(command_name, unit, *args):
    global queue
    if commands[command_name]['num_args'] != len(args):
        print "Bad command args", command_name, len(args)
            
    #Convert any strings in the args to ids
    raw_args = [0,0,0]
    for i,arg in enumerate(args):
        if type(arg) == str:
            try:
                raw_args[i] = id_of[arg]
            except KeyError:
                print "Bad name", arg
        elif type(arg) == game.Unit:
            raw_args[i] = arg.id
        else:
            raw_args[i] = arg
    commands[command_name]['id']
    command_string = ":%d;%d;%d;%d;%d"%(
                    commands[command_name]['id'],
                    unit.id,
                    raw_args[0],
                    raw_args[1],
                    raw_args[2]
                    )
    queue.put(command_string)

def wrap_command(command_name):
    def closure(unit, *args):
        return add_command_to_queue(command_name, unit, *args)
    return closure

#Inject the commands into this modules namespace
for command in commands:
    globals()[command] = wrap_command(command)
    
