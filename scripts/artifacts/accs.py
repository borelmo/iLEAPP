import os
import plistlib
import sqlite3

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, is_platform_windows 


def get_accs(files_found, report_folder, seeker):
    file_found = str(files_found[0])
    db = sqlite3.connect(file_found)
    cursor = db.cursor()
    cursor.execute(
        """
		SELECT
		ZACCOUNTTYPEDESCRIPTION,
		ZUSERNAME,
		DATETIME(ZDATE+978307200,'UNIXEPOCH','UTC' ) AS 'ZDATE TIMESTAMP',
		ZACCOUNTDESCRIPTION,
		ZACCOUNT.ZIDENTIFIER,
		ZACCOUNT.ZOWNINGBUNDLEID
		FROM ZACCOUNT
		JOIN ZACCOUNTTYPE ON ZACCOUNTTYPE.Z_PK=ZACCOUNT.ZACCOUNTTYPE
		ORDER BY ZACCOUNTTYPEDESCRIPTION
		"""
    )

    all_rows = cursor.fetchall()
    usageentries = len(all_rows)
    if usageentries > 0:
        data_list = []
        for row in all_rows:
            data_list.append((row[0],row[1],row[2],row[3],row[4],row[5]))                
        report = ArtifactHtmlReport('Account Data')
        report.start_artifact_report(report_folder, 'Account Data')
        report.add_script()
        data_headers = ('Account Desc.','Username','Timestamp','Description','Identifier','Bundle ID' )     
        report.write_artifact_data_table(data_headers, data_list, file_found)
        report.end_artifact_report()

    else:
        logfunc("No Account Data available")

