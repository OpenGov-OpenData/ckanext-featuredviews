import pytest
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckan.tests import helpers, factories

from ckanext.featuredviews.db import Featured


@pytest.mark.usefixtures('clean_db', 'featuredviews_setup', 'clean_session')
class TestCreateFeaturedViews(object):
    def test_featured_create_no_args(self):
        '''
        Calling featured_create without args raises ValidationError.
        '''
        sysadmin = factories.Sysadmin()
        context = {
            'user': sysadmin['name']
        }

        # no featuredviews exist
        assert model.Session.query(Featured).count() == 0

        with pytest.raises(toolkit.ValidationError):
            helpers.call_action(
                'featured_create', context=context,
            )

        # no featuredviews created
        assert model.Session.query(Featured).count() == 0

    def test_featured_create_with_args(self):
        '''
        Calling featured_create with a resource view id creates a featured view
        '''
        sysadmin = factories.Sysadmin()
        dataset = factories.Dataset()
        resource = factories.Resource(
            package_id=dataset['id'],
            format='png'
        )
        resource_view = factories.ResourceView(
            resource_id=resource['id'],
            image_url='http://some.image.png'
        )
        context = {
            'user': sysadmin['name']
        }

        # no featuredviews exist
        assert model.Session.query(Featured).count() == 0

        featuredview_dict = helpers.call_action(
            'featured_create',
            context=context,
            resource_view_id=resource_view['id'],
            canonical=True,
            homepage=False
        )

        # a featuredview created
        assert model.Session.query(Featured).count() == 1
        assert featuredview_dict.get('resource_view_id') == resource_view['id']
        assert featuredview_dict.get('package_id') == dataset['id']
        assert featuredview_dict.get('canonical') == True
        assert featuredview_dict.get('homepage') == False


@pytest.mark.usefixtures('clean_db', 'featuredviews_setup', 'clean_session')
class TestUpsertFeaturedViews(object):
    def test_featured_upsert_no_args(self):
        '''
        Calling featured_upsert without args raises ValidationError.
        '''
        sysadmin = factories.Sysadmin()
        context = {
            'user': sysadmin['name']
        }

        # no featuredviews exist
        assert model.Session.query(Featured).count() == 0

        with pytest.raises(toolkit.ValidationError):
            helpers.call_action(
                'featured_upsert', context=context,
            )

        # no featuredviews created
        assert model.Session.query(Featured).count() == 0

    def test_featured_upsert_with_args(self):
        '''
        Calling featured_upsert with a resource view id creates a featured view
        '''
        sysadmin = factories.Sysadmin()
        dataset = factories.Dataset()
        resource = factories.Resource(
            package_id=dataset['id'],
            format='png'
        )
        resource_view = factories.ResourceView(
            resource_id=resource['id'],
            image_url='http://some.image.png'
        )
        context = {
            'user': sysadmin['name']
        }

        featuredview_dict_1 = helpers.call_action(
            'featured_upsert',
            context=context,
            resource_view_id=resource_view['id'],
            canonical=False,
            homepage=True
        )

        # a featuredview created
        assert featuredview_dict_1.get('resource_view_id') == resource_view['id']
        assert featuredview_dict_1.get('package_id') == dataset['id']
        assert featuredview_dict_1.get('canonical') == False
        assert featuredview_dict_1.get('homepage') == True

        featuredview_dict_2 = helpers.call_action(
            'featured_upsert',
            context=context,
            resource_view_id=resource_view['id'],
            canonical=True,
            homepage=False
        )

        # update a featuredview
        assert featuredview_dict_2.get('resource_view_id') == resource_view['id']
        assert featuredview_dict_2.get('package_id') == dataset['id']
        assert featuredview_dict_2.get('canonical') == True
        assert featuredview_dict_2.get('homepage') == False


@pytest.mark.usefixtures('clean_db', 'featuredviews_setup', 'clean_session')
class TestShowFeaturedViews(object):
    def test_featured_show_not_found(self):
        '''
        Calling featured_show without any saved featuredviews
        '''
        sysadmin = factories.Sysadmin()
        context = {
            'user': sysadmin['name']
        }

        with pytest.raises(toolkit.ObjectNotFound):
            helpers.call_action(
                'featured_show',
                context=context,
                resource_view_id='fake-id'
            )

    def test_featured_show_with_result(self):
        '''
        Calling featured_show without any saved featuredviews
        '''
        sysadmin = factories.Sysadmin()
        dataset = factories.Dataset()
        resource = factories.Resource(
            package_id=dataset['id'],
            format='png'
        )
        resource_view = factories.ResourceView(
            resource_id=resource['id'],
            image_url='http://some.image.png'
        )
        context = {
            'user': sysadmin['name']
        }

        helpers.call_action(
            'featured_create',
            context=context,
            resource_view_id=resource_view['id'],
            canonical=True,
            homepage=False
        )

        featuredview_dict = helpers.call_action(
            'featured_show',
            context=context,
            resource_view_id=resource_view['id']
        )

        # found a featuredview
        assert featuredview_dict.get('resource_view_id') == resource_view['id']
        assert featuredview_dict.get('package_id') == dataset['id']
        assert featuredview_dict.get('canonical') == True
        assert featuredview_dict.get('homepage') == False
