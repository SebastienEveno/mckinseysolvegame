from setuptools import setup, find_packages

with open('README.md', 'r', encoding="utf-8", errors='ignore') as fh:
    long_description = fh.read()

version = {}
with open("mckinseysolvegame/_version.py", encoding="utf-8") as fp:
    exec(fp.read(), version)

setup(name='mckinseysolvegame',
      version=version['__version__'],
      description='Python library for solving McKinsey Solve Game',
      author='Sebastien Eveno',
      author_email='sebastien.louis.eveno@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SebastienEveno/mckinseysolvegame',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.23.5',
          'pandas>=1.5.1',
          'scipy>=1.9.3',
          'pytest>=7.1.3',
          'marshmallow>=3.19.0'
      ],
      python_requires='>=3.10.2, <4',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Financial and Insurance Industry',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.10',
          'Operating System :: OS Independent',
          'Intended Audience :: Science/Research',
          'Topic :: Software Development',
          'Topic :: Office/Business :: Financial',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ]
      )
