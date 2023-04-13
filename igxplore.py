from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple
from xopen import xopen

import pandas as pd


class ParseError(Exception):
    pass


@dataclass
class Experiment:
    name: str
    database: Path
    reads: Path
    is_paired: bool


def read_experiments(path) -> Tuple[Dict[str, Experiment], pd.DataFrame]:
    """
    Return a dict that maps an experiment name to an Experiment object
    """
    experiments = {}
    table = pd.read_table(path, sep="\t", comment="#")
    if list(table.columns)[:3] != ["id", "database", "reads"]:
        raise ParseError(
            f"The first three columns in {path} must be 'id', 'database' and 'reads'"
        )
    for row in table.itertuples():
        is_paired = "?" in row.reads
        experiment = Experiment(
            name=row.id, database=row.database.rstrip("/"), reads=row.reads, is_paired=is_paired
        )
        if row.id in experiments:
            raise ValueError(
                f"Experiment id {row.id} occurs twice in {path}, but it needs to be unique"
            )
        experiments[row.id] = experiment
    metadata = table.drop(columns=["database", "reads"])
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
    metadata_column_names = list(metadata.columns)
    header = True
    with xopen(output + ".tmp", mode="w") as f:
        for path, metadata in zip(input, metadata.itertuples(index=False)):
            table = pd.read_table(path)
            for i, column_name in enumerate(metadata_column_names):
                table.insert(i, column_name, getattr(metadata, column_name))
            f.write(table.to_csv(header=header, index=False, sep="\t"))
            header = False
    os.rename(output + ".tmp", output)
