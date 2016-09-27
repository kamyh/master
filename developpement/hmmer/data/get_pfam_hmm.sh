#!/usr/bin/env bash

curl ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam30.0/Pfam-A.hmm.gz > Pfam-A.hmm.gz
gunzip -d Pfam-A.hmm.gz