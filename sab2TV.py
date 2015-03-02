import sys
from nzb import NZB
from db import TVDatabaseManager

# print len(sys.argv)
# for arg in sys.argv:
#     print arg
SAB_STATUS_SUCCESS = 0
SAB_STATUS_FAILEDVERIFY = 1
SAB_STATUS_FAILEDUNPACK = 2
SAB_STATUS_PPFAILED = 3
SAB_STATUS_FAILEDDOWNLOAD = -1

result_dir = sys.argv[1]
nzb_name = sys.argv[2]
nzb_name_clean = sys.argv[3]
newzbin_id = sys.argv[4]
category = sys.argv[5]
group = sys.argv[6]
status = int(sys.argv[7])

myDB = TVDatabaseManager()
nzb = myDB.getNZB(nzb_name_clean)
print "Status is: " + str(status)
if nzb:
    ep = nzb.getEpisode()
    if status == SAB_STATUS_SUCCESS:
        print "SAB reported success!"
        nzb.status = NZB.NZB_STATUS_SUCCESS
    else:
        print "SAB reported an error!"
        nzb.status = NZB.NZB_STATUS_FAIL
    ep.status = nzb.status
    ep.save()
    nzb.save()
    if ep.status != nzb.NZB_STATUS_SUCCESS:
        print "NZB Failed! Going to try to find another..."
        ep.startDownloading()
    print "Done"
else:
    print "Couldn't find NZB in database"