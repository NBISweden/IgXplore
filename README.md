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


## Running the tests

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
