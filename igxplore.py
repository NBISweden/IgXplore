from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd


class ParseError(Exception):
    pass


@dataclass
class Sample:
    name: str
    database: Path
    reads: Path


def read_samples(path) -> Tuple[Dict[str, Sample], pd.DataFrame]:
    """
    Return a dict that maps a sample name to a Sample object
    """
    samples = {}
    table = pd.read_table(path, sep="\t", comment="#")
    if list(table.columns)[:3] != ["sample_id", "database", "r1"]:
        raise ParseError(
            f"The first three columns in {path} must be 'sample_id', 'database' and 'r1'"
        )
    for row in table.itertuples():
        sample = Sample(name=row.sample_id, database=row.database, reads=row.r1)
        samples[row.sample_id] = sample
    metadata = table.drop(columns=["database", "r1"])
    return samples, metadata


def add_metadata_and_merge_tables(input: Iterable[str], output: str, metadata: pd.DataFrame):
    """
    Read table files from the paths in the *input* iterable,
    augment them with metadata (input file n is augmented with metadata
    from row n of the *metadata* table),
    then merge the tables and write them to the *output*.
    """
    tables = []
    metadata_column_names = list(metadata.columns)
    for path, metadata in zip(input, metadata.itertuples(index=False)):
        table = pd.read_table(path)
        for i, column_name in enumerate(metadata_column_names):
            table.insert(i, column_name, getattr(metadata, column_name))
        tables.append(table)
    pd.concat(tables).to_csv(output, index=False, sep="\t")
