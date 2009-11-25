import os,glob,stat,time

def checkSumRecurse():
  val = 0
  for dirpath, dirs, files in os.walk('.'):
      for file in [file for file in files if file[-3:]=='.py' or file[-4:] == '.yml']:
          absoluteFileName = os.path.join( dirpath, file)
          stats = os.stat(absoluteFileName)
          val += stats [stat.ST_SIZE] + stats [stat.ST_MTIME]
  return val
  
val = checkSumRecurse()

def files_changed():
    global val
    new_val = checkSumRecurse()
    changed = new_val != val
    val = new_val
    return changed
    
def execute_on_change(function):
    while True:
        if files_changed():
            function()
            break
        time.sleep(1)
