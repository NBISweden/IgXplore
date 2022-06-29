from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import pandas as pd


class ParseError(Exception):
    pass


@dataclass
class Experiment:
    name: str
    database: Path
    reads: Path


def read_experiments(path) -> Tuple[Dict[str, Experiment], pd.DataFrame]:
    """
    Return a dict that maps an experiment name to an Experiment object
    """
    experiments = {}
    table = pd.read_table(path, sep="\t", comment="#")
    if list(table.columns)[:3] != ["id", "database", "r1"]:
        raise ParseError(
            f"The first three columns in {path} must be 'id', 'database' and 'r1'"
        )
    for row in table.itertuples():
        experiment = Experiment(
            name=row.id, database=row.database.rstrip("/"), reads=row.r1
        )
        if row.id in experiments:
            raise ValueError(
                f"Experiment id {row.id} occurs twice in {path}, but it needs to be unique"
            )
        experiments[row.id] = experiment
    metadata = table.drop(columns=["database", "r1"])
    return experiments, metadata


def add_metadata_and_merge_tables(
    input: Iterable[str], output: str, metadata: pd.DataFrame
):
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
