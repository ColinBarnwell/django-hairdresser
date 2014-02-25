Django Hairdresser
==================

Adds extra perms to your Django models (how you use them is up to you)


Basic usage
-----------

There is no need to add this to your INSTALLED_APPS (unless you wish to run
the tests).

Instead import the following somewhere that will be run before any models are
loaded, such as the main __init__.py file.

```
import hairdresser
hairdresser.add_perms()
```

This must be done before Django begins loading models, otherwise Hairdresser
will miss the signals that are fired when some of those models are loaded.

The next time you run sycdb or migrate, all of your models will receive list
and view permission in addition to the add, change and delete permissions
created by Django.

This does not affect any other custom permissions you may already have created.

As a bonus, Hairdresser will install any other custom permissions without you
having to create a custom migration in, for example, South.

_Note that certain Django apps, namely auth, contenttypes and sites, are not,
and cannot be modified by this app._

Customising permissions
-----------------------

In settings, declare HAIRDRESSER_ACTIONS as a list of action strings for each
of the permissions you wish to create.

```python

# Default
HAIRDRESSER_ACTIONS = ['list', 'view']

# Override
HAIRDRESSER_ACTIONS = ['batch_update']

```

Blacklisting apps or models
---------------------------

In settings, declare HAIRDRESSER_BLACKLIST and add to it a list of app names
or (app name, model name) pairs.

```python

HAIRDRESSER_BLACKLIST = (
    'auth',
    'south',
    ('myapp', 'mymodel')
)

```

Whitelisting apps or models
---------------------------

In settings, declare HAIRDRESSER_WHITELIST and add to it a list of app names
or (app name, model name) pairs.

```python

HAIRDRESSER_WHITELIST = (
    'myapp',
    ('myotherapp', 'mymodel')
)

```