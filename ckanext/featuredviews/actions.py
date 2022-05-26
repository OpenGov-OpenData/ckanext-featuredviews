import logging
import ckan.model as model
import ckan.plugins.toolkit as tk

from ckan.plugins.toolkit import get_validator, ValidationError, asbool
from ckan.lib.dictization import table_dictize
from ckan.logic import NotFound
from ckanext.featuredviews import db

import ckan.lib.navl.dictization_functions as df

log = logging.getLogger(__name__)

try:
    unicode_safe = get_validator('unicode_safe')
except tk.UnknownValidator:
    # CKAN 2.7
    unicode_safe = unicode  # noqa: F821

schema = {
    'resource_view_id': [get_validator('not_empty'), unicode_safe],
    'package_id': [get_validator('ignore_empty'), unicode_safe],
    'canonical': [get_validator('boolean_validator'), unicode_safe],
    'homepage': [get_validator('boolean_validator'), unicode_safe]
}

schema_get = {
    'resource_view_id': [get_validator('not_empty'), unicode_safe]
}

def featured_create(context, data_dict):
    data, errors = df.validate(data_dict, schema, context)

    if errors:
        raise ValidationError(errors)

    featured = db.Featured()
    featured.resource_view_id = data['resource_view_id']
    featured.canonical = asbool(data.get('canonical', False))
    featured.homepage = asbool(data.get('homepage', False))

    resource_id = model.ResourceView.get(featured.resource_view_id).resource_id
    featured.package_id = model.Resource.get(resource_id).package_id

    featured.save()

    session = context['session']
    session.add(featured)
    session.commit()

    return table_dictize(featured, context)

def featured_show(context, data_dict):
    data, errors = df.validate(data_dict, schema_get, context)

    if errors:
        raise ValidationError(errors)

    featured = db.Featured.get(resource_view_id=data['resource_view_id'])
    if featured is None:
        raise NotFound()

    return table_dictize(featured, context)

def featured_upsert(context, data_dict):
    data, errors = df.validate(data_dict, schema, context)

    if errors:
        raise ValidationError(errors)

    featured = db.Featured.get(resource_view_id=data['resource_view_id'])
    if featured is None:
        featured = db.Featured()

    featured.resource_view_id = data['resource_view_id']

    if 'canonical' in data:
        featured.canonical = asbool(data['canonical'])

    if 'homepage' in data:
        featured.homepage = asbool(data['homepage'])

    resource_id = model.ResourceView.get(featured.resource_view_id).resource_id
    featured.package_id = model.Resource.get(resource_id).package_id

    featured.save()

    session = context['session']
    session.add(featured)
    session.commit()

    return table_dictize(featured, context)
