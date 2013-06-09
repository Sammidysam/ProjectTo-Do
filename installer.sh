#!/bin/bash

uninstall ()
{
	rm -rf /home/$USER/.todo
	rm /home/$USER/.local/share/applications/todo.desktop
	rm /home/$USER/.local/share/icons/todo.svg
}

install ()
{
	mkdir -p /home/$USER/.todo
	mkdir -p /home/$USER/.local/share/applications
	mkdir -p /home/$USER/.local/share/icons
	cp src/*.py /home/$USER/.todo

	cp img/icon.svg /home/$USER/.local/share/icons/todo.svg
	
	echo "[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=To-Do Lists
Exec=python /home/$USER/.todo/todo.py
Terminal=false
Categories=Utility;
Icon=todo" > /home/$USER/.local/share/applications/todo.desktop
	chmod +x /home/$USER/.local/share/applications/todo.desktop
}

if [ "$1" == "uninstall" ];
then
	uninstall
else
	install
fi
