from Bio import Entrez

Entrez.email = "vincent.deruaz@master.hes-so.ch"
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

query = 'G[gene] AND VHSV[orgn] NOT "mRNA"[title] AND "complete cds"[title]'
handle = Entrez.esearch(db='nucleotide',retmax=1000,term=query)
record = Entrez.read(handle)
gi = record['IdList']
print (len(gi))

protein_info = Entrez.efetch(db="nucleotide",id=gi,rettype="gb",retmode="xml")
protein_info = Entrez.read(protein_info)