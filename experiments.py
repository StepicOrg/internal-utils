import re

from github import Github

# First create a Github instance:
g = Github()

# Then play with your Github objects:
user = g.get_user()


def save_pull(issue):
    search = pattern.search(issue.body)
    if search:
        yt_issue = search.group(1).strip()
    else:
        print('Failed to parse', issue.pull_request.html_url, issue.body)
        yt_issue = '!!!!!!'

    out.write('1. [#{}]({})  ({})'.format(issue.number, issue.pull_request.html_url, yt_issue))
    out.write('\n')
    out.write('-------------------------------------------\n')
    if issue.assignee and issue.assignee.name:
        out.write(issue.assignee.name)
        out.write('\n')
    out.write(issue.title)
    out.write('\n')
    out.write('-------------------------------------------\n')
    out.write(issue.body)
    out.write('\n')
    out.write('-------------------------------------------\n')


stepik_repo = g.get_repo("bioinf/edy")
milestone = stepik_repo.get_milestone(38)

# Issue:
#  body - description
#  number - pull request id
#  pull_request.html_url - pull request url (https://github.com/bioinf/edy/pull/1039)

all_closed = stepik_repo.get_issues(state='closed', milestone=milestone)

pattern = re.compile('Solves issue\(s\)\*\*:(.*)\*\*Description', re.MULTILINE | re.DOTALL)

out = open('result.txt', 'w')

for _ in all_closed:
    save_pull(_)
