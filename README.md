# Shared #

Python snippets to manage server plugins.

Newly compiled plugins should be placed in the `unsorted` folder. 

On run plugins are sorted into `plugins/<pluginName>/<version>/<pluginName>.jar`

## to-do ##

Sort command, no-delete option
Symlink command, linking to plugin directory, takes server root as arg


## Example usage ##

	$ python main.py
	INFO:Folder created (plugins/AsyncWorldEdit)
	INFO:Folder created (plugins/AsyncWorldEdit/2.1.5)
	INFO:Placed (AsyncWorldEdit.jar) to (plugins/AsyncWorldEdit/2.1.5/asyncworldedit.jar)
	INFO:Folder created (plugins/AsyncWorldEditInjector)
	INFO:Folder created (plugins/AsyncWorldEditInjector/2.1.3)
	INFO:Placed (AsyncWorldEditInjector.jar) to (plugins/AsyncWorldEditInjector/2.1.3/asyncworldeditinjector.jar)
	INFO:Folder created (plugins/WorldBorder)
	INFO:Folder created (plugins/WorldBorder/1.8.3)
	INFO:Placed (WorldBorder.jar) to (plugins/WorldBorder/1.8.3/worldborder.jar)
	INFO:Folder created (plugins/WorldEdit)
	INFO:Folder created (plugins/WorldEdit/6.0;3342-78f975b9)
	INFO:Placed (worldedit-bukkit-6.0.jar) to (plugins/WorldEdit/6.0;3342-78f975b9/worldedit.jar)
	INFO:Folder created (plugins/WorldGuard)
	INFO:Folder created (plugins/WorldGuard/6.0.0-beta-05.1569-)
	INFO:Placed (worldguard-6.0.0-beta-05.jar) to (plugins/WorldGuard/6.0.0-beta-05.1569-/worldguard.jar)
