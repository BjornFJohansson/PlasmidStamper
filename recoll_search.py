#!/usr/bin/python3

import sys
from recoll import recoll

scriptname, queryfn = sys.argv
db = recoll.connect()
query = db.query()
nres = query.execute(f"filename:{queryfn}")
results = query.fetchmany(1_000_000)
for doc in results:
    print(doc.url)


# This produces a list with rows like these in stdout:
#
# file:///home/bjorn/myvault/files/ongoing-work/pTA flexible backbone/amp/pBR322.gb
# file:///home/bjorn/myvault/files/ongoing-work/ProjectBCKADH/pTA1.gb
# ...

# This script is called by genbank_file_create_list.py
