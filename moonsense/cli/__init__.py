import click
from download import run_download

@click.group()
def main():
    pass

@click.command()
@click.option('--until', help='The date in YYYY-MM-DD format until the data should be included')
@click.option('--since', help='The date in YYYY-MM-DD format since data should be included')
@click.option('--label', '-l', multiple=True, help='Labels to filter sessions by')
def download_cmd():
    click.echo('Download')

main.add_command(download_cmd)

if __name__ == '__main__':
    main()