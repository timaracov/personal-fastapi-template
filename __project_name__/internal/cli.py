import click


@click.group()
def cli():
    pass


@cli.command("create-admin")
def cli_command():
    pass

if __name__ == "__main__":
    cli()
