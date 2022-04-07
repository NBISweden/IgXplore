from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

import pandas as pd


class ParseError(Exception):
    pass


@dataclass
class Sample:
    name: str
    database: Path
    reads: Path


def read_samples(path) -> Dict[str, Sample]:
    """
    Return a dict that maps a sample name to a Sample object
    """
    samples = {}
    table = pd.read_table(path, sep="\t", comment="#")
    if list(table.columns)[:3] != ["name", "database", "r1"]:
        raise ParseError(
            f"The first three columns in {path} must be 'name', 'database' and 'r1'"
        )
    for row in table.itertuples():
        sample = Sample(name=row.name, database=row.database, reads=row.r1)
        samples[row.name] = sample
    return samples


def merge_tables(input: Iterable[str], output: str, samples: Iterable[str]):
    """
    Merge table files given in *input* and write them to *output*.
    Add a sample_id column.
    """
    tables = []
    for path, name in zip(input, samples):
        table = pd.read_table(path)
        table.insert(0, "sample_id", name)
        tables.append(table)
    pd.concat(tables).to_csv(output, index=False, sep="\t")
