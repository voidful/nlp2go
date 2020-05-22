from setuptools import setup, find_packages

setup(
    name='nlp2go',
    version='0.0.18',
    description='hosting nlp models for demo purpose',
    url='https://github.com/voidful/nlp2go',
    author='Voidful',
    author_email='voidful.stack@gmail.com',
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords='nlp tfkit classification generation tagging deep learning machine reading',
    packages=find_packages(),
    install_requires=[
        "tfkit>=0.3.10",
        "flask",
        "flask-cors",
        "gevent"
    ],
    entry_points={
        'console_scripts': ['nlp2go=nlp2go.server:main', 'nlp2go-preload=nlp2go.prep:main']
    },
    zip_safe=False,
)
