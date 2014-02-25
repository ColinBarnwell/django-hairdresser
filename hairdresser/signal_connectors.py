from django.conf import settings
from django.db.models import signals

# Check if any migrators are installed in case we need to force in new perms
if 'south' in settings.INSTALLED_APPS:
    import migrate_south
if hasattr(signals, 'post_migrate'):
    import migrate_django


def _perm_model(sender, **kwargs):
    """
    Add action-based permissions to all valid models according to
    HAIRDRESSER_ACTIONS setting or application defaults.

    If HAIRDRESSER_BLACKLIST setting is declared, then any apps or
    app/model tuples in that list will be ignored.

    If HAIRDRESSER_WHITELIST setting is declared, then only apps or
    app/model tuples in that list will be included.
    """
    actions = set(getattr(settings, 'HAIRDRESSER_ACTIONS', ['list', 'view']))
    blacklist = getattr(settings, 'HAIRDRESSER_BLACKLIST', []) + ['auth', 'contenttypes', 'sites']
    whitelist = getattr(settings, 'HAIRDRESSER_WHITELIST', None)

    opts = sender._meta

    # Only add perms to distinct, non-abstract, user-created models
    if opts.abstract or opts.auto_created or opts.proxy:
        return

    # Skip blacklistsed apps or models
    if (
        opts.app_label in blacklist
        or (opts.app_label, opts.model_name) in blacklist
    ):
        return

    # Validate against whitelisted apps and models (if any)
    if whitelist is not None:
        if not (
            opts.app_label in whitelist
            or (opts.app_label, opts.model_name) in whitelist
        ):
            return

    permission_codenames = [permission[0] for permission in opts.permissions]

    for action in actions:
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
