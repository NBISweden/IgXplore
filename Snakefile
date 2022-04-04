from igxplore import read_samples

configfile: "igxplore.yaml"

samples = read_samples("samples.tsv")
for sample in samples:
    print(sample)
