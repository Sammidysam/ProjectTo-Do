#!/bin/bash

uninstall ()
{
	# remove installed files
	rm -rf /home/$USER/.todo
	rm /home/$USER/.local/share/applications/todo.desktop
	rm /home/$USER/.local/share/icons/todo.svg
	
	# check for errors
	if [ $? == 0 ];
	then
		echo "Uninstalled successfully!"
	else
		echo "Error in uninstallation!"
	fi
}

install ()
{
	# make necessary directories if needed
	mkdir -p /home/$USER/.todo
	mkdir -p /home/$USER/.local/share/applications
	mkdir -p /home/$USER/.local/share/icons
	cp src/*.py /home/$USER/.todo
	
	# create launch script
	echo "cd /home/$USER/.todo
python todo.py" > /home/$USER/.todo/launch.sh
	chmod +x /home/$USER/.todo/launch.sh

	# copy icon
	cp img/icon.svg /home/$USER/.local/share/icons/todo.svg
	
	# create launcher
	echo "[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=To-Do Lists
Exec=/home/$USER/.todo/launch.sh
Terminal=false
Categories=Utility;
Icon=todo" > /home/$USER/.local/share/applications/todo.desktop
	chmod +x /home/$USER/.local/share/applications/todo.desktop
	
	# check for errors
	if [ $? == 0 ];
	then
		echo "Installed successfully!"
	else
		echo "Error in installation!"
	fi
}

if [ "$1" == "uninstall" ];
then
	uninstall
else
	install
fi
