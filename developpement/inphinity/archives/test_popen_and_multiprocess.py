import subprocess
from multiprocessing import Pool

def cmd(value):
    from time import gmtime, strftime
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    #This command could have multiple commands separated by a new line \n
    some_command = "ls && sleep 10 && echo %d" % value

    p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    #This makes the wait possible
    p_status = p.wait()

    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    #This will give you the output of the command being executed
    print("Command output: %s" % output)

    return [start_time, end_time]

def multiprocess():
    p = Pool(5)
    print(p.map(cmd, [1, 2, 3]))

if __name__ == '__main__':
    multiprocess()