from igxplore import read_samples

configfile: "igxplore.yaml"

samples = read_samples("samples.tsv")
for sample in samples.values():
    print(sample)


rule all:
    input:
        expand("{name}/final/clonotypes.tsv", name=samples.keys())


rule igdiscover_init:
    output: "{name}/igdiscover.yaml"
    input:
        reads=lambda wildcards: f"reads/{samples[wildcards.name].reads}",
        database=config["database"]
    shell:
        "rmdir {wildcards.name}; "
        "igdiscover init"
        " --reads1={input.reads}"
        " --database={input.database}"
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
        members="{name}/final/clonotype-members.tsv",
    input: "{name}/final/filtered.tsv.gz"
    shell:
        "igdiscover"
        " clonotypes"
        " --members={output.members}"
        " {input}"
        " > {output.tsv}"
