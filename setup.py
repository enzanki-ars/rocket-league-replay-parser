import glob
import os
from distutils.core import setup

setup(
        name='rocketleaguereplayanalysis',
        version='1.4.0-alpha3',
        url='https://enzanki-ars.github.io/rocket-league-replay-analysis',
        license='GNU AGPLv3',
        author='Alex Shafer',
        author_email='enzanki.ars@gmail.com',
        description='Parses Rocket League replay json files and '
                    'creates a minimap video',
        requires=[],
        packages=['rocketleaguereplayanalysis'],
        package_dir={
            'rocketleaguereplayanalysis': 'rocketleaguereplayanalysis'
        },
        package_data={
            'rocketleaguereplayanalysis':
                [glob.glob(os.path.join('assets', '*'))]
        },
)
