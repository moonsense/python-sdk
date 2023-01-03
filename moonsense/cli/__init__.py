import click
from .download import run_download

@click.group()
def main():
    pass

@click.command()
@click.option('--until', help='The date in YYYY-MM-DD format until the data should be included')
@click.option('--since', help='The date in YYYY-MM-DD format since data should be included')
@click.option('--output', help='Output folder where to download data. Defaults to $PWD/data')
@click.option('--skip-days', multiple=True, help='Skip downloading data for the provided days.')
@click.option('--incremental', default=True, help='If true, only download data that is not already \
              downloaded. If false, download all data')
@click.option('--label', '-l', multiple=True, help='Filter downloaded sessions by provided labels')
@click.option('--platform', '-p', multiple=True, help='Filter downloaded sessions by platform: web,\
              ios, android. Leave this empty for all platforms')
@click.option('--with-journey-id', default=False, help='If true, the folder structure uses includes the \
              journey id')
@click.option("--verbose", is_flag=True, show_default=True, default=False, \
              help="Turn on more verbose logging.")
def download(until, since, output, skip_days, incremental, label, platform, with_journey_id, verbose):
    run_download(output, until, since, skip_days, incremental, label, platform, with_journey_id, verbose)

main.add_command(download)

if __name__ == '__main__':
    main()
