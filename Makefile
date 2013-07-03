bin=bin
src=src

binary=project-todo

all: $(src)/todo.vala
	valac --pkg gtk+-3.0 -o $(bin)/$(binary) $(src)/todo.vala
