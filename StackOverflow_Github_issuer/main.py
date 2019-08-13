# Library to Help interact with GitHub
from github import Github
import bs4
from requests import get, post

import sys
import os
import json
from time import sleep


# Log function
def l(msg):
    print("[*] " + str(msg))


if len(sys.argv) != 2:
    l("Usage: %s data.json" % (sys.argv[0]))
    exit(-1)

vuln_file_path = sys.argv[1]
if not os.path.isfile(vuln_file_path):
    l(vuln_file_path + " Doesn't exist!")
    exit(-1)

DELAY_SECONDS = 1

GITHUB_USERNAME = "GITHUB_USERNAME"
GITHUB_PASSWORD = "GITHUB_PASSWORD"

# Since github has a rate limit for it's API, We'll send 1 request per second only
# DELAY_SECONDS = int(os.getenv("DELAY_SECONDS"))

github_user = Github(GITHUB_USERNAME, GITHUB_PASSWORD)

from requests.auth import HTTPBasicAuth

# At this point we need to parse list of repositories with Title and Body for make an Issue about the vulnerability

l("Parsing issue list")
l("Start making issues")
with open(vuln_file_path) as vulnerability_repository_file:
    vulns_list = json.load(vulnerability_repository_file)

    for i, vuln_report in enumerate(vulns_list):

        owner_username = vuln_report['repo_name'].split('/')[0]
        repo_nameee = vuln_report['repo_name']
        print("Getting username")

        fullname = owner_username
        try:
            user = github_user.get_user(owner_username)
            if user.name:
                fullname = user.name
                print(fullname)
                print(user.name)
                print('-----')
        except Exception as e:
            print(e)
            pass

        survey_link = "https://docs.google.com/forms/d/e/1FAIpQLScyzcHYnBBzXxGmAJV09-qyyOJws7aMGJFmvsJUFX6xvMGvOA/viewform?entry.793621839=" + str(
            vuln_report['id'])

        part1 = """Dear %s, 
We are a group of Academic researchers. We are analyzing vulnerable C++ code snippets migrated from StackOverflow to GitHub. Our research will be published in Academic publications and will not be used in any Industrial application. 
We noted a vulnerable code snippet in your repository that was most likely copied from Stack Overflow. The vulnerability exists in this source code [file](%s) of your repository.

Please verify our report here with regards to the above vulnerability to assist you.
**[Link to report](%s)** with four questions for you related to the vulnerability (should not take more than 5 minutes to answer).

Here is a summary of the vulnerable code snippet:

Description:
===
%s  
""" % (fullname, vuln_report['github_link'], survey_link, vuln_report['vulndetails']['description'])

        part2 = ""
        part3 = ""

        if (vuln_report['vulndetails']['mitigations'].strip() != ""):
            part2 = """ 
Mitigation:
===
%s
        """ % vuln_report['vulndetails']['mitigations']

        if (vuln_report['vulndetails']["references"].strip() != ""):
            part3 = """
References:
===
%s
        
        """ % vuln_report['vulndetails']["references"]

        part4 = """
---
Please verify our report here with regards to the above vulnerability to assist you.
**[Link to report](%s)** with four questions for you related to the vulnerability (should not take more than 5 minutes to answer).

Sincerely yours,
[AUTHOR NAMES HAVE BEEN REMOVED]
""" % (survey_link)
        issue = part1 + part2 + part3 + part4
        open('ss%s.txt' % (i), 'w+').write(issue)

        try:
            repo = github_user.get_repo(repo_nameee)
            repo.create_issue(title="Academic research on vulnerable c++ code snippet", body=issue)
            l("Index[%d] Making Issue for sucessed: %s " % (i, repo_nameee))
            sleep(DELAY_SECONDS)
        except Exception as e:
            l("Index[%d] Making Issue for: %s  Failed !" % (i, repo_nameee))
            l(e)
            sleep(DELAY_SECONDS)

l("Done :)")
