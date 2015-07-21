# Manage.py #

Python snippets to manage server plugins.

Newly compiled plugins should be placed in the `unsorted` folder. 

On run plugins are sorted into `plugins/<pluginName>/<version>/<pluginName>.jar`

## to-do ##

- Symlink command, linking to plugin directory, takes server root as arg


## Example usage ##

	$ python manage.py sort
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


	$ python manage.py report nms
	INFO:BookExploitFix v0.5 requires nms: 1_8_R2, 1_8_R1
	INFO:bPermissions v2.10.9m requires nms: 
	INFO:CombatTag v6.3.0-SNAPSHOT requires nms: 1_8_R1
	INFO:CommandBlock v2.0 requires nms: 
	INFO:CommandHelper v3.3.1-SNAPSHOT.2822- requires nms: 
	INFO:NoCheatPlus v3.12.0-BETA2-sASO-b813 requires nms: 1_8_R1, 1_4_R1, 1_7_R1, 1_6_R1, 1_8_R2, 1_6_R3, 1_6_R2, 1_7_R4, 1_7_R2, 1_5_R1, 1_5_R2, 1_5_R3, 1_4_5, 1_4_6, 1_7_R3
	INFO:NoSpawnerChange v1.0 requires nms: 
	INFO:OpenInv v2.2.8 requires nms: 1_8_R1, 1_4_R1, 1_7_R1, 1_6_R1, 1_6_R3, 1_6_R2, 1_7_R4, 1_7_R2, 1_7_R3, 1_5_R2, 1_5_R3, 1_4_5, 1_4_6
	INFO:WorldBorder v1.7.9 requires nms: 
	INFO:WorldEdit v6.0.2-SNAPSHOT;no_git_id requires nms: 1_8_R1, 1_7_R4, 1_7_R2, 1_7_R3, 1_6_R3
	INFO:WorldGuard v6.0.0-beta-05.1569- requires nms: