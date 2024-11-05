#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os

from pydna.readers import read

blacklist = "pGeneX.gb", "sequence.gb"

stamp = False
minlen = 80
maxlen = 30000

with open('gb_files.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Ignore first line in csv file
    for row in reader:
        name, seguid, path = row
        try:
            s = read(path)
        except ValueError:
            print("could not read", path)
            print()
            continue

        if name in blacklist:  # ignore these file names
            continue

        if s.annotations.get("comment") and seguid in s.annotations.get("comment"):  # ignore file if already stamped
            continue

        if not minlen < len(s) < maxlen:  # ignore file if sequence length not witin minlen, maxlen
            continue

        print(name)

        if not stamp:  # Set boolean variable stamp to True above to stamp files
            continue

        try:
            code = s.stamp()  # The Pydna.dseqrecord.stamp() method adds the seguid for the sequence.
        except ValueError:
            print("could not stamp", path)
            print()
        else:
            stat = os.stat(path)
            s.write(path)
            os.utime(path, times=(stat.st_atime, stat.st_mtime))
