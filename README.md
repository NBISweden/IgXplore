# IgXplore

## Installation

- Install Conda and Bioconda. Use the
  [Bioconda instructions](https://bioconda.github.io/user/install.html) if you
  don’t have Conda and/or Bioconda, yet.
- Optionally, but highly recommend is to install [Mamba](https://github.com/mamba-org/mamba),
  which is a faster alternative to Conda:

      conda install mamba

  If you skip this, write `conda` instead of `mamba` in the next step,
  but the installation will take longer.

- Create a new Conda environment and install the dependencies into it:

      mamba env create -n igxplore -f environment.yml

- Activate the environment

      conda activate igxplore


## Running the pipeline

1. Create a directory ("run directory") for the new pipeline run and change into it.
   We call it "myrun" in the following:

       mkdir myrun
       cd myrun

2. Create a directory named `reads/`

       mkdir reads

3. Make the paired-end FASTQ files (`.fastq` or `.fastq.gz`) for all samples available in the
   `reads/` directory, preferably by using symbolic links.
   For example:

       cd reads
       ln -s /path/to/raw/reads/sample1_R1.fastq.gz .
       ln -s /path/to/raw/reads/sample1_R2.fastq.gz .
4. Create a directory for the V/D/J germline database and place the appropriate
   `V.fasta`, `D.fasta`, `J.fasta` files into it.

       mkdir database
       cp /path/to/database/{V,D,J}.fasta database/

   If your run uses multiple databases, you need to create multiple database directories.
   For example, if you have databases `mouse1` and `mouse2`, you can arrange the directories
   like this:

       mkdir databases
       mkdir databases/mouse1
       mkdir databases/mouse2
   (Then copy the appropriate V/D/J.fasta files into `databases/mouse1` and `databases/mouse2`.)
5. Copy the file `igxplore.yaml` into the run directory.
   Open it with a text editor and adjust it (if necessary).
6. Create a sample sheet file `samples.tsv` within the `myrun/` directory.
   Use the provided template or write a file from scratch; see the section below.
7. Finally, run the pipeline using the provided `Snakefile`:

       snakemake -p -j8 -s ../path/to/Snakefile
   Adjust the value 8 according to how many CPU cores you want to use,
   or use `-j all` to use all available cores.


## The sample sheet

The sample sheet `samples.tsv` is a table that lists all samples of a run
along with their metadata. Example:

    sample_id  database        r1                   timepoint
    sample19   .               sample19_1.fastq.gz  6
    sample20   .               sample20_1.fastq.gz  12
    sample24   databases/IGH/  sample24_1.fastq.gz  24

- Any row that starts with `#` is a comment and is ignored.
- The values cannot contain spaces.
- Columns *sample_id*, *database* and *r1* are required.
- *sample_id* is an arbitrary name that must be unique for each sample.
- *database* is the path to the database to use for that sample.
  If you write a dot (`.`), the database that is configured in `igxplore.yaml` is used.
- *r1* is the name of a FASTQ file within the `reads/` directory.
  This is the name to the file containing R1 reads.
  The name for the second (R2) file is detected automatically.
- Any extra columns (here: *timepoint*) are taken to be sample-specific metadata and
  are copied to the final output table.

The file can be edited in a text editor or even in a spreadsheet program such
as LibreOffice Calc (you can run `localc samples.tsv` on the command line to open
the file in Calc).


## Result files

The pipeline creates the following main result files in the run directory.

* `report.html`: Report in HTML format. Open this in a browser.
* `clonotypes.tsv`: Merged clonotype tables of all samples.
* `filtered.tsv.gz`: Merged `filtered.tsv.gz` tables of all samples.

The merged tables contain an additional *sample_id* column and
also all extra metadata columns specified in `samples.tsv`.

Results for individual runs can be found in subdirectories named according to *sample_id*.


## Running the tests (during development)

Follow the installation instructions as above.

Then, it is recommended that you enable the IgDiscover cache,
which you can do the following way:

    echo "use_cache: true" > ~/.config/igdiscover.conf

See <http://docs.igdiscover.se/en/stable/guide.html#caching-of-igblast-results-and-of-merged-reads>
for details. With the cache enabled, the tests run much faster.

Finally, run the tests with

    ./test.sh

This will create a directory named `testrun/`.
You will find all generated output in that directory.
