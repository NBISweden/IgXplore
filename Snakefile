from igxplore import read_experiments, add_metadata_and_merge_tables

configfile: "igxplore.yaml"

experiments, metadata = read_experiments("experiments.tsv")
for experiment in experiments.values():
    print(experiment)


rule all:
    input:
        "report.html", "filtered.tsv.gz"


rule igdiscover_init:
    output: "{name}/igdiscover.yaml"
    input:
        reads=lambda wildcards: f"reads/{experiments[wildcards.name].reads}".replace("?", "1"),
        reads2=lambda wildcards: f"reads/{experiments[wildcards.name].reads}".replace("?", "2") if experiments[wildcards.name].is_paired else [],
        database=lambda wildcards: expand(f"{experiments[wildcards.name].database}/{{gene}}.fasta", gene=("V", "D", "J"))
    params:
        database_dir=lambda wildcards: f"{experiments[wildcards.name].database}",
        reads_arg=lambda wildcards: f"reads1" if experiments[wildcards.name].is_paired else "single-reads"
    shell:
        "rmdir {wildcards.name}; "  # Created by Snakemake
        "igdiscover init"
        " --{params.reads_arg}={input.reads}"
        " --database={params.database_dir}"
        " {wildcards.name}; "
        "igdiscover config"
        " --file {wildcards.name}/igdiscover.yaml"
        " --set iterations 0"
        " --set barcode_length_5prime {config[umi_length_5prime]}"
        " --set barcode_length_3prime {config[umi_length_3prime]}"


rule igdiscover_run:
    output: "{name}/final/filtered.tsv.gz"
    input: "{name}/igdiscover.yaml"
    shell:
        "cd {wildcards.name}; "
        "igdiscover run final/filtered.tsv.gz"


rule igdiscover_clonotypes:
    output:
        tsv="{name}/final/clonotypes.tsv",
        clustered="{name}/final/clustered.tsv",
    input: "{name}/final/filtered.tsv.gz"
    shell:
        "igdiscover"
        " clonotypes"
        " --clustered={output.clustered}"
        " {input}"
        " > {output.tsv}"


rule merge_filtered_tables:
    output:
        tsv="filtered.tsv.gz"
    input:
        expand("{name}/final/filtered.tsv.gz", name=experiments.keys())
    run:
        add_metadata_and_merge_tables(input, output.tsv, metadata)


rule merge_clonotype_tables:
    output:
        tsv="clonotypes.tsv"
    input:
        expand("{name}/final/clonotypes.tsv", name=experiments.keys())
    run:
        add_metadata_and_merge_tables(input, output.tsv, metadata)


rule report:
    output: "report.html"
    input: "clonotypes.tsv", "filtered.tsv.gz"
    script: "scripts/report.Rmd"
