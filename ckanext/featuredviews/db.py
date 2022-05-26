import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from ckan.model.meta import metadata,  mapper, Session
from ckan.model.types import make_uuid

import logging
log = logging.getLogger(__name__)


featured_table = None


def setup():
    if featured_table is None:
        define_featured_table()
        log.debug('FeaturedViews table defined in memory')

    if not featured_table.exists():
        featured_table.create()
        log.debug('FeaturedViews table created')
    else:
        log.debug('FeaturedViews table already exist')


class Featured(model.DomainObject):
    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).first()

    @classmethod
    def find(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw)


def define_featured_table():
    global featured_table

    featured_table = Table(
        'featured',
        metadata,
        Column('resource_view_id', types.UnicodeText, primary_key=True),
        Column('package_id', types.UnicodeText),
        Column('canonical', types.Boolean),
        Column('homepage', types.Boolean)
    )

    mapper(Featured, featured_table)
