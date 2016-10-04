#!/usr/bin/env bash

docker run --rm --privileged -v ~/tm/hmmer/data:/data tm/hmmer hmmsearch --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta