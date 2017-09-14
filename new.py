import re

from github import Github

RELEASE_NOTES_MIN_LENGTH = 10
PULL_REQUEST_PATTERN = re.compile(
    '\*\*Задача\*\*:(.*)\*\*Коротко для Release Notes, в формате «Сделали/Добавили/Исправили N»\*\*:(.*)\*\*Описание\*',
    re.MULTILINE | re.DOTALL)

GITHUB_USERNAME = ''
GITHUB_PASSWORD = ''
GITHUB_REPO = 'bioinf/edy'


def get_issues(username, password, repo_name):
    stepik_repo = Github(username, password).get_repo(repo_name)
    upcoming_milestone = stepik_repo.get_milestones()[0]

    return stepik_repo.get_issues(state='closed', milestone=upcoming_milestone)


def get_release_note(issue, issue_pattern):
    search = issue_pattern.search(issue.body)

    if search:
        yt_issue = search.group(1).strip()
        release_notes = search.group(2).strip()
    else:
        print('Failed to parse', issue.pull_request.html_url, issue.body)
        yt_issue = '!!!!!!YouTrack issue!!!!!!'
        release_notes = '?????Release notes?????'

    if len(release_notes) < RELEASE_NOTES_MIN_LENGTH:
        return

    return '1. [#{}]({}) ({}) {}\n'.format(issue.number, issue.pull_request.html_url, yt_issue, release_notes)


output_file = open('result.txt', 'w')
closed_issues = get_issues(GITHUB_USERNAME, GITHUB_PASSWORD, GITHUB_REPO)

for issue in closed_issues:
    rn = get_release_note(issue, PULL_REQUEST_PATTERN)

    if rn:
        output_file.write(rn)
