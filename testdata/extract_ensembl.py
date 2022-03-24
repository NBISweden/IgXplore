#!/usr/bin/env python3
import sys
import re
from pyfaidx import Fasta

fasta = Fasta(sys.argv[1])
gene_name = sys.argv[2]

# Only tested with these gene types. Certainly works for others.
assert gene_name in ('IGHV', 'IGHD', 'IGHJ')

sequences = set()
search_gene_name = ' gene_name "{}'.format(gene_name)
gene_name_regex = re.compile(' gene_name "([^"]*)"')
for line in sys.stdin:
	if line.startswith('#'):
		continue
	fields = line.strip().split('\t')
	chrom, source, feature, start, end, score, strand, frame, attributes = fields
	if feature != 'gene':
		continue
	if search_gene_name not in attributes:
		continue
	start = int(start) - 1
	end = int(end)
	sequence = fasta[chrom][start:end]
	if strand == '-':
		sequence = sequence.reverse.complement
	else:
		assert strand == '+'
	sequence = str(sequence)
	name = gene_name_regex.search(attributes).group(1)
	if sequence in sequences:
		print('Sequence of record {!r} already seen, skipping'.format(name), file=sys.stderr)
		continue
	sequences.add(sequence)
	print('>{}\n{}'.format(name, sequence))
