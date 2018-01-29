from setuptools import setup, find_packages
from battleship import __version__ as battleship_version
from pip.req import parse_requirements
from pip import download

# Let's get our requirements from requirements.txt
requirements = parse_requirements("requirements.txt", session=download.PipSession())
my_requirements = [str(req.req) for req in requirements]

setup(
    name='battleship',
    version = battleship_version,
    description='Python console version of battleship.',
    author='Tanner Purves, Zane Durkin',
    author_email='purvesta0704@gmail.com, zanedurkin@gmail.com',
    url='https://github.com/durkinza/battleship',
    packages=find_packages(exclude=['tests*']),
    install_requires=my_requirements
)
