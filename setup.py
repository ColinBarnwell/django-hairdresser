from distutils.core import setup

setup(
    name='django-hairdresser',
    version='0.1',
    author='Colin Barnwell',
    packages=['hairdresser'],
    description='Add extra perms to your Django models',
    long_description=open('README.md').read(),
    install_requires=["Django >= 1.4"],
)