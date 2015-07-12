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

def _safejoin(*args):
	p = os.path.abspath(os.path.join(*args))
	assert p.startswith(ROOT)
	return p

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
	return (pluginyaml['name'], pluginyaml['version'])

def move_version(pluginname, version, filename):
	_makedir(PLUGINS, pluginname)
	_makedir(PLUGINS, pluginname, version)
	pfile = _safejoin(PLUGINS, pluginname, version, pluginname.lower() + ".jar")
	with open(pfile, 'wb+') as ouf:
		with open(_safejoin(UNSORTED, filename), 'rb') as inf:
			ouf.write(inf.read())
			logging.info('Placed (%s) to (%s)', filename, pfile)
	os.remove(_safejoin(UNSORTED, filename))

if __name__ == '__main__':
	_makedir(UNSORTED)
	_makedir(PLUGINS)

	for x in get_plugins():
		plugin, version = get_plugin_info(get_pluginyaml(x))
		move_version(plugin, version, x)