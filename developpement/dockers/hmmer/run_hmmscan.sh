#!/usr/bin/env bash

# hmmpress /data/Pfam-A.hmm only first time fter getting the .hmm file
docker run --rm --privileged -v $PWD/data:/data tm/hmmer hmmpress /data/Pfam-A.hmm

docker run --rm --privileged -v $PWD/data-hmm:/data-hmm tm/hmmer hmmscan --tblout /data-hmm/results/hits.txt /data-hmm/Pfam-A.hmm /data-hmm/fasta/seq_diogo_03102016.fasta