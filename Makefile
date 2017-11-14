all:
	rm plugin.xpi
	7z a -tzip plugin.xpi -w browser_plugin/.
