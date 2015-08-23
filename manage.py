#!/usr/bin/env python
"""Manage.py, MC server assistant

Usage:
  manage.py sort [--folder=<DIR>]
  manage.py report (nms|permissions)
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
import collections
import string
import multiprocessing
from multiprocessing.pool import ThreadPool

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

ROOT = os.path.abspath(os.path.dirname(__file__))


def _safejoin(*args):
	"""Ensure we're not open to directory traversal"""
	p = os.path.abspath(os.path.join(*args))
	assert p.startswith(ROOT)
	return p

def _makedir(*args):
	"""Create the requested directory if it doesn't exist, silently pass if it does"""
	if not os.path.exists(_safejoin(*args)):
		os.mkdir(_safejoin(*args))
		logging.info('Folder created (%s)', os.path.join(*args))

class Plugin(object):
	def __init__(self, filepath):
		self.fh = zipfile.ZipFile(filepath, 'r')

	def __del__(self):
		try:
			self.fh.close()
		except:
			pass

	def getPluginYAML(self):
		return yaml.load(self.getPluginFile('plugin.yml'))

	def getPluginInfo(self):
		plugin_yaml = self.getPluginYAML()
		return map(str, [plugin_yaml['name'], plugin_yaml['version']])

	def getPluginFiles(self):
		return self.fh.infolist()

	def getPluginFile(self, filename):
		return self.fh.read(filename)

	def getPluginNMS(self):
		buff = collections.deque([], 500)
		nmsbuff = ""
		readversion = False
		nmsfound = []

		for f in self.getPluginFiles():
			if f.filename.endswith('.class'):
				for c in self.getPluginFile(f):
					if c in string.printable:
						buff.append(c)
					if readversion and c != "/":
						nmsbuff += c
					if readversion and c == "/":
						readversion = False
						nmsfound.append(nmsbuff)
						nmsbuff = ""
					if ''.join(buff).endswith('net/minecraft/server/v') or \
					   ''.join(buff).endswith('org/bukkit/craftbukkit/v'):
					   readversion = True
		return set(nmsfound)


class ClassSearcher(object):
	def __init__(self, filepath):
		self.plugin_dir = _safejoin(ROOT, 'plugins')

		# Throw our list of plugins at a threaded pool to help async process this
		pool = ThreadPool(multiprocessing.cpu_count())
		pool.map(self.formatInfo, [Plugin(x) for x in self.findPlugins()])

	def findPlugins(self):
		for root, dirnames, filenames in os.walk(self.plugin_dir):
		    for filename in filenames:
		        if filename.endswith('.jar'):
		            yield _safejoin(root, filename)

	def formatInfo(self, plugin):
		logging.info("%s v%s requires nms: %s", plugin.getPluginInfo()[0], plugin.getPluginInfo()[1], ', '.join(plugin.getPluginNMS()))


class pluginSorter(object):
	""" Sort plugins based on plugin.yml stated version """
	def __init__(self, options):
		self.plugin_dir = _safejoin(ROOT, 'plugins')
		self.unsorted_dir = _safejoin(ROOT, 'unsorted')

		if not options['--folder'] is None:
			self.unsorted_dir = os.path.join(ROOT, options['--folder'])

		_makedir(self.unsorted_dir)
		_makedir(self.plugin_dir)

		for x in self.getPlugins():
			plugin = self.getPlugin(x)
			pluginname, version = plugin.getPluginInfo()
			self.move_version(pluginname, version, x)

	def getPlugins(self):
		"""Enumerate our unsorted plugin folder, return .jar files"""
		for f in os.listdir(self.unsorted_dir):
			if f.endswith('.jar'):
				yield f

	def getPlugin(self, filepath):
		"""Return an open file handle to our .jar file.
		   Use from a with block to esure file handle close
		"""
		return Plugin(_safejoin(self.unsorted_dir, filepath))

	def confirmwrite(self, jarloc):
		print("Please confirm overwrite file with different hash at location: %s" % jarloc)
		while True:
			n = raw_input('Overwrite file? [y/n] ')
			if n.lower() in ['y', 'n']:
				return n.lower() == 'y'

	def comparefiles(self, unsortedjar, newjar):
		"""Compare two files using their hash, low chance of md5 collision"""
		with open(unsortedjar, 'r') as a, open(newjar, 'r') as b:
			return hashlib.md5(a.read()).hexdigest() == hashlib.md5(b.read()).hexdigest()

	def move_version(self, pluginname, version, filename):
		"""Move an unsorted jar to its final location, ensure that we
		   have created all the directories in the path
		"""
		_makedir(self.plugin_dir, pluginname)
		_makedir(self.plugin_dir, pluginname, version.replace(os.sep, '_'))
		pfile = _safejoin(self.plugin_dir, pluginname, version, pluginname.lower() + ".jar")
		sfile = _safejoin(self.unsorted_dir, filename)
		if os.path.exists(pfile) and not self.comparefiles(sfile, pfile):
			if not self.confirmwrite(pfile):
				return
		
		with open(pfile, 'wb+') as ouf, open(sfile, 'rb') as inf:
			ouf.write(inf.read())
			logging.info('Placed (%s) to (%s)', filename, pfile)
		os.remove(_safejoin(self.unsorted_dir, filename))

if __name__ == '__main__':
	arguments = docopt(__doc__, version='Manage.py 1.0')

	if arguments['sort']:
		pluginSorter(arguments)
	if arguments['report'] and arguments['nms']:
		ClassSearcher(arguments)

	