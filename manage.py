#!/usr/bin/env python
"""Manage.py, MC server assistant

Usage:
  manage.py sort [--folder=<unsorted_dir>]
  manage.py (-h | --help)
  manage.py --version

Options:
  --folder=<unsorted_dir>  Specify an input folder relative to this file
  -h --help                Show this screen.
  --version                Show version.

"""
from docopt import docopt
import hashlib
import logging
import os
import sys
import yaml
import zipfile
from pprint import pprint as pp

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

ROOT = os.path.abspath(os.path.dirname(__file__))
UNSORTED = os.path.join(ROOT, 'unsorted')
PLUGINS = os.path.join(ROOT, 'plugins')

def _confirmwrite(jarloc):
	print "Please confirm overwrite file with different hash at location: ", jarloc
	while True:
		n = raw_input('Overwrite file?: ')
		if n in ['y', 'n']:
			return n == 'y'

def _safejoin(*args):
	p = os.path.abspath(os.path.join(*args))
	assert p.startswith(ROOT)
	return p

def _comparefiles(unsortedjar, newjar):
	with open(unsortedjar, 'r') as a, open(newjar, 'r') as b:
		return hashlib.md5(a.read()).hexdigest() == hashlib.md5(b.read()).hexdigest()

def _makedir(*args):
	if not os.path.exists(_safejoin(*args)):
		os.mkdir(_safejoin(*args))
		logging.info('Folder created (%s)', os.path.join(*args))

def get_plugins():
	for f in os.listdir(UNSORTED):
		if f.endswith('.jar'):
			yield f

def get_plugin(filepath):
	return zipfile.ZipFile(_safejoin(UNSORTED, filepath), 'r')

def get_pluginyaml(filepath):
	with get_plugin(filepath) as _zip:
		return yaml.load(_zip.read('plugin.yml'))

def get_plugin_info(pluginyaml):
	return map(str, [pluginyaml['name'], pluginyaml['version']])

def move_version(pluginname, version, filename):
	_makedir(PLUGINS, pluginname)
	_makedir(PLUGINS, pluginname, version)
	pfile = _safejoin(PLUGINS, pluginname, version, pluginname.lower() + ".jar")
	sfile = _safejoin(UNSORTED, filename)
	if os.path.exists(pfile) and not _comparefiles(sfile, pfile):
		if not _confirmwrite(pfile):
			return
	
	with open(pfile, 'wb+') as ouf:
		with open(sfile, 'rb') as inf:
			ouf.write(inf.read())
			logging.info('Placed (%s) to (%s)', filename, pfile)
	os.remove(_safejoin(UNSORTED, filename))

def sort_main(args):
	if '--folder' in args:
		UNSORTED = os.path.join(ROOT, args['--folder'])

	_makedir(UNSORTED)
	_makedir(PLUGINS)

	for x in get_plugins():
		plugin, version = get_plugin_info(get_pluginyaml(x))
		move_version(plugin, version, x)


if __name__ == '__main__':
	arguments = docopt(__doc__, version='Manage.py 1.0')
	print(arguments)

	if 'sort' in arguments and arguments['sort']:
		sort_main(arguments)

	