import typer
from src import github, utils
from typing import Optional

app = typer.Typer()


@app.command()
def contributors(owner: str, repo: str, uname: Optional[str] = typer.Argument(None)):
    """Get contributors of a repo
    """
    typer.echo(github.find_contributors_from_repo(owner=owner, repo=repo, uname=uname))


@app.command()
def org(
    organisation: str, threads: int = 2, uname: Optional[str] = typer.Argument(None)
):
    """Get list of users of an Organisation
    """
    usernames = github.find_users_from_organisation(
        organisation=organisation, uname=uname
    )
    result = []
    for username in usernames:
        result.append(github.find_email_from_username(username=username))
    typer.echo(result)


@app.command()
def username(username: str, uname: Optional[str] = typer.Argument(None)):
    """Get email from username
    """
    typer.echo(github.find_email_from_username(username))


@app.command()
def repo(owner: str, repo: str, uname: Optional[str] = typer.Argument(None)):
    """
    returns email of contributors repo 
    """
    typer.echo(github.find_emails_from_repo(username=owner, repo=repo, uname=uname))


@app.command()
def stargazzers(
    owner: str,
    repo: str,
    info: bool = False,
    uname: Optional[str] = typer.Argument(None),
):
    """
    returns list of people who starred this repo
    --info to get info of user
    """
    usernames = github.find_stargazzers_from_repo(owner=owner, repo=repo, uname=uname)
    results = []
    for username in usernames:
        results.append(github.find_email_from_username(username=username))
    if not info:
        return typer.echo(results)

    typer.echo(utils.get_info_for_usernames(results=results, uname=uname))


@app.command()
def info(username: str, uname: Optional[str] = typer.Argument(None)):
    typer.echo(github.get_profile_info_from_user(username=username, uname=uname))


if __name__ == "__main__":
    app()
