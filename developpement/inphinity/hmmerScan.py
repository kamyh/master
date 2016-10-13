##
#   Created by: Deruaz Vincent
#   wrapper of hmmer scan calls from a docker container
#   03.10.2016
##

from subprocess import Popen, PIPE
import os;

class HmmerScan:
    def __init__(self):
        print("HmmerScan wrapper tool initialization")

    ##
    #   Display the output of 'docker ps' command
    ##
    def docker_ps(self):
        p = Popen(["docker", "ps"])
        output = p.communicate()[0]
        print(output)

    def ls(self):
        p = Popen(["ls"])
        output = p.communicate()[0]
        print(output)

    ##
    #   Display the output of the scan hmmer command
    #   docker run --rm --privileged -v $PWD/data:/data tm/hmmer hmmsearch --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta
    ##
    def compute_domaine_from_host(self):
        pwd = '../dockers/hmmer'
        cwd = os.getcwd()

        os.chdir(pwd)

        self.ls()

        p = Popen([
            "docker",
            "run",
            "--rm",
            "--privileged",
            "-v",
            cwd + "/data:/data",
            "tm/hmmer",
            "hmmsearch",
            "--tblout",
            "/data/results/hits.txt",
            "/data/Pfam-A.hmm",
            "/data/fasta/test_data.fasta" #TODO issue with file directory - Cannot be called from hmmer dir
        ])
        output = p.communicate()[0]
        print(output)