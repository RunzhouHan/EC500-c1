#Created by Ferris Armstrong

import subprocess
import time
start_time = time.time()
def main():
    subprocess.call("python.exe Mini_project.py") #call the python file
    print("--- %s seconds ---" % (time.time() - start_time)) #get the runtime
    return

if __name__=='__main__':
    main()
