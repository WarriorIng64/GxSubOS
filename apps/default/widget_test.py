# This file is part of GxSubOS.
# Copyright (C) 2013 Christopher Kyle Horton <christhehorton@gmail.com>

# GxSubOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GxSubOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GxSubOS. If not, see <http://www.gnu.org/licenses/>.

widget_test = self.CreateWindow(48, 0, 450, 250, 'Widget Test')
vbox1 = VBox(widget_test.top_level_container, widget_test, [])
widget_test.AddWidget(vbox1)

hbox_bottom = HBox(vbox1, widget_test, [])
hbox_top = HBox(vbox1, widget_test, [])
widget_test.AddWidget(hbox_top, vbox1)
widget_test.AddWidget(hbox_bottom, vbox1)

# Top HBox widgets
top_button = Button(hbox_top, widget_test, "Create new window", "self.parent_window.wm.CreateWindow(48, 0, 400, 400, 'Spawned by button')")
top_label = Label(hbox_top, widget_test, "Click to make a new window")
widget_test.AddWidget(top_button, hbox_top)
widget_test.AddWidget(top_label, hbox_top)

# Lower HBox widgets
left_button = Button(hbox_bottom, widget_test, "Left test button", "print 'Left test button clicked!'")
right_button = Button(hbox_bottom, widget_test, "Right test button", "print 'Right test button clicked!'")
empty_space = EmptyWidget(hbox_bottom, widget_test)
widget_test.AddWidget(left_button, hbox_bottom)
widget_test.AddWidget(empty_space, hbox_bottom)
widget_test.AddWidget(right_button, hbox_bottom)
