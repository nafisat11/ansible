#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Deployment script for Chorus.
"""
from distutils.core import setup
import re

import libchorus3dp

setup(
    name='chorus3dp',
    version=libchorus3dp.VERSION,
    description="Fire-and-forget, priority-queue-oriented fleet configuration engine",
    author=re.search('(.*?) <', libchorus3dp.CONTACT).group(1),
    author_email=re.search('<(.*?)>', libchorus3dp.CONTACT).group(1),
    url=libchorus3dp.URL,
    license='Limited Use Software License Agreement',
    packages=[
        'libchorus3dp',
    ],
    scripts=[
        'chorus3dp',
    ],
    data_files = [
        ('/etc/3d-p/chorus3dp/', [
            'sample/chorus3dp.json',
        ]),
    ],
)
