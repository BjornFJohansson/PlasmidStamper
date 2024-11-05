#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script lists all files in gb_files.csv for which one name is associated with 
# more than one 


import csv
from pathlib import Path
from subprocess import run
from pydna.readers import read
import tqdm
from pydna.utils import smallest_rotation, rc
from Bio.SeqUtils.CheckSum import seguid
import os
from itertools import groupby
from collections import defaultdict

csums = defaultdict(set)
paths = defaultdict(list)

with open('genbank_files.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
       name, seguid, path = row
       csums[name].add(seguid)
       paths[seguid].append(path)

names_with_more_than_one_code = [k for k,v in csums.items() if len(v)>1]

names_with_more_than_one_code.remove("pGeneX.gb")
names_with_more_than_one_code.remove("pUCmuT7pt.gb")
names_with_more_than_one_code.remove("sequence.gb")

names_with_more_than_one_code.sort()

print(len(names_with_more_than_one_code))

for name in names_with_more_than_one_code:
    print(name)
    seguids = csums[name]
    for seguid in seguids:
        print(seguid, len(paths[seguid]))
