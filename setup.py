from setuptools import setup, find_packages

setup(
    name='xDisHook',
    version='1.0.0',
    author='Hanzou',
    author_email='hanzou@hanzou.sh',
    description='A tool for generating and checking Discord Nitro codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/im-hanzou/DisHook',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'xdishook=xDisHook.main:main_function',
        ],
    },
)
