#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import glob
import os
import multiprocessing #https://docs.python.org/2/library/multiprocessing.html
import subprocess

# Function take a fasta file as input with the following format:
# user@computer:~$ python Calculator_C.py my_protein_sequences.fasta
# Output will print to screen and will also create an output called "count_C.txt" for the 
## specified input file. There will be three tab-delimited columns. The first is the header
## for each organism in the fasta file, the second is the total number of C-atoms counted 
## for each amino acid side chain in the protein sequence (not counting the backbone),
## and the third is the average number of C-atoms the protein sequence (i.e., normalized to amino acid sequence length)

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))
    
a=sys.argv[1]
f = open(a, 'r')
counter=0
f2=open("count_C.txt",'w') #add an extention to make it unique

for name, seq in read_fasta(f):
	seqf=seq
	seql=len(seq)
	if re.match('[U]',seqf):
		for letter in seqf:
			if letter=="A":
				counter+=5
			elif letter=="U":
				counter+=2
			elif letter=="G":
				counter+=5
			elif letter=="C":
				counter+=3
			else:
				print("ERROR, Unknown letter in Sequence, Please Check!!!!")
		print(counter, "Final Nucleotide")
		counter=0

	else:
		for letter in seqf:
			if letter=="G":
				counter+=0
				#print letter+str(counter)
			elif any(c in letter for c in ("A","C","S")):
				counter+=1
				#print letter+str(counter)
			elif any(c in letter for c in ("D","N","T")):
				counter+=2
				#print letter+str(counter)
			elif any(c in letter for c in ("E","M","P","Q","V")):
				counter+=3
				#print letter+str(counter)
			elif any(c in letter for c in ("H","I","K","L","R")):
				counter+=4
				#print letter+str(counter)
			elif any(c in letter for c in ("F","Y")):
				counter+=7
				#print letter+str(counter)
			elif letter=="W":
				counter+=9
				#print letter+str(counter)
			else:
				print("ERROR, Unknown letter in Sequence, Please Check!!!!")
		print(name, counter, counter/seql) #, "Final Amino Acid"
		f2.write(str(name)+'\t'+str(counter)+'\t'+str(counter/seql)+'\n')
		counter=0
f2.close()