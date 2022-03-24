#!/usr/bin/env python3
import sys
import re
from pyfaidx import Fasta

fasta = Fasta(sys.argv[1])
gene_name = sys.argv[2]

# Only tested with these gene types. Certainly works for others.
assert gene_name in ('IGHV', 'IGHD', 'IGHJ')

CHROMOSOMES = {
	'NC_000014.9': '14',
}
# search_gene_name = ' gene_name "{}'.format(gene_name)
gene_name_regex = re.compile(';gene=([^;]*);')
for line in sys.stdin:
	if line.startswith('#'):
		continue
	fields = line.strip().split('\t')
	chrom, source, feature, start, end, score, strand, frame, attributes = fields
	if feature != 'gene':
		continue
	name = gene_name_regex.search(attributes).group(1)
	if not name.startswith(gene_name):
		continue
	start = int(start) - 1
	end = int(end)
	chrom = CHROMOSOMES[chrom]
	sequence = fasta[chrom][start:end]
	if strand == '-':
		sequence = sequence.reverse.complement
	else:
		assert strand == '+'
	sequence = str(sequence)
	print('>{}\n{}'.format(name, sequence))
