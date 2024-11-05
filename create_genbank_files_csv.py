#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script calls "find_with_recoll.py" to list all files with a ".gb" suffix
# (assumed to be genbank files).
#
# The script called "find_with_recoll.py" must be present in the cwd.
# It calls recoll (https://www.recoll.org) which must be installed.
#
# Only files that can be read by pydna.readers.read are included.
#
# Only files with a sequence length between minlen and maxlen are included.
#
# a file called genbank_files.csv is generated:
#
# name, seguid, path
#

import csv
from pathlib import Path
from subprocess import run
from pydna.readers import read
import tqdm

arg = Path("*.gb")

minlen = 80
maxlen = 30000

cp = run(["/usr/bin/python3", "recoll_search.py", str(arg)], capture_output=True, encoding="utf8")

paths = [Path(pth.removeprefix("file://")) for pth in cp.stdout.splitlines()]

paths = [p for p in paths if p.suffix == arg.suffix]

paths = [p for p in paths if p.exists() and not p.is_symlink()]

lols = []

log = []

for path in tqdm.tqdm(paths, position=0, leave=True):

    try:
        s = read(path)
    except ValueError as err:
        log.append(f"could not read {path}")
        log.append(str(err))
        continue

    if not minlen < len(s) < maxlen:
        continue

    try:
        code = s.seguid()
    except ValueError as err:
        log.append(f"could not make seguid for {path}")
        log.append(str(err))
        continue

    lols.append([path.name, s.seguid(), path])

lols.sort()

lols.insert(0, ["name", "seguid", "path"])

with open('genbank_files.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(lols)

print("\n".join(log))
