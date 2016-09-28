import os
from setuptools import setup, find_packages

version = '0.1.dev0'

setup(name='git.scripts',
      version=version,
      description="Git Scripts",
      long_description=open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='git scripts',
      author='FBruynbroeck',
      author_email='francois.bruynbroeck@hotmail.com',
      url='https://github.com/FBruynbroeck/git.scripts',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['git', 'git.scripts'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zest.releaser',
          'pyaml',
      ],
      entry_points={
          'console_scripts': [
              'reload_hooks = git.scripts.hooks:reload_hooks',
              'remove_hooks = git.scripts.hooks:remove_hooks',
              'changelogrelease = git.scripts.release:change_log',
              'changeremote = git.scripts.remote:change_remote',
          ],
      }
      )
