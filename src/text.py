#! /usr/bin/python

# for curses stuff
import curses
import curses.panel

# for file manipulation stuff
import fileutils
import os

projectList = []

selectedProject = 0

def createProjectsList():
	global projectList
	
	for x in range(0, len(fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub")))):
		match = False
		
		for y in range(0, len(fileutils.parseJson("conf.json", "blacklist"))):
			if fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub"))[x] == fileutils.parseJson("conf.json", "blacklist")[y]:
				match = True
				
		if not match:
			projectList.append(fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub"))[x])

def drawSelectWin():
	global projectList
	global selectedProject
	
	global selectWin

	selectWin.clear()

	for x in range(0, len(projectList)):
		if x == selectedProject:
			selectWin.standout()
			
		selectWin.addstr(0 + x, 0, projectList[x])
		
		if x == selectedProject:
			selectWin.standend()

def drawListWin():
	global projectList
	global selectedProject

	global listWin

	listWin.clear()

	fileName = fileutils.parseJson("conf.json", "projecthub") + os.sep + projectList[selectedProject] + os.sep + ".todo.json"

	if not os.path.isfile(fileName):
		listWin.addstr(0, (listWin.getmaxyx()[1] / 2) - (len("No to-do list found!") / 2), "No to-do list found!")
		listWin.addstr(1, (listWin.getmaxyx()[1] / 2) - (len("Expected to-do list at") / 2), "Expected to-do list at")
		listWin.addstr(2, (listWin.getmaxyx()[1] / 2) - (len(str(fileName)) / 2) if listWin.getmaxyx()[1] > len(str(fileName)) else 0, str(fileName))
	else:
		listWin.addstr(0, (listWin.getmaxyx()[1] / 2) - (len("Incomplete") / 2), "Incomplete")
		
		currentLine = 1
		for x in range(0, len(fileutils.parseJson(fileName, "incomplete"))):
			listWin.addstr(currentLine, 2, fileutils.parseJson(fileName, "incomplete")[x])
			currentLine += len(fileutils.parseJson(fileName, "incomplete")[x]) / (listWin.getmaxyx()[1] - 3) + 1

		currentLine += 1
		listWin.addstr(currentLine, (listWin.getmaxyx()[1] / 2) - (len("Complete") / 2), "Complete")
		currentLine += 1

		#for x in range(0, len(fileutils.parseJson(fileName)))

def main(screen):
	global projectList
	global selectedProject

	global selectWin
	global listWin
	
	# set up projects list
	createProjectsList()
	
	# set up window
	screen.box()
	screen.hline(2, 1, curses.ACS_HLINE, screen.getmaxyx()[1] - 2)
	screen.addstr(1, (screen.getmaxyx()[1] / 2) - (len("To-Do Lists") / 2), "To-Do Lists")

	selectWin = screen.subwin(screen.getmaxyx()[0] - 4, (screen.getmaxyx()[1] - 1) / 2 - 1, 3, 1)
	listWin = screen.subwin(screen.getmaxyx()[0] - 4, (screen.getmaxyx()[1] - 1) / 2, 3, screen.getmaxyx()[1] / 2)
	
	screen.vline(3, (screen.getmaxyx()[1] - 1) / 2, curses.ACS_VLINE, screen.getmaxyx()[0] - 4)

	drawSelectWin()
	drawListWin()

	curses.curs_set(False)
		
	screen.refresh()

	running = True
	
	while running:
		key = chr(screen.getch())
		if key == 'q' or key == chr(27):
			running = False
		elif key == 'w':
			if selectedProject > 0:
				selectedProject -= 1
				
				drawSelectWin()
				selectWin.refresh()

				drawListWin()
				listWin.refresh()
		elif key == 's':
			if selectedProject < len(projectList) - 1:
				selectedProject += 1
				
				drawSelectWin()
				selectWin.refresh()

				drawListWin()
				listWin.refresh()
