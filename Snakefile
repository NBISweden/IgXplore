from igxplore import read_samples

configfile: "igxplore.yaml"

samples = read_samples("samples.tsv")
for sample in samples.values():
    print(sample)


rule all:
    input: expand("{name}/igdiscover.yaml", name=samples.keys())


rule igdiscover_init:
    output: "{name}/igdiscover.yaml"
    input:
        reads=lambda wildcards: f"reads/{samples[wildcards.name].reads}",
        database=config["database"]
    shell:
        "rmdir {wildcards.name}"
        " && "
        "igdiscover init"
        " --reads1={input.reads}"
        " --database={input.database}"
        " {wildcards.name}"
