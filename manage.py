#!/usr/bin/env python
"""Manage.py, MC server assistant

Usage:
  manage.py sort [--folder=<DIR>]
  manage.py (-h | --help)
  manage.py --version

Options:
  --folder=<DIR>  Specify an input folder relative to this file
  -h --help       Show this screen.
  --version       Show version.

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
	print("Please confirm overwrite file with different hash at location: %s" % jarloc)
	while True:
		n = raw_input('Overwrite file? [y/n] ')
		if n in ['y', 'n']:
			return n == 'y'

def _safejoin(*args):
	"""Ensure we're not open to directory traversal"""
	p = os.path.abspath(os.path.join(*args))
	assert p.startswith(ROOT)
	return p

def _comparefiles(unsortedjar, newjar):
	"""Compare two files using their hash, low chance of md5 collision"""
	with open(unsortedjar, 'r') as a, open(newjar, 'r') as b:
		return hashlib.md5(a.read()).hexdigest() == hashlib.md5(b.read()).hexdigest()

def _makedir(*args):
	"""Create the requested directory if it doesn't exist, silently pass if it does"""
	if not os.path.exists(_safejoin(*args)):
		os.mkdir(_safejoin(*args))
		logging.info('Folder created (%s)', os.path.join(*args))

def get_plugins():
	"""Enumerate our unsorted plugin folder, return .jar files"""
	for f in os.listdir(UNSORTED):
		if f.endswith('.jar'):
			yield f

def get_plugin(filepath):
	"""Return an open file handle to our .jar file"""
	return zipfile.ZipFile(_safejoin(UNSORTED, filepath), 'r')

def get_pluginyaml(filepath):
	"""Rip the plugin.yml out of our plugin jar, return a python object"""
	with get_plugin(filepath) as _zip:
		return yaml.load(_zip.read('plugin.yml'))

def get_plugin_info(pluginyaml):
	"""Filter the yaml returned into plugin name and version"""
	return map(str, [pluginyaml['name'], pluginyaml['version']])

def move_version(pluginname, version, filename):
	"""Move an unsorted jar to its final location, ensure that we
	   have created all the directories in the path
	"""
	_makedir(PLUGINS, pluginname)
	_makedir(PLUGINS, pluginname, version.replace(os.sep, '_'))
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
	"""Handler for the sort command"""
	if not args['--folder'] is None:
		global UNSORTED
		UNSORTED = os.path.join(ROOT, args['--folder'])

	_makedir(UNSORTED)
	_makedir(PLUGINS)

	for x in get_plugins():
		plugin, version = get_plugin_info(get_pluginyaml(x))
		move_version(plugin, version, x)
		x.close()


if __name__ == '__main__':
	arguments = docopt(__doc__, version='Manage.py 1.0')

	if arguments['sort']:
		sort_main(arguments)

	