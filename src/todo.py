#!/usr/bin/python

# for graphics
import pygtk
pygtk.require('2.0')
import gtk
import pango

# for manipulating files
import fileutils
import os

class ToDo:
	# default selected to-do list
	selected = 0

	# called when cancel button is clicked
	def cancelCall(self, widget, data=None):
		gtk.main_quit()

	# called when the OK button is clicked
	def okCall(self, widget, data=None):
		# retrieve entry from entry boxes
		# then turn it into json and write to file
		projecthub = self.hubentry.get_text()
		blacklist = self.blackentry.get_text().split(',')
		json = {'projecthub': projecthub,
				'blacklist': blacklist}
		fileutils.writeJson(json, 'todo.json')

		# destroy current window and make new one
		self.window.destroy()
		self.__init__()

	# called when help button is clicked
	def helpCall(self, widget, data=None):
		# create help window
		self.helpWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.helpWindow.connect("delete_event", lambda w, e: gtk.main_quit())
		self.helpWindow.set_border_width(10)
		self.helpWindow.set_title("Help")

		# create vbox for window
		self.helpvbox = gtk.VBox(False, 10)

		# create button to close window
		self.close = gtk.Button("Close")
		self.close.connect("clicked", lambda w, e: self.helpWindow.destroy(), None)

		# create help label
		self.helpLabel = gtk.Label("The currently shown items in the entry boxes are the default values of the variables."
			+ "  Feel free to change them.\n\nThe Project Hub is the location where all of your projects are."
			+ "  You must enter a path for it, such as the example in the box.\n\nThe blacklist is a list of folders that you do not want Project To-Do to generate a to-do list for."
			+ "  Two examples are shown, though you likely do not have either in your project hub, so you should remove them and add any folders that you do not want a to-do list for."
			+ "  In the blacklist, each folder name is separated by one comma [,].  For example, in the default value of blacklist there are two values:  \".git\" and \"secretproject\"."
			+ "\n\nYou can further edit the settings in <i>" + fileutils.getInstallLocation() + os.sep + 'todo.json' + "</i> or inside the program.")
		self.helpLabel.set_line_wrap(True)
		self.helpLabel.set_use_markup(gtk.TRUE)

		# add components
		self.helpvbox.add(self.helpLabel)
		self.helpvbox.add(self.close)
		self.helpWindow.add(self.helpvbox)
		self.helpWindow.show_all()

	# used to recreate the to-do window
	def redrawToDo(self):
		self.todoBox.destroy()
		self.createToDoView()
		self.window.show_all()

	# called when a project button is clicked
	def switchProject(self, widget, *data):
		self.selected = data[0]
		self.redrawToDo()

	# create a todo list for the specified item in the list
	def createToDo(self, widget, data=None):
		json = {'complete': [], 'incomplete': [], 'archive': []}
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.redrawToDo()

	# switch item from unfinished to finished
	def finished(self, widget, *data):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['incomplete'].remove(data[0])
		json['complete'].append(data[0])
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.redrawToDo()

	# keep checkbox active
	def toggleChecked(self, widget, data=None):
		widget.set_active(gtk.TRUE)

	# add new item to list
	def newItem(self, widget, data=None):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['incomplete'].append('New Item')
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.redrawToDo()

	# update existing text for item
	def updateJson(self, widget, entry, *data):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		if data[0]:
			json['complete'][json['complete'].index(data[1])] = entry.get_text()
		else:
			json['incomplete'][json['incomplete'].index(data[1])] = entry.get_text()
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.redrawToDo()

	# clear completed tasks
	def clear(self, widget, data=None):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['archive'] += json['complete']
		json['complete'] = []
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.redrawToDo()

	# create to-do viewer
	def createToDoView(self):
		# create vbox
		self.todoBox = gtk.VBox(False, 10)

		# add label to vbox
		self.todoLabel = gtk.Label("<b>To-Do List</b>")
		self.todoLabel.set_use_markup(gtk.TRUE)
		self.todoBox.pack_start(self.todoLabel, False, False, 0)

		# display to-do list for selected item
		# first check if to-do list exists
		if os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
			# get lists of items
			incomplete = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'incomplete')
			done = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'complete')
			
			# add scrolled window for check list
			self.scroll = gtk.ScrolledWindow()
			self.scroll.set_border_width(0)
			self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

			# create vbox for scroll box
			self.scrollbox = gtk.VBox(False, 10)

			# add label
			incompleteLabel = gtk.Label("<b>Incomplete</b>")
			incompleteLabel.set_use_markup(gtk.TRUE)
			self.scrollbox.pack_start(incompleteLabel, False, False, 0)

			# create variable used to get good size
			highx = 0

			# create incomplete check boxes
			for x in range(0, len(incomplete)):
				item = gtk.HBox(False, 10)
				check = gtk.CheckButton(None)
				check.connect("toggled", self.finished, incomplete[x])
				item.pack_start(check, False, False, 0)
				checkentry = gtk.Entry(max=0)
				checkentry.select_region(0, len(checkentry.get_text()))
				checkentry.set_text(incomplete[x])
				checkentry.connect("activate", self.updateJson, checkentry, False, incomplete[x])
				item.pack_start(checkentry, True, True, 0)
				self.scrollbox.pack_start(item, False, False, 0)
				if check.size_request()[0] + checkentry.size_request()[0] > highx:
					highx = check.size_request()[0] + checkentry.size_request()[0]
				highy = checkentry.size_request()[1]
			
			if len(fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')['complete']) > 0:
				# add label
				completeLabel = gtk.Label("<b>Complete</b>")
				completeLabel.set_use_markup(gtk.TRUE)
				self.scrollbox.add(completeLabel)

				# create complete check boxes
				for x in range(0, len(done)):
					check = gtk.CheckButton(done[x])
					check.set_active(gtk.TRUE)
					check.connect("toggled", self.toggleChecked, None)
					self.scrollbox.add(check)

			# add create and delete buttons
			self.itembox = gtk.HBox(False, 10)
			self.createItem = gtk.Button("Add Item")
			self.createItem.connect("clicked", self.newItem, None)
			self.removeItem = gtk.Button("Clear Complete")
			self.removeItem.connect("clicked", self.clear, None)
			self.itembox.add(self.createItem)
			self.itembox.add(self.removeItem)

			# add scrollBox to scroll window
			self.scroll.add_with_viewport(self.scrollbox)

			# request better size
			# this better size should prevent a horizontal scroll bar
			self.scroll.set_size_request(highx + 30, highy * 4)

			# add scroll window to todoBox
			self.todoBox.pack_start(self.scroll, True, True, 0)

			# add buttons at bottom
			self.todoBox.pack_start(self.itembox, False, False, 0)
		else:
			# write that no to-do list is found
			self.notFound = gtk.Label("No To-Do list found in\n<i>" + fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json' + "</i>!")
			self.notFound.set_use_markup(gtk.TRUE)
			self.todoBox.add(self.notFound)
			
			# add button to create to-do list
			self.createButton = gtk.Button("<b>Create To-Do List</b>")
			self.createButton.child.set_use_markup(gtk.TRUE)
			self.createButton.connect("clicked", self.createToDo, None)
			self.todoBox.add(self.createButton)

		# add todo list viewer to hbox
		self.hbox.pack_start(self.todoBox, True, True, 0)

	# initialize gui
	def __init__(self):
		# initialize window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", lambda w, e: gtk.main_quit())
		self.window.set_border_width(10)
		self.window.set_title("To-Do Lists")
		self.window.set_position(gtk.WIN_POS_CENTER)

		# set project hub and blacklist
		# only if configuration json does not exist
		if not os.path.isfile('todo.json'):
			# change title to preferences
			self.window.set_title("Preferences")

			# create setup vertical box
			self.vbox = gtk.VBox(False, 10)

			# add some whitespace
			self.vbox.add(gtk.Label(None))

			# create project hub entry box, label, and checkbox
			self.hubbox = gtk.HBox(False, 10)
			self.projectLabel = gtk.Label("Project Hub:")
			self.labelLength = self.projectLabel.size_request()
			self.hubentry = gtk.Entry(max=0)
			self.hubentry.select_region(0, len(self.hubentry.get_text()))
			self.hubentry.set_text(str(fileutils.parseJson(fileutils.defaultJson, 'projecthub')))
			self.hubbox.add(self.projectLabel)
			self.hubbox.add(self.hubentry)
			
			# create blacklist entry box, label, and checkbox
			self.blackbox = gtk.HBox(False, 10)
			self.blackLabel = gtk.Label("Blacklist:")
			self.blackLabel.set_size_request(self.labelLength[0], self.labelLength[1])
			self.blackentry = gtk.Entry(max=0)
			self.blackentry.select_region(0, len(self.blackentry.get_text()))
			defaultBlacklist = fileutils.parseJson(fileutils.defaultJson, 'blacklist')
			combined = defaultBlacklist[0]
			for x in range(1, len(defaultBlacklist)):
				combined += ',' + defaultBlacklist[x]
			self.blackentry.set_text(combined)
			self.blackbox.add(self.blackLabel)
			self.blackbox.add(self.blackentry)

			# add horizontal boxes to vertical box
			self.vbox.add(self.hubbox)
			self.vbox.add(self.blackbox)

			# add help button
			self.help = gtk.Button("Help")
			self.help.connect("clicked", self.helpCall, None)
			self.vbox.add(self.help)

			# create cancel and OK buttons
			self.cancel = gtk.Button("Cancel")
			self.cancel.connect("clicked", self.cancelCall, None)
			self.OK = gtk.Button("OK")
			self.OK.connect("clicked", self.okCall, None)

			# add some whitespace
			self.vbox.add(gtk.Label(None))

			# put buttons in hbox and add to vbox
			self.buttonbox = gtk.HBox(False, 10)
			self.buttonbox.add(self.cancel)
			self.buttonbox.add(self.OK)
			self.vbox.add(self.buttonbox)
			
			# add vertical box to window
			self.window.add(self.vbox)
		else:
			# create hbox for entire display
			self.hbox = gtk.HBox(False, 10)

			# create project changer
			# create projects vbox
			self.projectBox = gtk.VBox(False, 10)

			# add scrolled window for check list
			self.projscroll = gtk.ScrolledWindow()
			self.projscroll.set_border_width(0)
			self.projscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

			# create vbox for scroll box
			self.projscrollbox = gtk.VBox(False, 10)

			# add label to projects vbox
			self.projectLabel = gtk.Label("<b>Projects</b>")
			self.projectLabel.set_use_markup(gtk.TRUE)
			self.projectBox.pack_start(self.projectLabel, False, False, 0)

			# add all projects into array projects
			# ignore blacklist items
			self.projects = []
			for x in range(0, len(fileutils.getSubdirs(fileutils.parseJson('todo.json', 'projecthub')))):
				match = False
				for y in range(0, len(fileutils.parseJson('todo.json', 'blacklist'))):
					if fileutils.getSubdirs(fileutils.parseJson('todo.json', 'projecthub'))[x] == fileutils.parseJson('todo.json', 'blacklist')[y]:
						match = True
				if not match:
					self.projects.append(fileutils.getSubdirs(fileutils.parseJson('todo.json', 'projecthub'))[x])

			# create variables for finding largest x and y
			highx = 0
			highy = 0

			# add project buttons to project vbox
			for x in range(0, len(self.projects)):
				projectButton = gtk.Button(self.projects[x])
				projectButton.connect("clicked", self.switchProject, x)
				self.projscrollbox.pack_start(projectButton, True, True, 0)
				if projectButton.size_request()[0] > highx:
					highx = projectButton.size_request()[0]
				if projectButton.size_request()[1] > highy:
					highy = projectButton.size_request()[1]

			# add scrollbox to scroll area
			self.projscroll.add_with_viewport(self.projscrollbox)

			# set a size request
			# due to a bug where scroll bar does not detect necessary size
			# this request results in a nice size
			self.projscroll.set_size_request(highx + 20, highy * 5 + 60)

			# add scroll area to vbox
			self.projectBox.pack_start(self.projscroll, True, True, 0)

			# add vbox to hbox
			self.hbox.pack_start(self.projectBox, False, False, 0)

			# run method to make to-do viewer
			self.createToDoView()

			# add hbox to window
			self.window.add(self.hbox)
		
		# show window on screen
		self.window.show_all()

	# start gtk main method
	def main(self):
		gtk.main()

if __name__ == "__main__":
	# start program
	todo = ToDo()
	todo.main()
