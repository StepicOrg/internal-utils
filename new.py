import re

from github import Github

RELEASE_NOTES_MIN_LENGTH = 10
PULL_REQUEST_PATTERN = re.compile(
   # '\*\*Задача\*\*:(?P<issues>.*)\[(?P<is_public>[\s|x])\] рассказать пользователям(.*)\*\*Коротко для Release Notes, в формате «Сделали/Добавили/Исправили N»\*\*:(?P<rn_text>.*)\*\*Описание\*\*:',
   '\*\*Задача\*\*:(?P<issues>.*)\s\-\s\[(?P<is_public>.*)\] рассказать пользователям(.*)\*\*Коротко для Release Notes, в формате «Сделали/Добавили/Исправили N»\*\*:(?P<rn_text>.*)\*\*Описание\*\*:',
    re.MULTILINE | re.DOTALL)

GITHUB_ACCESS_TOKEN = ''
GITHUB_REPO = 'bioinf/edy'


def get_issues(access_token, repo_name):
    stepik_repo = Github(access_token).get_repo(repo_name)
    print(list(stepik_repo.get_milestones()))
    upcoming_milestone = stepik_repo.get_milestone(150)
    return stepik_repo.get_issues(state='closed', milestone=upcoming_milestone)


def get_release_note(issue, issue_pattern):
    search = issue_pattern.search(issue.body)

    if search:
        yt_issue = search.group('issues').strip()
        release_notes = search.group('rn_text').strip()
        is_public = bool(search.group('is_public').strip())
    else:
        print('Failed to parse', issue.pull_request.html_url, issue.body)
        yt_issue = '!!!!!!YouTrack issue!!!!!!'
        release_notes = '?????Release notes?????'
        is_public = False

    if len(release_notes) < RELEASE_NOTES_MIN_LENGTH:
        return

    return '1. [#{}]({}){} ({}) {}\n'.format(issue.number,
                                             issue.pull_request.html_url,
                                             '🔥' if is_public else '',  yt_issue, release_notes)


output_file = open('result.txt', 'w')
closed_issues = get_issues(GITHUB_ACCESS_TOKEN, GITHUB_REPO)

for issue in closed_issues:
    rn = get_release_note(issue, PULL_REQUEST_PATTERN)

    if rn:
        output_file.write(rn)
    else:
        print('Skip pr:', issue.pull_request.html_url, issue.body)
