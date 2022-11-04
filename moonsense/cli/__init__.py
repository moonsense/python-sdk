import click
from .download import run_download

@click.group()
def main():
    pass

@click.command()
@click.option('--until', help='The date in YYYY-MM-DD format until the data should be included')
@click.option('--since', help='The date in YYYY-MM-DD format since data should be included')
@click.option('--output', help='Output folder where to download data. Defaults to $PWD/data')
@click.option('--label', '-l', multiple=True, help='Filter downloaded sessions by provided labels')
@click.option('--platform', '-p', multiple=True, help='Filter downloaded sessions by platform: web,\
              ios, android. Leave this empty for all platforms')
@click.option('--with-group-id', default=False, help='If true, the folder structure uses includes the \
              client session group id')
def download(until, since, output, label, platform, with_group_id):
    run_download(output, until, since, label, platform, with_group_id)

main.add_command(download)

if __name__ == '__main__':
    main()
