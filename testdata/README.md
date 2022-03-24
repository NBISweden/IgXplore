The files in this directory make it possible to recreate the test dataset if necessary.

To create the human heavy chain database, run `make`.
This creates (among other temporary files), the files
`IGHV.fasta`, `IGHD.fasta` and `IGHJ.fasta`.

To create the `sample*.fastq.gz` files, run `./download.sh`.

Then create igxplore-testdata:

    mkdir -p igxplore-testdata/{databases/human/IGH,reads}
    for d in V D J; do cp IGH${d}.fasta igxplore-testdata/databases/human/IGH/${d}.fasta; done
    cp sample{19,20,24}_{1,2}.fastq.gz igxplore-testdata/reads/
    tar cf igxplore-testdata-1.tar igxplore-testdata/

Source for the test reads are: SRR5408019, SRR5408020, SRR5408024.
To avoid any potential legal problems, we do not redistribute parts of the
IMGT database, but recreate a simple V/D/J (heavy chain) database from
public ENSEMBL and NCBI annotations.
