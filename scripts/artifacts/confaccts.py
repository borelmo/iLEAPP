import os
import plistlib
import sqlite3

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, is_platform_windows 


def get_confaccts(files_found, report_folder, seeker):
    data_list = []
    file_found = str(files_found[0])
    with open(file_found, "rb") as fp:
        pl = plistlib.load(fp)
        for key, val in pl.items():
            data_list.append((key, val))
    
    report = ArtifactHtmlReport('Account Configuration')
    report.start_artifact_report(report_folder, 'Account Configuration')
    report.add_script()
    data_headers = ('Key','Values' )     
    report.write_artifact_data_table(data_headers, data_list, file_found)
    report.end_artifact_report()
            
    
