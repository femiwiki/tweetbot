import setuptools

setuptools.setup(
    name='tweetbot',
    packages=setuptools.find_packages(),
    install_requires=[
        'python-twitter',
        'mwclient',
    ],
)
