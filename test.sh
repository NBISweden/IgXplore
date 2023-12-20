#!/bin/bash
set -euo pipefail
set -x
# The version of the test dataset
version=1

# Retrieve test dataset
testdata_file=igxplore-testdata-${version}.tar
if ! [[ -f ${testdata_file} ]]; then
  wget -nv https://export.uppmax.uu.se/snic2021-23-477/igxplore-testdata-1.tar
fi
rm -rf igxplore-testdata
tar xf igxplore-testdata-${version}.tar

# Merge paired-end dataset into single ends
single_end_fasta=igxplore-testdata/reads/sample19premerged.fasta
if ! [[ -f ${single_end_fasta} ]]; then
  igdiscover merge igxplore-testdata/reads/sample19_{1,2}.fastq.gz ${single_end_fasta}.fastq.gz
  cutadapt --quiet -o ${single_end_fasta} ${single_end_fasta}.fastq.gz
  rm ${single_end_fasta}.fastq.gz
fi

# Initialize pipeline directory
rm -rf testrun
mkdir testrun
cd testrun
cp ../igxplore.yaml .
cp ../experiments.tsv .
ln -s ../igxplore-testdata/reads reads
ln -s ../igxplore-testdata/databases databases

# Run the pipeline
snakemake -p --cores=all -s ../Snakefile "$@"
