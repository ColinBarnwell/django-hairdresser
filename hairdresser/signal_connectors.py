from django.conf import settings
from django.db.models import signals

# Check if any migrators are installed in case we need to force in new perms
if 'south' in settings.INSTALLED_APPS:
    import migrate_south
if hasattr(signals, 'post_migrate'):
    import migrate_django


_HAIRDRESSER_ACTIONS = set(getattr(settings, 'HAIRDRESSER_ACTIONS', ['list', 'view']))
_HAIRDRESSER_BLACKLIST = getattr(settings, 'HAIRDRESSER_BLACKLIST', []) + ['auth', 'contenttypes', 'sites']
_HAIRDRESSER_WHITELIST = getattr(settings, 'HAIRDRESSER_WHITELIST', None)


def _perm_model(sender, **kwargs):
    """
    Add action-based permissions to all valid models according to
    HAIRDRESSER_ACTIONS setting or application defaults.

    If HAIRDRESSER_BLACKLIST setting is declared, then any apps or
    app/model tuples in that list will be ignored.

    If HAIRDRESSER_WHITELIST setting is declared, then only apps or
    app/model tuples in that list will be included.
    """
    opts = sender._meta

    # Only add perms to distinct, non-abstract, user-created models
    if opts.abstract or opts.auto_created or opts.proxy:
        return

    # Skip blacklistsed apps or models
    if (
        opts.app_label in _HAIRDRESSER_BLACKLIST
        or (opts.app_label, opts.model_name) in _HAIRDRESSER_BLACKLIST
    ):
        return

    # Validate against whitelisted apps and models (if any)
    if _HAIRDRESSER_WHITELIST is not None:
        if not (
            opts.app_label in _HAIRDRESSER_WHITELIST
            or (opts.app_label, opts.model_name) in _HAIRDRESSER_WHITELIST
        ):
            print 'excluding %s.%s' % (opts.app_label, opts.model_name)
            return

    print 'including %s.%s' % (opts.app_label, opts.model_name)

    permission_codenames = [permission[0] for permission in opts.permissions]

    for action in _HAIRDRESSER_ACTIONS:
        codename = u'{action}_{model_name}'.format(
            action=action,
            model_name=opts.model_name
        )
        name = u'Can {action} {name}'.format(
            action=action,
            name=opts.verbose_name.lower()[:50]
        )
        if codename not in permission_codenames:
            opts.permissions += (codename, name),


signals.class_prepared.connect(_perm_model)
