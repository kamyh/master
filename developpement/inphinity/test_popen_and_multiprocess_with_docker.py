import subprocess
from multiprocessing import Pool
from config import Config
import uuid
from toolsIo import ToolsIO

def cmd(value):
    from time import gmtime, strftime
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    configuration = Config('inphinity/default.ini')
    io = ToolsIO()
    path_to_core = configuration.get_path_to_core()

    #This command could have multiple commands separated by a new line \n
    #some_command = "ls && sleep 10 && echo %d" % value

    results_filename = "/data-hmm/results/hits_test_"+str(uuid.uuid4())+".txt"

    p = subprocess.Popen([
        "docker " +
        "run " +
        "--rm " +
        "--privileged " +
        "-v " +
        path_to_core + "/data-hmm:/data-hmm " +
        "inphinity-hmmer " +
        "hmmsearch " +
        "--tblout " +
        results_filename+" " +
        "/data-hmm/Pfam-A.hmm " +
        "/data-hmm/fasta/seq_diogo_03102016.fasta"
    ], stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    #This makes the wait possible
    p_status = p.wait()

    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    results = io.read_results(results_filename, configuration.get_detailed_logs())

    returned_domains=[]

    for result in results:
        result_tab = result.split(' ')
        result_tab = list(filter(None, result_tab))

        best_1_domain=result_tab[2]
        num_domain=result_tab[3].split('.')[0]
        e_value=result_tab[4]
        score=result_tab[5]
        biais=result_tab[6]

        returned_domains.append(num_domain)

    p = subprocess.Popen([
        "rm",
        results_filename
    ])
    p.communicate()
    p_status = p.wait()

    return [start_time, end_time]

def multiprocess():
    p = Pool(5)
    print(p.map(cmd, [1, 2, 3]))

if __name__ == '__main__':
    multiprocess()