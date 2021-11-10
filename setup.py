import pathlib
import sys
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

REQUIRES = ["connexion"]

use = [
    'bcrypt',
    'certifi',
    'Django',
    'psycopg2-binary',
    'dnspython',
    'pymongo',
    'python-dotenv'
]

tests = [
    'coverage',
    'mutmut'
]

dev = [
]

setup(
      name='GoatBoat Mentoring',
      version="1.0.0",
      description='Mentor Matching Application',
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://github.com/crav12345/GoatBoat/",
      author='GoatBoat',
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
      ],
      packages=find_packages(),
      package_data={'': ['swagger/swagger.yaml']},
      include_package_data=True,
      install_requires=use,
      tests_require=tests,
      entry_points={
        'console_scripts': [
            'goatboat = mentor.manage:main',
            'swagger_server=swagger_server.__main__:main',
        ],
      }
)
