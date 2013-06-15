# ProjectTo-Do

A Python program, designed for Linux, that manages to-do lists for your various projects.  It has been tested so far on three computers running Fedora 18 and all successfully ran it.  It could possibly run on Windows, but to do so requires installing pyGTK which doesn't come with Windows which would be very annoying.

## Running and Installing

To run the local copy, navigate to the project directory and run

`python src/todo.py`

To install the program, navigate to the project directory and run

`./install.sh`

After installing, if you are on Fedora and you navigate to your GNOME Shell activities menu and click show applications, the application will be installed under the name `To-Do Lists`.  You can also go to the category `Accessories` to find it.

The program installation requires **no** admin rights because its desktop file will be installed to the user directory for installing applications `~/.local` and its source code will be stored in `~/.todo`.  This means that you have to install separately for each user, however.

## How to Use

After opening, you will need to set your preferences.  In so are the items:

- Program Settings
	- Project Hub
	- Blacklist
- Window Settings
	- X Size
	- Y Size

The project hub is the absolute path where all of your project folders are, and the blacklist is any folders in that project hub that you don't want to be in your dropdown menu.  In the entry boxes will be the defaults.  The defaults are, for the Program Settings, the items I prefer, and for the Window Settings, the sizes I feel would be most convenient for the user.  The preferences will be saved to `~/.todo/conf.json`.  Then you will be able to use the program.  If you create a to-do list, it will be saved in `the project folder/.todo.json` or `project hub/project folder/.todo.json` as another way to visualize it.  As an example, if I have my project hub as `/home/sam/Documents/Workspace` and I create a to-do list for my project `StudyHelper`, the to-do list will be stored in `/home/sam/Documents/Workspace/StudyHelper/.todo.json`.  After creating a to-do list, you can add items, check them off, and clear your completed items.  When you clear your completed items, they are moved to the array `archive` on the JSON file so that you can revisit your old finished items.

## Screenshots

These screenshots were taken at the point of [this commit](https://github.com/Sammidysam/ProjectTo-Do/commit/f3ae47ff05357f5f25c326544feea201381e37c9).

![Interface 1](http://s15.postimg.org/dyn5p0mcb/screenshot0.png)

![Interface 2](http://s22.postimg.org/omcnt6wmp/screenshot2.png)

![Dropdown](http://s24.postimg.org/nafmyu079/screenshot1.png)

## Contributors

- [Sammidysam](https://github.com/Sammidysam)
	- Whole program in Python
- [four04](https://github.com/four04)
	- Install script
	- Icon image

### How to Contribute

This project is nearly done--likely from here on out only very small updates will come by.  If you would like to add features or layout changes to ProjectTo-Do, you can do so by forking the repository and adding a pull request with your changes.  I will then review them and try them out.  If they work nicely I will merge them.

## Reporting Bugs or Suggesting Features

If you have encountered a bug or want to suggest a feature, head over to the [issues page](https://github.com/Sammidysam/ProjectTo-Do/issues?state=open) and create a new issue.  If it is a bug, label it with the tag `bug` and if it is a suggestion for improvement label it with the tag `enhancement`.  Then just write your message and I will review it and give feedback.
