import re
from typing import List

from requests import get
from requests.auth import HTTPBasicAuth

HTTP_SUCCESS = 200


def find_contributors_from_repo(owner: str, repo: str, uname: str = "") -> List[str]:
    """Contributors for a repo

    >>> find_contributors_from_repo(owner = "gauthamzz", repo = "maker")
    ['gauthamzz']
    """
    response = get(
        f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    contributors = re.findall(r'https://github\.com/(.*?)"', response)
    return contributors


def find_repos_from_owner(owner: str, uname: str = "") -> List[str]:
    """Gets list of repos owned by user

    >>> find_repos_from_owner(owner="featuremonkey")
    []
    """
    response = get(
        f"https://api.github.com/users/{owner}/repos?per_page=100&sort=pushed",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % owner, response)
    nonForkedRepos = []
    for repo in repos:
        if repo[1] == "false":
            nonForkedRepos.append(repo[0])
    return nonForkedRepos


def find_email_from_contributor(
    username: str, repo: str, contributor: str, breach: bool = False, uname: str = ""
) -> str:
    """
    >>> find_email_from_contributor("tiangolo", "typer", "tiangolo", True)
    'tiangolo@gmail.com'
    """
    response = get(
        f"https://github.com/{username}/{repo}/commits?author={contributor}",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
    if latestCommit:
        latestCommit = latestCommit.group(1)
    else:
        latestCommit = "dummy"
    commitDetails = get(
        f"https://github.com/{username}/{repo}/commit/{latestCommit}.patch",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    email = re.search(r"<(.*)>", commitDetails)
    if email:
        email = email.group(1)
        if breach:
            if (
                get(
                    f"https://haveibeenpwned.com/api/v2/breachedaccount/{email}"
                ).status_code
                == HTTP_SUCCESS
            ):
                email = f"{email}[pwned]"
    return email


def find_email_from_username(username: str, uname: str = "") -> str:
    """
    >>> find_email_from_username("gauthamzz")
    'gauthamzz : thabeatsz@gmail.com'
    """
    repos = find_repos_from_owner(owner=username)
    for repo in repos:
        email = find_email_from_contributor(
            username=username, repo=repo, contributor=username, uname=uname
        )
        if email:
            return username + " : " + email


def find_emails_from_repo(username: str, repo: str, uname: str = ""):
    """
    >>> find_emails_from_repo("gauthamzz", "maker")
    {'gauthamzz': 'thabeatsz@gmail.com'}
    """
    user_emails = {}
    contributors = find_contributors_from_repo(owner=username, repo=repo)
    for contributor in contributors:
        email = find_email_from_contributor(
            username=username, repo=repo, contributor=contributor, uname=uname
        )
        if email:
            user_emails[contributor] = email
    return user_emails


def find_users_from_organisation(organisation: str, uname: str = ""):
    """
    >>> find_users_from_organisation("anna-assistant")
    ['gauthamzz', 'srvkmr130', 'yasharmaster']
    """
    response = get(
        f"https://api.github.com/orgs/{organisation}/members?per_page=100",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    members = re.findall(r'"login":"(.*?)"', response)
    return members


def find_stargazzers_from_repo(owner: str, repo: str, uname: str = "") -> List[str]:
    """
    >>> find_stargazzers_from_repo("gauthamzz", "hazel")
    ['mubaris', 'AviBomb', 'SOHELAHMED7', 'ananya', 'todun', 'klonggan', 'x0rzkov', 'aryan-harsh', 'shalusinha1411']
    """
    response = get(
        f"https://api.github.com/repos/{owner}/{repo}/stargazers?per_page=100",
        auth=HTTPBasicAuth(uname, ""),
    ).text
    contributors = re.findall(r'https://github\.com/(.*?)"', response)
    return contributors



