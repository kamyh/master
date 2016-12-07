import subprocess
from multiprocessing import Pool
from config import Config
import uuid
from toolsIo import ToolsIO
from database_utilities import DBUtilties
from Bio import *
from Bio import SeqIO
import multiprocessing

DEBUG = True


def analyze_domaines(values_tab):
    from time import gmtime, strftime
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    configuration = Config('inphinity/v_0.3/config_v0.3.ini')
    io = ToolsIO()
    path_to_core = configuration.get_path_to_core()

    fasta = '>' + values_tab[0] + '\n' + values_tab[1] + '\n'
    fasta_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.fasta'
    io.write(fasta_filename, fasta)

    results_filename = "/data-hmm/results/hits_test_" + str(uuid.uuid4()) + ".txt"

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
        results_filename + " " +
        "/data-hmm/Pfam-A.hmm " +
        fasta_filename
        # "/data-hmm/fasta/seq_diogo_03102016.fasta"
    ], stdout=subprocess.PIPE, shell=True)

    (output, err) = p.communicate()

    # This makes the wait possible
    p_status = p.wait()

    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    results = io.read_results(results_filename, configuration.get_detailed_logs())

    returned_domains = []

    for result in results:
        result_tab = result.split(' ')
        result_tab = list(filter(None, result_tab))

        best_1_domain = result_tab[2]
        num_domain = result_tab[3].split('.')[0]
        e_value = result_tab[4]
        score = result_tab[5]
        biais = result_tab[6]

        returned_domains.append(num_domain)

    p = subprocess.Popen([
        "rm",
        results_filename
    ])
    p.communicate()
    p_status = p.wait()

    p = subprocess.Popen([
        "rm",
        fasta_filename
    ])
    p.communicate()
    p_status = p.wait()

    return [values_tab[0], returned_domains, [start_time, end_time]]


# TODO: check seek_domaines() original fct
def seek_domaines_multiprocess(tab, id_cell):
    bool_bacteria = 0

    print('CPU Count: %s' % multiprocessing.cpu_count())
    pool_size = multiprocessing.cpu_count()
    print('Pool Size: %s' % pool_size)

    p = Pool(pool_size)
    results = p.map(analyze_domaines, tab)

    print(results)

    for result in results:
        id_prot = result[0]
        domaines_returned = result[1]

        db.execute_insert_domains(id_prot, domaines_returned, id_cell, bool_bacteria, "--")


#####################################

def analyze_organisme(id, db):
    print('Organism ID: ' + str(id))
    pidss_bact = []
    pseqss_bact = []
    resultats_organismes = db.get_sequence_proteines_bacteria(id)
    pidss_bact, pseqss_bact = parse_sequences_prot(resultats_organismes[0][3])

    if (DEBUG):
        pidss_bact = pidss_bact[:10]
        pseqss_bact = pseqss_bact[:10]

    # seek_domaines(pidss_bact, pseqss_bact, id, 0)
    print('%d sequences to compute domaines!' % (len(pidss_bact)))
    seek_domaines_multiprocess(zip(pidss_bact, pseqss_bact), id)

    db.show_tables_of_phage_bact()


# Parser les sequences multi-fasta
def parse_sequences_prot(sequence):
    configuration = Config('inphinity/v_0.3/config_v0.3.ini')
    pid = []
    pseq = []
    text_file = open(configuration.get_temp_file_p_seqs(), "w")
    text_file.write(sequence)
    text_file.close()

    fasta_sequences = SeqIO.parse(open(configuration.get_temp_file_p_seqs()), 'fasta')
    for fasta in fasta_sequences:
        pid.append(fasta.id)

        # pseq.append(fasta.seq.tostring()) DEPRECATED (toSting())
        pseq.append(str(fasta.seq))

        # new_sequence = some_function(sequence)
        # write_fasta(out_file)

    return pid, pseq


if __name__ == '__main__':
    db = DBUtilties(False)
    list_id_organismes = db.get_id_all_bacts()

    nbr_organismes = len(list_id_organismes)
    nbr_organismes_analyzed = 0

    for id in list_id_organismes:
        print('%d/%d organismes analysed' % (nbr_organismes_analyzed, nbr_organismes))
        analyze_organisme(id, db)
        nbr_organismes_analyzed += 1
