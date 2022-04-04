# V/D/J gene database bootstrapping
#
# This uses the ENSEMBL and NCBI annotations to create files with the sequence of some known
# human IGHV, IGHD and IGHJ genes.

REF := Homo_sapiens.GRCh38.dna.primary_assembly.fa

.PRECIOUS: $(REF) $(REF).fai

.INTERMEDIATE: $(REF).gz

.PHONY: all clean

all: IGHV.fasta IGHD.fasta IGHJ.fasta

clean:
	rm -f IGH[VDJ].fasta ncbi-genes.txt ensembl-genes.txt ncbi.IGH[VDJ].fasta ensembl.IGH[VDJ].fasta

ncbi.IGH%.fasta: ncbi-genes.txt venv-has-pyfaidx $(REF) $(REF).fai
	.venv/bin/python3 extract_ncbi.py $(REF) IGH$* < $< > $@

ensembl.IGH%.fasta: ensembl-genes.txt venv-has-pyfaidx $(REF) $(REF).fai
	.venv/bin/python3 extract_ensembl.py $(REF) IGH$* < $< > $@

IGHJ.fasta: ncbi.IGHJ.fasta
	awk '/^>/ {$$0 = $$0  "*99"};1' $< | sed 's|GT$$||' > $@

IGHV.fasta: ncbi.IGHV.fasta
	@# trim leader sequence
	awk '/^>/{name=$$0};!/^>/{s=substr($$0, length($$0)-310); i=match(s, ".A..T.....T.....A....GG"); if (i>0){printf("%s\n%s\n", name, substr(s, i))}}' $< >$@

IGHD.fasta: ensembl.IGHD.fasta
	cp $< $@

ensembl-genes.txt: Homo_sapiens.GRCh38.92.gtf.gz
	zgrep ' gene_biotype "IG_[VDJ]_gene"' $< | awk '$$3=="gene"' > $@.tmp && mv $@.tmp $@

ncbi-genes.txt: GCF_000001405.38_GRCh38.p12_genomic.gff.gz
	zgrep '^NC_000014.9\b.*\b;gene=IGH[VDJ].*;gene_biotype=[VDJ]_segment;' $< | tac > $@

%.fa: %.fa.gz
	gunzip $^

%.fa.fai: %.fa
	samtools faidx $^

venv-has-pyfaidx: .venv/bin/pip
	.venv/bin/pip install pyfaidx && touch venv-has-pyfaidx

.venv/bin/pip:
	python3 -m venv .venv

# Downloads
$(REF).gz:
	wget http://ftp.ensembl.org/pub/release-92/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

Homo_sapiens.GRCh38.92.gtf.gz:
	wget ftp://ftp.ensembl.org/pub/release-92/gtf/homo_sapiens/Homo_sapiens.GRCh38.92.gtf.gz

GCF_000001405.38_GRCh38.p12_genomic.gff.gz:
	wget https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/annotation/annotation_releases/109/GCF_000001405.38_GRCh38.p12/GCF_000001405.38_GRCh38.p12_genomic.gff.gz
	# this used to be available at
	# ftp://ftp.ncbi.nlm.nih.gov/genomes/Homo_sapiens/GFF/ref_GRCh38.p12_top_level.gff3.gz
