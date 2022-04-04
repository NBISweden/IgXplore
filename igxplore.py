from dataclasses import dataclass
from pathlib import Path
from typing import Dict

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
