from django.test import TestCase

from signal_connectors import _perm_model as perm_model


def _create_mock_model(**opts):

    class MockOpts(object):
        abstract = False
        app_label = 'mock'
        auto_created = False
        model_name = 'fake'
        permissions = []
        proxy = None
        verbose_name = 'No such thing'

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            super(MockOpts, self).__init__()

    class MockModel(object):

        def __init__(self, **opts):
            self._meta = MockOpts(**opts)
            super(MockModel, self).__init__()

    return MockModel(**opts)


class TestPermsAdded(TestCase):

    def setUp(self):
        self.rightapp_model = _create_mock_model(
            app_label='rightapp',
            model_name='rightmodel',
            verbose_name='Right model'
        )
        self.wrongmodel_model = _create_mock_model(
            app_label='rightapp',
            model_name='wrongmodel',
            verbose_name='Wrong model'
        )
        self.wrongapp_model = _create_mock_model(
            app_label='wrongapp',
            model_name='wrongmodel',
            verbose_name='Wrong model'
        )
        self.abstract_model = _create_mock_model(
            abstract=True
        )
        self.auto_model = _create_mock_model(
            auto_created=True
        )
        self.proxy_model = _create_mock_model(
            proxy=self.rightapp_model
        )

    def test_perms_added(self):

        self.assertEquals(
            self.rightapp_model._meta.permissions,
            []
        )
        perm_model(self.rightapp_model)
        self.assertEquals(
            self.rightapp_model._meta.permissions,
            [
                ('list_rightmodel', 'Can list right model'),
                ('view_rightmodel', 'Can view right model'),
            ]
        )

    def test_custom_perms_added(self):

        with self.settings(HAIRDRESSER_ACTIONS=['rollback']):
            perm_model(self.rightapp_model)
            self.assertEquals(
                self.rightapp_model._meta.permissions,
                [
                    ('rollback_rightmodel', 'Can rollback right model'),
                ]
            )

    def test_app_blacklist(self):

        with self.settings(HAIRDRESSER_BLACKLIST=['wrongapp']):
            perm_model(self.rightapp_model)
            perm_model(self.wrongapp_model)

            self.assertEquals(
                self.rightapp_model._meta.permissions,
                [
                    ('list_rightmodel', 'Can list right model'),
                    ('view_rightmodel', 'Can view right model'),
                ]
            )

            self.assertEquals(
                self.wrongapp_model._meta.permissions,
                []
            )

    def test_model_blacklist(self):

        with self.settings(HAIRDRESSER_BLACKLIST=[('rightapp', 'wrongmodel')]):
            perm_model(self.rightapp_model)
            perm_model(self.wrongmodel_model)

            self.assertEquals(
                self.rightapp_model._meta.permissions,
                [
                    ('list_rightmodel', 'Can list right model'),
                    ('view_rightmodel', 'Can view right model'),
                ]
            )

            self.assertEquals(
                self.wrongmodel_model._meta.permissions,
                []
            )

    def test_app_whitelist(self):

        with self.settings(HAIRDRESSER_WHITELIST=['rightapp']):
            perm_model(self.rightapp_model)
            perm_model(self.wrongapp_model)

            self.assertEquals(
                self.rightapp_model._meta.permissions,
                [
                    ('list_rightmodel', 'Can list right model'),
                    ('view_rightmodel', 'Can view right model'),
                ]
            )

            self.assertEquals(
                self.wrongapp_model._meta.permissions,
                []
            )

    def test_model_whitelist(self):

        with self.settings(HAIRDRESSER_WHITELIST=[('rightapp', 'rightmodel')]):
            perm_model(self.rightapp_model)
            perm_model(self.wrongmodel_model)

            self.assertEquals(
                self.rightapp_model._meta.permissions,
                [
                    ('list_rightmodel', 'Can list right model'),
                    ('view_rightmodel', 'Can view right model'),
                ]
            )

            self.assertEquals(
                self.wrongmodel_model._meta.permissions,
                []
            )
