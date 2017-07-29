#!/usr/bin/python

# python setup.py sdist --format=zip,gztar

from setuptools import setup, find_packages
import os
import sys
import platform
import imp


if sys.version_info[:3] < (2, 7, 0):
    sys.exit("Error: Reddcoin Electrum requires Python version >= 2.7.0...")

usr_share = '/usr/share'
if not os.access(usr_share, os.W_OK):
    usr_share = os.getenv("XDG_DATA_HOME", os.path.join(os.path.expanduser("~"), ".local", "share"))

data_files = []
if (len(sys.argv) > 1 and (sys.argv[1] == "sdist")) or (platform.system() != 'Windows' and platform.system() != 'Darwin'):
    print "Including all files"
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['reddcoin-electrum.desktop']),
        (os.path.join(usr_share, 'app-install', 'icons/'), ['icons/reddcoin-electrum.png'])
    ]
    if not os.path.exists('locale'):
        os.mkdir('locale')
    for lang in os.listdir('locale'):
        if os.path.exists('locale/%s/LC_MESSAGES/reddcoin-electrum.mo' % lang):
            data_files.append((os.path.join(usr_share, 'locale/%s/LC_MESSAGES' % lang), ['locale/%s/LC_MESSAGES/reddcoin-electrum.mo' % lang]))

util = imp.load_source('util', 'lib/util.py')
appdata_dir = util.appdata_dir()
if not os.access(appdata_dir, os.W_OK):
    appdata_dir = os.path.join(usr_share, "reddcoin-electrum")

data_files += [
    (appdata_dir, ["data/README"]),
    (os.path.join(appdata_dir, "cleanlook"), [
        "data/cleanlook/name.cfg",
        "data/cleanlook/style.css"
    ]),
    (os.path.join(appdata_dir, "sahara"), [
        "data/sahara/name.cfg",
        "data/sahara/style.css"
    ]),
    (os.path.join(appdata_dir, "dark"), [
        "data/dark/name.cfg",
        "data/dark/style.css"
    ])
]

for lang in os.listdir('data/wordlist'):
    data_files.append((os.path.join(appdata_dir, 'wordlist'), ['data/wordlist/%s' % lang]))

basedir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    f = open(os.path.join(basedir, filename))
    try:
        return f.read()
    finally:
        f.close()


VERSION = '1.0.5'
setup(
    name="reddcoin-electrum",
    version=VERSION,
    install_requires=['ecdsa>=0.9', 'pbkdf2', 'requests', 'pyasn1', 'pyasn1-modules',
                      'qrcode', 'tlslite>=0.4.5', 'numpy', 'SocksiPy-branch'],
    packages=['reddcoin_electrum', 'reddcoin_electrum_gui', 'reddcoin_electrum_gui.qt', 'reddcoin_electrum_plugins'],
    package_dir={
        'reddcoin_electrum': 'lib',
        'reddcoin_electrum_gui': 'gui',
        'reddcoin_electrum_plugins': 'plugins',
    },
    scripts=['reddcoin-electrum'],
    include_package_data=True,
    data_files=data_files,
    description="Reddcoin Electrum wallets for desktop",
    author="Thomas Voegtlin, Larry Ren",
    author_email="thomasv1@gmx.de, ren@reddcoin.com",
    maintainer="Larry Ren",
    maintainer_email="ren@reddcoin.com",
    license="GNU GPLv3",
    url="https://wallet.reddcoin.com",
    download_url="https://pypi.python.org/packages/source/l/reddcoin-electrum/reddcoin-electrum-%s.tar.gz" % VERSION,
    long_description=read_file('README.rst'),
    platforms="All",
    classifiers=[
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
