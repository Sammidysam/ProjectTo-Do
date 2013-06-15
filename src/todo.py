#!/usr/bin/python

# for graphics
import pygtk
pygtk.require("2.0")
import gtk

# for manipulating files
import fileutils
import os

# check if in right directory
if os.getcwd() == fileutils.getHome() and os.path.isdir(".todo"):
	os.chdir(".todo")

class ToDo:
	# default selected to-do list
	selected = 0

	# current mode: preferences (0) or gui (1)
	mode = 0

	# saves the contents of all entry boxes in incomplete
	def saveEntries(self):
		for x in range(0, len(self.incomplete.get_children())):
			for y in range(0, len(self.incomplete.get_children()[x].get_children())):
				if isinstance(self.incomplete.get_children()[x].get_children()[y], gtk.Entry):
					self.incomplete.get_children()[x].get_children()[y].activate()

	# called when window quits
	def quit(self, widget, event, data=None):
		# loop through incomplete to-do items
		# then, run the activate method on the entry boxes
		# this will update the JSON
		# so that your changes are saved when closing
		if self.mode != 0 and os.path.isfile(self.getToDoList()):
			self.saveEntries()

		# quit the program
		gtk.main_quit()
		return False

	# returns the current to-do list being processed
	def getToDoList(self):
		return self.currentList

	# called when the OK button is clicked
	def okCall(self, widget, data=None):
		# retrieve entry from entry boxes
		# then turn it into json and write to file
		projecthub = self.hubentry.get_text()
		blacklist = self.blackentry.get_text().split(',')
		sizeX = self.xsizeentry.get_text()
		sizeY = self.ysizeentry.get_text()
		screen = gtk.gdk.display_get_default().get_default_screen()
		if int(sizeX) < 0 or int(sizeX) > screen.get_width():
			print "Invalid sizeX; using default..."
			sizeX = fileutils.parseJson(fileutils.defaultJson, "sizeX")
		if int(sizeY) < 0 or int(sizeY) > screen.get_height():
			print "Invalid sizeY; using default..."
			sizeY = fileutils.parseJson(fileutils.defaultJson, "sizeY")
		json = {"projecthub": projecthub,
				"blacklist": blacklist,
				"sizeX": sizeX,
				"sizeY": sizeY}
		fileutils.writeJson(json, "conf.json")

		# destroy current window and make new one
		self.window.destroy()
		self.__init__()

	# called when help button is clicked
	def helpCall(self, widget, data=None):
		# create help window
		self.helpWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.helpWindow.connect("delete_event", lambda w, e: self.helpWindow.destroy())
		self.helpWindow.set_border_width(10)
		self.helpWindow.set_title("Help")

		# create vbox for window
		self.helpvbox = gtk.VBox(False, 10)
		self.helpLabel = gtk.Label(None)
		self.close = gtk.Button("Close")

		# help vbox
		self.helpWindow.add(self.helpvbox)

		# create help label
		self.helpLabel.set_text("The currently shown items in the entry boxes are the default values of the variables."
			+ "  Feel free to change them.\n\n<b>Program Settings</b>\nThe project hub is the location where all of your projects are."
			+ "  You must enter a path for it, such as the example in the box.\n\nThe blacklist is a list of folders that you do not want ProjectTo-Do to manage a to-do list for."
			+ "  In the blacklist, each folder name is separated by one comma [,].  For example, in the default value of blacklist there is one item:  \".metadata\"."
			+ "  You can add a new item by adding a comma then the name of your new item, for example, changing it to \".metadata,.git\" to add \".git\" to the blacklist."
			+ "\n\n<b>Window Settings</b>\nThe two variables are pretty self-explanatory.  The two defaults are the values that I think will be most convenient."
			+ "  Setting a value to \"0\" will result in the window not being resized at all; it will be the size that all of its components require"
			+ "\n\nYou can further edit the settings in <i>" + fileutils.getInstallLocation() + os.sep + "conf.json" + "</i>.")
		self.helpLabel.set_line_wrap(True)
		self.helpLabel.set_use_markup(gtk.TRUE)
		self.helpvbox.add(self.helpLabel)

		# create button to close window
		self.close.connect("clicked", lambda w, e: self.helpWindow.destroy(), None)
		self.helpvbox.add(self.close)

		# show components
		self.helpvbox.show()
		self.helpLabel.show()
		self.close.show()
		self.helpWindow.show()

	# called when the project dropdown is used
	def switchProject(self, combobox):
		if isinstance(combobox, gtk.ComboBox):
			self.selected = combobox.get_active()
		else:
			self.selected = combobox
		if os.path.isfile("conf.json"):
			# save entry boxes if necessary
			if os.path.isfile(self.getToDoList()):
				self.saveEntries()
			self.currentList = fileutils.parseJson("conf.json", "projecthub") + os.sep + self.projects[self.selected] + os.sep + ".todo.json"
			if isinstance(combobox, gtk.ComboBox):
				self.window.set_title("To-Do Lists - " + self.projects[combobox.get_active()])
			else:
				self.window.set_title("To-Do Lists - " + self.projects[combobox])

		if os.path.isfile(self.getToDoList()):
			# show and hide necessary components
			self.addItem.show()
			self.clearComplete.show()
			self.notFound.hide()
			self.createButton.hide()

			# rebuild scrollbox
			# get incomplete and complete lists
			incomplete = fileutils.parseJson(self.getToDoList(), "incomplete")
			done = fileutils.parseJson(self.getToDoList(), "complete")

			# remove old items
			for x in range(0, len(self.incomplete.get_children())):
				self.incomplete.remove(self.incomplete.get_children()[0])

			for x in range(0, len(self.complete.get_children())):
				self.complete.remove(self.complete.get_children()[0])

			# add new items
			for x in range(0, len(fileutils.parseJson(self.getToDoList(), "incomplete"))):
				item = gtk.HBox(False, 10)

				# declare items
				check = gtk.CheckButton(None)
				checkentry = gtk.Entry(0)

				# adjust items
				check.connect("toggled", self.finished, incomplete[x], checkentry, item)
				check.show()
				item.pack_start(check, False, False, 0)
				checkentry.select_region(0, len(checkentry.get_text()))
				checkentry.set_text(incomplete[x])
				checkentry.connect("activate", self.updateJson, checkentry, incomplete[x])
				checkentry.show()
				item.pack_start(checkentry, True, True, 0)
				item.show()
				self.incomplete.pack_start(item, False, False, 0)

			# show that there are no to-do list items if there are none
			# hide otherwise
			if len(self.incomplete.get_children()) == 0:
				self.noneLabel.show()
			else:
				self.noneLabel.hide()

			for x in range(0, len(fileutils.parseJson(self.getToDoList(), "complete"))):
				check = gtk.CheckButton(done[x])
				check.set_active(gtk.TRUE)
				check.connect("toggled", lambda w, d: w.set_active(gtk.TRUE), None)
				check.show()
				self.complete.pack_start(check, False, False, 0)

			# hide label if there are no complete items
			# show it otherwise
			if len(self.complete.get_children()) == 0:
				self.completeLabel.hide()
			else:
				self.completeLabel.show()

			# show scrolled window
			self.scroll.show()
		else:
			# show and hide necessary components
			self.addItem.hide()
			self.clearComplete.hide()
			self.scroll.hide()

			# adjust notFound
			self.notFound.set_text("No To-Do list found in\n<i>" + self.getToDoList() + "</i>!")
			self.notFound.set_use_markup(gtk.TRUE)

			# finish
			self.notFound.show()
			self.createButton.show()

	# create a to-do list for the specified item in the list
	def createToDo(self, widget, data=None):
		# create empty to-do list
		json = {"complete": [], "incomplete": [], "archive": []}
		fileutils.writeJson(json, self.getToDoList())

		# hide and show necessary components
		self.addItem.show()
		self.clearComplete.show()
		self.notFound.hide()
		self.createButton.hide()

		# remove old gui
		# if not done, the old to-do list's contents would appear
		for x in range(0, len(self.incomplete.get_children())):
			self.incomplete.remove(self.incomplete.get_children()[0])

		for x in range(0, len(self.complete.get_children())):
			self.complete.remove(self.complete.get_children()[0])

		# show no items in to-do list
		self.noneLabel.show()

		# hide complete items label
		self.completeLabel.hide()

		# show gui
		self.scroll.show()

	# switch item from unfinished to finished
	def finished(self, widget, *data):
		# data[0] is the text when initialized
		# data[1] is the entry box next to the check box
		# data[2] is the hbox the check and entry boxes are in
		json = fileutils.getJson(self.getToDoList())
		# checks if the entry text does not equal the initial text
		if data[1].get_text() != data[0]:
			json["incomplete"].remove(data[0])
			json["complete"].append(data[1].get_text())
		else:
			json["incomplete"].remove(data[1].get_text())
			json["complete"].append(data[1].get_text())

		# remove hbox from incomplete
		self.incomplete.remove(data[2])

		# show noneLabel if no items on to-do list
		if len(self.incomplete.get_children()) == 0:
			self.noneLabel.show()

		# create check box in complete
		check = gtk.CheckButton(data[1].get_text())
		check.set_active(gtk.TRUE)
		check.connect("toggled", lambda w, d: w.set_active(gtk.TRUE), None)
		check.show()
		self.complete.add(check)

		# show complete label
		self.completeLabel.show()

		fileutils.writeJson(json, self.getToDoList())

	# add new item to list
	def newItem(self, widget, data=None):
		# add new item to to-do list file
		json = fileutils.getJson(self.getToDoList())
		json["incomplete"].append("New Item")
		fileutils.writeJson(json, self.getToDoList())

		# add new item to gui
		item = gtk.HBox(False, 10)

		# declare items
		check = gtk.CheckButton(None)
		checkentry = gtk.Entry(0)

		# adjust items
		check.connect("toggled", self.finished, "New Item", checkentry, item)
		check.show()
		item.pack_start(check, False, False, 0)
		checkentry.select_region(0, len(checkentry.get_text()))
		checkentry.set_text("New Item")
		checkentry.connect("activate", self.updateJson, checkentry, "New Item")
		checkentry.show()
		item.pack_start(checkentry, True, True, 0)
		item.show()
		self.incomplete.add(item)

		# hide noneLabel
		self.noneLabel.hide()

	# update existing text for item
	def updateJson(self, widget, entry, *data):
		json = fileutils.getJson(self.getToDoList())
		json["incomplete"][json["incomplete"].index(data[0])] = entry.get_text()
		fileutils.writeJson(json, self.getToDoList())

	# clear completed tasks
	def clear(self, widget, data=None):
		# update to-do list file
		json = fileutils.getJson(self.getToDoList())
		json["archive"] += json["complete"]
		json["complete"] = []
		fileutils.writeJson(json, self.getToDoList())

		# update gui
		# remove all items in complete
		for x in range(0, len(self.complete.get_children())):
			self.complete.remove(self.complete.get_children()[0])

		# hide complete label
		self.completeLabel.hide()

	# initialize gui
	def __init__(self):
		# initialize window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.quit)
		self.window.set_border_width(10)
		self.window.set_wmclass("To-Do Lists", "To-Do Lists")
		self.window.set_title("To-Do Lists")
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_icon_from_file("img" + os.sep + "icon.svg")
		self.window.set_resizable(True)

		# set mode
		# ternary operator used
		self.mode = 0 if not os.path.isfile("conf.json") else 1

		# set project list, current list being used by program
		self.projects = []
		self.currentList = ""
		if self.mode == 1:
			# create projects list
			for x in range(0, len(fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub")))):
				match = False
				for y in range(0, len(fileutils.parseJson("conf.json", "blacklist"))):
					if fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub"))[x] == fileutils.parseJson("conf.json", "blacklist")[y]:
						match = True
				if not match:
					self.projects.append(fileutils.getSubdirs(fileutils.parseJson("conf.json", "projecthub"))[x])

			# create current list
			self.currentList = fileutils.parseJson("conf.json", "projecthub") + os.sep + self.projects[self.selected] + os.sep + ".todo.json"

		# define all component variables
		# vbox for whole display
		self.vbox = gtk.VBox(False, 10)

		# preferences components
		self.programLabel = gtk.Label("<b>Program Settings</b>")
		self.hubbox = gtk.HBox(False, 10)
		self.projectLabel = gtk.Label("Project Hub:")
		self.hubentry = gtk.Entry(0)
		self.blackbox = gtk.HBox(False, 10)
		self.blackLabel = gtk.Label("Blacklist:")
		self.blackentry = gtk.Entry(0)
		self.windowLabel = gtk.Label("<b>Window Settings</b>")
		self.xsizebox = gtk.HBox(False, 10)
		self.xsizeLabel = gtk.Label("X Size:")
		self.xsizeentry = gtk.Entry(0)
		self.ysizebox = gtk.HBox(False, 10)
		self.ysizeLabel = gtk.Label("Y Size:")
		self.ysizeentry = gtk.Entry(0)
		self.help = gtk.Button("Help")
		self.botwhite = gtk.Label(None)
		self.prefButtons = gtk.HBox(False, 10)
		self.cancel = gtk.Button("Cancel")
		self.ok = gtk.Button("OK")

		# to-do viewer components
		self.viewButtons = gtk.HBox(False, 10)
		self.projselect = gtk.combo_box_new_text()
		self.addItem = gtk.Button("Add Item")
		self.clearComplete = gtk.Button("Clear Complete")
		self.notFound = gtk.Label("No To-Do list found in\n<i>" + self.getToDoList() + "</i>!")
		self.createButton = gtk.Button("<b>Create To-Do List</b>")
		self.scroll = gtk.ScrolledWindow()
		self.scrollbox = gtk.VBox(False, 10)
		self.incompleteLabel = gtk.Label("<b>Incomplete</b>")
		self.noneLabel = gtk.Label("No items in To-Do List!")
		self.incomplete = gtk.VBox(False, 10)
		self.completeLabel = gtk.Label("<b>Complete</b>")
		self.complete = gtk.VBox(False, 10)

		# now initialize components

		# initialize vbox
		self.window.add(self.vbox)

		# preference components initialization

		# label of program settings
		self.programLabel.set_use_markup(gtk.TRUE)
		self.vbox.add(self.programLabel)

		# hbox for project hub
		self.vbox.add(self.hubbox)

		# label and entry for project hub
		self.labelSize = self.projectLabel.size_request()
		self.hubbox.add(self.projectLabel)
		self.hubentry.set_text(fileutils.parseJson(fileutils.defaultJson, "projecthub"))
		self.hubbox.add(self.hubentry)

		# hbox for blacklist
		self.vbox.add(self.blackbox)

		# label and entry for blacklist
		self.blackLabel.set_size_request(self.labelSize[0], self.labelSize[1])
		self.blackbox.add(self.blackLabel)
		self.blackentry.set_text(fileutils.parseJson(fileutils.defaultJson, "blacklist")[0])
		self.blackbox.add(self.blackentry)
		
		# label of window settings
		self.windowLabel.set_use_markup(gtk.TRUE)
		self.vbox.add(self.windowLabel)

		# hbox for window's x size
		self.vbox.add(self.xsizebox)

		# label and entry for window's x size
		self.xsizeLabel.set_size_request(self.labelSize[0], self.labelSize[1])
		self.xsizebox.add(self.xsizeLabel)
		self.xsizeentry.set_text(fileutils.parseJson(fileutils.defaultJson, "sizeX"))
		self.xsizebox.add(self.xsizeentry)

		# hbox for window's y size
		self.vbox.add(self.ysizebox)

		# label and entry for window's y size
		self.ysizeLabel.set_size_request(self.labelSize[0], self.labelSize[1])
		self.ysizebox.add(self.ysizeLabel)
		self.ysizeentry.set_text(fileutils.parseJson(fileutils.defaultJson, "sizeY"))
		self.ysizebox.add(self.ysizeentry)

		# help button
		self.help.connect("clicked", self.helpCall, None)
		self.vbox.add(self.help)

		# whitespace
		self.vbox.add(self.botwhite)

		# hbox for cancel and ok buttons
		self.vbox.add(self.prefButtons)

		# cancel and okay buttons
		self.cancel.connect("clicked", lambda w, d: gtk.main_quit(), None)
		self.prefButtons.add(self.cancel)
		self.ok.connect("clicked", self.okCall, None)
		self.prefButtons.add(self.ok)

		# to-do viewer components initialization

		# dropdown, add item button, clear complete button box
		self.vbox.pack_start(self.viewButtons, False, False, 0)

		# dropdown
		for x in range(0, len(self.projects)):
			self.projselect.append_text(self.projects[x])
		self.projselect.set_active(0)
		self.projselect.connect("changed", self.switchProject)
		self.viewButtons.add(self.projselect)

		# add item button
		self.addItem.connect("clicked", self.newItem, None)
		self.viewButtons.add(self.addItem)

		# clear complete button
		self.clearComplete.connect("clicked", self.clear, None)
		self.viewButtons.add(self.clearComplete)

		# not found label
		self.notFound.set_use_markup(gtk.TRUE)
		self.vbox.add(self.notFound)

		# button to create to-do list
		self.createButton.child.set_use_markup(gtk.TRUE)
		self.createButton.connect("clicked", self.createToDo, None)
		self.vbox.add(self.createButton)

		# scroll box
		self.scroll.set_border_width(0)
		self.scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.vbox.add(self.scroll)

		# scroll box box
		self.scroll.add_with_viewport(self.scrollbox)

		# incomplete label
		self.incompleteLabel.set_use_markup(gtk.TRUE)
		self.scrollbox.pack_start(self.incompleteLabel, False, False, 0)

		# none label
		self.scrollbox.pack_start(self.noneLabel, False, False, 0)

		# incomplete list
		self.scrollbox.pack_start(self.incomplete, False, False, 0)

		# complete label
		self.completeLabel.set_use_markup(gtk.TRUE)
		self.scrollbox.pack_start(self.completeLabel, False, False, 0)

		# complete list
		self.scrollbox.pack_start(self.complete, False, False, 0)

		# do stuff only for specific mode
		if self.mode == 0:
			self.window.set_title("Preferences")
			self.programLabel.show()
			self.hubbox.show()
			self.projectLabel.show()
			self.hubentry.show()
			self.blackbox.show()
			self.blackLabel.show()
			self.blackentry.show()
			self.windowLabel.show()
			self.xsizebox.show()
			self.xsizeLabel.show()
			self.xsizeentry.show()
			self.ysizebox.show()
			self.ysizeLabel.show()
			self.ysizeentry.show()
			self.help.show()
			self.botwhite.show()
			self.prefButtons.show()
			self.cancel.show()
			self.ok.show()
		else:
			# set size request
			sizeX = int(fileutils.parseJson("conf.json", "sizeX"))
			sizeY = int(fileutils.parseJson("conf.json", "sizeY"))
			if sizeX == 0:
				sizeX = -1
			if sizeY == 0:
				sizeY = -1
			self.window.set_size_request(sizeX, sizeY)

			# show components
			self.viewButtons.show()
			self.projselect.show()
			if os.path.isfile(self.getToDoList()):
				self.switchProject(self.selected)
			else:
				self.notFound.show()
				self.createButton.show()

		# show no matter what
		self.scrollbox.show()
		self.incompleteLabel.show()
		self.incomplete.show()
		self.complete.show()

		# add vbox to window, display window
		self.vbox.show()
		self.window.show()

		print "Initialized successfully!"

	# start gtk main method
	def main(self):
		gtk.main()

if __name__ == "__main__":
	# start program
	todo = ToDo()
	todo.main()
