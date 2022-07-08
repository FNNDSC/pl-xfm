from setuptools import setup

setup(
    name='cxfm',
    version='0.1.0',
    description='A ChRIS plugin to perform XFM transformations on surfaces',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-xfm',
    py_modules=['cxfm'],
    install_requires=['chris_plugin', 'pycivet', 'loguru'],
    license='MIT',
    python_requires='>=3.10.2',
    entry_points={
        'console_scripts': [
            'cxfm = cxfm:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
