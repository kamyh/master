# Build

$ docker build -t tm/hmmer .

# Run hmmer search

## From container

$ docker run -v ~/hmmer/data:/data -it tm/hmmer
$ hmmsearch --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta

## From Host

$ docker run --rm --privileged -v ~/hmmer/data:/data tm/hmmer hmmsearch --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta

## Run with benchmark timer

$ time ./run.sh