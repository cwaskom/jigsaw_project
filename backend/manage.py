import sys
from flask.cli import FlaskGroup
from api.src import create_app
from run_adapters import RequestAndBuild
import click

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('build_hotels')
def build_hotels():
    runner = RequestAndBuild()
    runner.run()

if __name__ == '__main__':
    cli()
