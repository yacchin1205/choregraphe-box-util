#!/usr/bin/env python

from setuptools import setup

setup(name='ChoregrapheBoxUtils',
      version='0.1',
      description='Choregraphe Box Utilities',
      author='Satoshi Yazawa',
      author_email='yazawa@yzwlab.net',
      url='https://github.com/yacchin1205/choregraphe-box-util',
      packages=['choregraphebox'],
      install_requires=["lxml"],
      entry_points={'console_scripts':
                    ['verify-boxlib=choregraphebox.boxlib:verify'], },
      )
