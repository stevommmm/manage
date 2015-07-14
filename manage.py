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

def _safejoin(*args):
	"""Ensure we're not open to directory traversal"""
	p = os.path.abspath(os.path.join(*args))
	assert p.startswith(ROOT)
	return p

def _confirmwrite(jarloc):
	print("Please confirm overwrite file with different hash at location: %s" % jarloc)
	while True:
		n = raw_input('Overwrite file? [y/n] ')
		if n in ['y', 'n']:
			return n == 'y'

def _comparefiles(unsortedjar, newjar):
	"""Compare two files using their hash, low chance of md5 collision"""
	with open(unsortedjar, 'r') as a, open(newjar, 'r') as b:
		return hashlib.md5(a.read()).hexdigest() == hashlib.md5(b.read()).hexdigest()

def _makedir(*args):
	"""Create the requested directory if it doesn't exist, silently pass if it does"""
	if not os.path.exists(_safejoin(*args)):
		os.mkdir(_safejoin(*args))
		logging.info('Folder created (%s)', os.path.join(*args))


class pluginSorter(object):
	""" Sort plugins based on plugin.yml stated version """
	def __init__(self, options):
		self.plugin_dir = _safejoin(ROOT, 'plugins')
		self.unsorted_dir = _safejoin(ROOT, 'unsorted')

		if not options['--folder'] is None:
			self.unsorted_dir = os.path.join(ROOT, options['--folder'])

		_makedir(self.unsorted_dir)
		_makedir(self.plugin_dir)

		for x in self.get_plugins():
			plugin, version = self.get_plugin_info(self.get_pluginyaml(x))
			self.move_version(plugin, version, x)

	def get_plugins(self):
		"""Enumerate our unsorted plugin folder, return .jar files"""
		for f in os.listdir(self.unsorted_dir):
			if f.endswith('.jar'):
				yield f

	def get_plugin(self, filepath):
		"""Return an open file handle to our .jar file.
		   Use from a with block to esure file handle close
		"""
		return zipfile.ZipFile(_safejoin(self.unsorted_dir, filepath), 'r')

	def get_pluginyaml(self, filepath):
		"""Rip the plugin.yml out of our plugin jar, return a python object"""
		with self.get_plugin(filepath) as _zip:
			return yaml.load(_zip.read('plugin.yml'))

	def get_plugin_info(self, pluginyaml):
		"""Filter the yaml returned into plugin name and version"""
		return map(str, [pluginyaml['name'], pluginyaml['version']])

	def move_version(self, pluginname, version, filename):
		"""Move an unsorted jar to its final location, ensure that we
		   have created all the directories in the path
		"""
		_makedir(self.plugin_dir, pluginname)
		_makedir(self.plugin_dir, pluginname, version.replace(os.sep, '_'))
		pfile = _safejoin(self.plugin_dir, pluginname, version, pluginname.lower() + ".jar")
		sfile = _safejoin(self.unsorted_dir, filename)
		if os.path.exists(pfile) and not _comparefiles(sfile, pfile):
			if not _confirmwrite(pfile):
				return
		
		with open(pfile, 'wb+') as ouf:
			with open(sfile, 'rb') as inf:
				ouf.write(inf.read())
				logging.info('Placed (%s) to (%s)', filename, pfile)
		os.remove(_safejoin(self.unsorted_dir, filename))

if __name__ == '__main__':
	arguments = docopt(__doc__, version='Manage.py 1.0')

	if arguments['sort']:
		pluginSorter(arguments)

	