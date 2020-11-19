import typer
from src import github, utils

app = typer.Typer()


@app.command()
def contributors(owner: str, repo: str, uname: str = ""):
    """Get contributors of a repo
    """
    typer.echo(github.find_contributors_from_repo(owner=owner, repo=repo, uname=uname))


@app.command()
def org(organisation: str, threads: int = 2, uname: str = ""):
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
def username(username: str, uname: str = ""):
    """Get email from username
    """
    typer.echo(github.find_email_from_username(username))


@app.command()
def repo(owner: str, repo: str, uname: str = ""):
    """
    returns email of contributors repo 
    """
    typer.echo(github.find_emails_from_repo(username=owner, repo=repo, uname=uname))


if __name__ == "__main__":
    app()
