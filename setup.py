import setuptools

setuptools.setup(
        name='tq',
        version='0.0.0',
        author='Team Awesome',
        author_email='andrewmichaelhenry@gmail.com',
        packages=['tq'],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'twenty=tq.tq:main',
                'player=tq.player:main',
                ]
            },
        install_requires=[
            'scikit-learn',
            'prettytable',
            ],
        )

