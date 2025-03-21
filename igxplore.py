import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import dnaio
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
    from row n of the *metadata* table) and write a merged table to
    *output*.
    """
    prev_header = None
    tmp_path = "tmp-merge-" + output
    with xopen(tmp_path, mode="w", compresslevel=3) as f:
        for path, metadata_row in zip(input, metadata.itertuples(index=False)):
            print("Processing", path, file=sys.stderr)
            # Read first 100 rows with Pandas to catch any obvious formatting
            # problems
            _ = pd.read_table(path, nrows=100)

            prefix = "\t".join(str(m) for m in metadata_row)
            with xopen(path) as infile:
                input_header = infile.readline()
                if prev_header:
                    if prev_header != input_header:
                        raise ValueError("Headers different")
                else:
                    header_prefix = metadata[:0].to_csv(index=False, sep="\t").rstrip("\n")
                    f.write(header_prefix + "\t")
                    f.write(input_header)
                    prev_header = input_header

                for line in infile:
                    print(prefix, line, file=f, sep="\t", end="")

    os.rename(tmp_path, output)


def fail_if_databases_inconsistent(experiments: Iterable[Experiment], gene: str):
    db = {}
    sequences = {}
    inconsistent_message = "Databases use inconsistent nomenclature. "\
                        "Please fix the problems below and re-run IgXplore"
    error = False
    database_paths = set(experiment.database for experiment in experiments)
    for db_path in database_paths:
        path = Path(db_path) / f"{gene}.fasta"
        for record_id, sequence in read_database(path).items():
            if record_id not in db:
                db[record_id] = (sequence, path)
            elif db[record_id][0] != sequence:
                if not error:
                    print(inconsistent_message, file=sys.stderr)
                print(
                    f"- Record with name '{record_id}' exists "
                    f"in both '{path}' and '{db[record_id][1]}', but the "
                    "sequences are different", file=sys.stderr
                )
                error = True

            if sequence not in sequences:
                sequences[sequence] = (record_id, path)
            elif sequences[sequence][0] != record_id:
                if not error:
                    print(inconsistent_message, file=sys.stderr)
                print(
                    f"- Record '{record_id}' in '{path}' and "
                    f"record '{sequences[sequence][0]}' in "
                    f"'{sequences[sequence][1]}' contain the same sequence, but "
                    "different names",
                    file=sys.stderr
                )
                error = True
    if error:
        raise ValueError("Databases inconsistent")


def read_database(path: Path) -> Dict[str, str]:
    db = {}
    sequences = {}
    with dnaio.open(path) as f:
        for record in f:
            record_id = record.name.split()[0]
            if record_id in db:
                raise KeyError(f"Record with id '{record_id}' found twice in '{path}'")
            if record.sequence in sequences:
                raise KeyError(
                    f"Record '{record_id}' has the same sequence as record"
                    f"'{sequences[record.sequence]}'"
                )
            db[record_id] = record.sequence
            sequences[record.sequence] = record_id

    return db
