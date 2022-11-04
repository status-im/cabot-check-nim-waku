#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='cabot_check_nim_waku',
      version='0.1.0',
      description='A nim-waku canary check plugin for Cabot',
      author='Jakub Sokołowski',
      author_email='jakub@status.im',
      url='https://github.com/status-im/cabot-check-nim-waku',
      packages=find_packages(),
      download_url = 'https://github.com/status-im/cabot-check-status-go/tarball/0.1.0',
      )
