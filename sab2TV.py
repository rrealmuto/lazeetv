import sys
from nzb import NZB
from db import TVDatabaseManager

print len(sys.argv)
for arg in sys.argv:
    print arg

result_dir = sys.argv[1]
nzb_name = sys.argv[2]
nzb_name_clean = sys.argv[3]
newzbin_id = sys.argv[4]
category = sys.argv[5]
group = sys.argv[6]
status = sys.argv[7]

myDB = TVDatabaseManager()
nzb = myDB.getNZB(nzb_name)
if nzb:
    nzb.status = status
    nzb.save()