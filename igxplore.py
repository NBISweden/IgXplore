from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterable, Dict


class ParseError(Exception):
    pass


def read_tsv(path, columns: int) -> Iterable[List[str]]:
    """
    Read a tab-separated value file from path, allowing "#"-prefixed comments

    Yield a list of fields for every row (ignoring comments and empty lines)

    If the number of fields in a row does not match *columns*, a ParseError
    is raised.
    """
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            fields = line.strip().split()
            if len(fields) != columns:
                raise ParseError(
                    f"Expected {columns} tab-separated fields in {path}, but found {len(fields)}")
            yield fields


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
    for name, database, reads in read_tsv(path, columns=3):
        samples[name] = Sample(name=name, database=database, reads=reads)
    return samples
