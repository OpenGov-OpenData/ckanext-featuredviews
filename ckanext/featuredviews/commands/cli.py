import click
from ckanext.featuredviews.db import setup as model_setup

# Click commands for CKAN 2.9 and above


@click.group()
def featuredviews():
    '''
    featuredviews commands
    '''
    pass


@featuredviews.command()
def migrate():
    '''
    featuredviews migrate
    '''
    model_setup()


def get_commands():
    return [featuredviews]
