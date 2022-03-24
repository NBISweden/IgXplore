#!/bin/bash
# Create test datasets from SRR5408019, SRR5408020, SRR5408024

for d in 19 20 24; do
  for r in 1 2; do
    curl ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR540/00${d:1}/SRR54080${d}/SRR54080${d}_${r}.fastq.gz | gzip -dc | head -n 400000 | tail -n 4000 | gzip -9 > sample${d}_${r}.fastq.gz
  done
done
