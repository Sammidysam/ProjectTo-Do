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
			+ "  In the blacklist, each folder name is separated by one comma [,].  For example, in the default value of blacklist there is one item:  \".metadata\"."
			+ "  You can add a new item by adding a comma then the name of your new item, a la changing it to \".metadata,.git\" to add \".git\" to the blacklist."
			+ "\n\nYou can further edit the settings in <i>" + fileutils.getInstallLocation() + os.sep + 'todo.json' + "</i> or inside the program.")
		self.helpLabel.set_line_wrap(True)
		self.helpLabel.set_use_markup(gtk.TRUE)

		# add components
		self.helpLabel.show()
		self.close.show()
		self.helpvbox.add(self.helpLabel)
		self.helpvbox.add(self.close)
		self.helpvbox.show()
		self.helpWindow.add(self.helpvbox)
		self.helpWindow.show()

	# rebuild the to-do view
	def rebuildToDo(self):
		# destroy current scroll box
		self.scrollbox.destroy()

		# add incomplete label
		incompleteLabel = gtk.Label("<b>Incomplete</b>")
		incompleteLabel.set_use_markup(gtk.TRUE)
		incompleteLabel.show()
		self.scrollbox.add(incompleteLabel)

		# rebuild to-do list viewer
		incomplete = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'incomplete')
		done = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'complete')
		# create incomplete check boxes
		for x in range(0, len(incomplete)):
			item = gtk.HBox(False, 10)
			check = gtk.CheckButton(None)
			check.connect("toggled", self.finished, incomplete[x])
			check.show()
			item.pack_start(check, False, False, 0)
			checkentry = gtk.Entry(0)
			checkentry.select_region(0, len(checkentry.get_text()))
			checkentry.set_text(incomplete[x])
			checkentry.connect("activate", self.updateJson, checkentry, False, incomplete[x])
			checkentry.show()
			item.pack_start(checkentry, True, True, 0)
			item.show()
			self.scrollbox.add(item)
	
		# only show the complete label and items if there are complete items
		if len(fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')['complete']) > 0:
			# add label
			completeLabel = gtk.Label("<b>Complete</b>")
			completeLabel.set_use_markup(gtk.TRUE)
			completeLabel.show()
			self.scrollbox.add(completeLabel)

			# create complete check boxes
			for x in range(0, len(done)):
				check = gtk.CheckButton(done[x])
				check.set_active(gtk.TRUE)
				check.connect("toggled", self.toggleChecked, None)
				check.show()
				self.scrollbox.add(check)

		# re-show scroll box
		self.scrollbox.show()
		self.scroll.add_with_viewport(self.scrollbox)
		self.scroll.show()

	# called when the project dropdown is used
	def switchProject(self, combobox):
		self.selected = combobox.get_active()
		self.window.set_title("To-Do Lists - " + self.projects[combobox.get_active()])
		if os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
			self.createItem.show()
			self.removeItem.show()
			self.notFound.hide()
			self.createButton.hide()
			self.rebuildToDo()
		else:
			self.createItem.hide()
			self.removeItem.hide()
			self.scroll.hide()
			self.notFound.show()
			self.createButton.show()

	# create a todo list for the specified item in the list
	def createToDo(self, widget, data=None):
		json = {'complete': [], 'incomplete': [], 'archive': []}
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')

	# switch item from unfinished to finished
	def finished(self, widget, *data):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['incomplete'].remove(data[0])
		json['complete'].append(data[0])
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.rebuildToDo()
	
	# keep checkbox active
	def toggleChecked(self, widget, data=None):
		widget.set_active(gtk.TRUE)

	# add new item to list
	def newItem(self, widget, data=None):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['incomplete'].append('New Item')
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.rebuildToDo()

	# update existing text for item
	def updateJson(self, widget, entry, *data):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		if data[0]:
			json['complete'][json['complete'].index(data[1])] = entry.get_text()
		else:
			json['incomplete'][json['incomplete'].index(data[1])] = entry.get_text()
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.rebuildToDo()

	# clear completed tasks
	def clear(self, widget, data=None):
		json = fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		json['archive'] += json['complete']
		json['complete'] = []
		fileutils.writeJson(json, fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')
		self.rebuildToDo()

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
			whitespace = gtk.Label(None)
			whitespace.show()
			self.vbox.add(whitespace)

			# create project hub entry box, label, and checkbox
			self.hubbox = gtk.HBox(False, 10)
			self.projectLabel = gtk.Label("Project Hub:")
			self.labelLength = self.projectLabel.size_request()
			self.hubentry = gtk.Entry(0)
			self.hubentry.select_region(0, len(self.hubentry.get_text()))
			self.hubentry.set_text(str(fileutils.parseJson(fileutils.defaultJson, 'projecthub')))
			self.projectLabel.show()
			self.hubentry.show()
			self.hubbox.add(self.projectLabel)
			self.hubbox.add(self.hubentry)
			
			# create blacklist entry box, label, and checkbox
			self.blackbox = gtk.HBox(False, 10)
			self.blackLabel = gtk.Label("Blacklist:")
			self.blackentry = gtk.Entry(0)
			self.blackentry.select_region(0, len(self.blackentry.get_text()))
			defaultBlacklist = fileutils.parseJson(fileutils.defaultJson, 'blacklist')
			combined = defaultBlacklist[0]
			for x in range(1, len(defaultBlacklist)):
				combined += ',' + defaultBlacklist[x]
			self.blackentry.set_text(combined)
			self.blackLabel.show()
			self.blackentry.show()
			self.blackbox.add(self.blackLabel)
			self.blackbox.add(self.blackentry)

			# add horizontal boxes to vertical box
			self.hubbox.show()
			self.blackbox.show()
			self.vbox.add(self.hubbox)
			self.vbox.add(self.blackbox)

			# add help button
			self.help = gtk.Button("Help")
			self.help.connect("clicked", self.helpCall, None)
			self.help.show()
			self.vbox.add(self.help)

			# create cancel and OK buttons
			self.cancel = gtk.Button("Cancel")
			self.cancel.connect("clicked", self.cancelCall, None)
			self.OK = gtk.Button("OK")
			self.OK.connect("clicked", self.okCall, None)

			# add some whitespace
			whitespace = gtk.Label(None)
			whitespace.show()
			self.vbox.add(whitespace)

			# put buttons in hbox and add to vbox
			self.buttonbox = gtk.HBox(False, 10)
			self.cancel.show()
			self.OK.show()
			self.buttonbox.add(self.cancel)
			self.buttonbox.add(self.OK)
			self.buttonbox.show()
			self.vbox.add(self.buttonbox)
			
			# add vertical box to window
			self.vbox.show()
			self.window.add(self.vbox)
		else:
			# create vbox for entire display
			self.vbox = gtk.VBox(False, 10)

			# create hbox for dropdown and some buttons
			self.buttonbox = gtk.HBox(False, 10)

			# create combobox for projects (dropdown)
			self.projselect = gtk.combo_box_new_text()

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

			# add project buttons to project vbox
			for x in range(0, len(self.projects)):
				self.projselect.append_text(self.projects[x])

			# add create and delete buttons
			self.createItem = gtk.Button("Add Item")
			self.createItem.connect("clicked", self.newItem, None)
			self.removeItem = gtk.Button("Clear Complete")
			self.removeItem.connect("clicked", self.clear, None)
			if os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
				self.createItem.show()
				self.removeItem.show()

			# preventing errors by initializing variables before switchProject() is called
			# it is called when it is connected to the dropdown

			# add scrolled window for check list
			self.scroll = gtk.ScrolledWindow()
			self.scroll.set_border_width(0)
			self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

			# create not found label
			self.notFound = gtk.Label("No To-Do list found in\n<i>" + fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json' + "</i>!")
			self.notFound.set_use_markup(gtk.TRUE)

			# create a button to create a to-do list
			self.createButton = gtk.Button("<b>Create To-Do List</b>")
			self.createButton.child.set_use_markup(gtk.TRUE)
			self.createButton.connect("clicked", self.createToDo, None)

			# finish dropdown
			self.projselect.connect('changed', self.switchProject)
			self.projselect.set_active(0)
			self.window.set_title("To-Do Lists - " + self.projects[self.projselect.get_active()])
			self.projselect.show()

			# add components to buttonbox
			self.buttonbox.add(self.projselect)

			# set some size requests
			self.ysize = self.projselect.size_request()[1]
			self.projselect.set_size_request(self.projselect.size_request()[0], self.ysize)
			self.createItem.set_size_request(self.createItem.size_request()[0], self.ysize)
			self.removeItem.set_size_request(self.removeItem.size_request()[0], self.ysize)
			
			# finish
			self.buttonbox.add(self.createItem)
			self.buttonbox.add(self.removeItem)

			# add buttonbox to vbox
			self.buttonbox.show()
			self.vbox.pack_start(self.buttonbox, False, False, 0)

			# create vbox for to-do list
			self.todoBox = gtk.VBox(False, 10)

			# display to-do list for selected item
			# get lists of items
			if os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
				incomplete = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'incomplete')
				done = fileutils.parseJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json', 'complete')

			# create vbox for scroll box
			# this vbox will hold all the components you can scroll through
			self.scrollbox = gtk.VBox(False, 10)

			# add label
			incompleteLabel = gtk.Label("<b>Incomplete</b>")
			incompleteLabel.set_use_markup(gtk.TRUE)
			incompleteLabel.show()
			self.scrollbox.add(incompleteLabel)

			if os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
				# create incomplete check boxes
				for x in range(0, len(incomplete)):
					item = gtk.HBox(False, 10)
					check = gtk.CheckButton(None)
					check.connect("toggled", self.finished, incomplete[x])
					check.show()
					item.pack_start(check, False, False, 0)
					checkentry = gtk.Entry(0)
					checkentry.select_region(0, len(checkentry.get_text()))
					checkentry.set_text(incomplete[x])
					checkentry.connect("activate", self.updateJson, checkentry, False, incomplete[x])
					checkentry.show()
					item.pack_start(checkentry, True, True, 0)
					item.show()
					self.scrollbox.add(item)
			
				# only show the complete label and items if there are complete items
				if len(fileutils.getJson(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json')['complete']) > 0:
					# add label
					completeLabel = gtk.Label("<b>Complete</b>")
					completeLabel.set_use_markup(gtk.TRUE)
					completeLabel.show()
					self.scrollbox.add(completeLabel)

					# create complete check boxes
					for x in range(0, len(done)):
						check = gtk.CheckButton(done[x])
						check.set_active(gtk.TRUE)
						check.connect("toggled", self.toggleChecked, None)
						check.show()
						self.scrollbox.add(check)

			# add scrollBox to scroll window
			# then show scrolled window
			self.scrollbox.show()
			self.scroll.add_with_viewport(self.scrollbox)
			self.scroll.show()

			# add scroll window to todoBox
			self.todoBox.add(self.scroll)

			# write that no to-do list is found
			# add notFound to todoBox
			self.notFound.show()
			self.todoBox.add(self.notFound)
			
			# add button to create to-do list
			self.createButton.show()
			self.todoBox.add(self.createButton)

			# hide necessary components
			if not os.path.isfile(fileutils.parseJson('todo.json', 'projecthub') + os.sep + self.projects[self.selected] + os.sep + 'todo.json'):
				self.scroll.hide()
			else:
				self.notFound.hide()
				self.createButton.hide()

			# add todo list viewer to hbox
			self.todoBox.show()
			self.vbox.add(self.todoBox)

			# add hbox to window
			self.vbox.show()
			self.window.add(self.vbox)
		
		# show window on screen
		self.window.show()

	# start gtk main method
	def main(self):
		gtk.main()

if __name__ == "__main__":
	# start program
	todo = ToDo()
	todo.main()
