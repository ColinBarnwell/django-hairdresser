from south.signals import post_migrate


def _migrate_perms(*args, **kwargs):
    """
    Ensure that all declared permissions on a model have been installed once
    South migrations have been run.
    """
    import sys
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from django.db.models import get_app, get_models

    for model in get_models(get_app(kwargs['app'])):
        content_type = ContentType.objects.get_for_model(model)
        for codename, name in model._meta.permissions:
            perm, created = Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={
                    'name': name
                }
            )
            if created:
                sys.stdout.write(
                    "Installed new permission {app_label}.{codename}\n".format(
                        app_label=model._meta.app_label,
                        codename=codename
                    )
                )

post_migrate.connect(_migrate_perms)
