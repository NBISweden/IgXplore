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

# Initialize pipeline directory
rm -rf testrun
mkdir testrun
cd testrun
cp ../igxplore.yaml .
cp ../samples.tsv .
ln -s ../igxplore-testdata/reads reads
ln -s ../igxplore-testdata/databases databases

# Run the pipeline
snakemake -p -s ../Snakefile "$@"
