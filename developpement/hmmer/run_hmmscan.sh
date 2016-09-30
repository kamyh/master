#!/usr/bin/env bash

# hmmpress /data/Pfam-A.hmm only first time fter getting the .hmm file
docker run --rm --privileged -v $PWD/data:/data tm/hmmer hmmpress /data/Pfam-A.hmm

docker run --rm --privileged -v $PWD/data:/data tm/hmmer hmmscan --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta