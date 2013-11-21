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

window = self.CreateWindow(48, 0, 450, 250, 'GxCalculator')

vbox1 = VBox(window.top_level_container, window, [])
window.AddWidget(vbox1)
window.display_label = Label(vbox1, window, "");
window.AddWidget(display_label, vbox1);

hbox1 = HBox(vbox1, window, [])
hbox2 = HBox(vbox1, window, [])
hbox3 = HBox(vbox1, window, [])
hbox4 = HBox(vbox1, window, [])
window.AddWidget(hbox1, vbox1)
window.AddWidget(hbox2, vbox1)
window.AddWidget(hbox3, vbox1)
window.AddWidget(hbox4, vbox1)

# Top row of calculator buttons
button_7 = Button(hbox1, window, "7", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '7')")
button_8 = Button(hbox1, window, "8", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '8')")
button_9 = Button(hbox1, window, "9", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '9')")
button_add = Button(hbox1, window, "+", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '+')")
window.AddWidget(button_7, hbox1)
window.AddWidget(button_8, hbox1)
window.AddWidget(button_9, hbox1)
window.AddWidget(button_add, hbox1)

# Second row of calculator buttons
button_4 = Button(hbox2, window, "4", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '4')")
button_5 = Button(hbox2, window, "5", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '5')")
button_6 = Button(hbox2, window, "6", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '6')")
button_minus = Button(hbox2, window, "-", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '-')")
window.AddWidget(button_4, hbox2)
window.AddWidget(button_5, hbox2)
window.AddWidget(button_6, hbox2)
window.AddWidget(button_minus, hbox2)

# Third row of calculator buttons
button_1 = Button(hbox3, window, "1", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '1')")
button_2 = Button(hbox3, window, "2", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '2')")
button_3 = Button(hbox3, window, "3", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '3')")
button_times = Button(hbox3, window, "*", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '*')")
window.AddWidget(button_1, hbox3)
window.AddWidget(button_2, hbox3)
window.AddWidget(button_3, hbox3)
window.AddWidget(button_times, hbox3)

# Fourth row of calculator buttons
button_0 = Button(hbox4, window, "0", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '0')")
button_dot = Button(hbox4, window, ".", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '.')")
button_clr = Button(hbox4, window, "CLR", "self.parent_window.display_label.SetLabelText('')")
button_divide = Button(hbox4, window, "/", "self.parent_window.display_label.SetLabelText(self.parent_window.display_label.GetLabelText() + '/')")
window.AddWidget(button_0, hbox4)
window.AddWidget(button_dot, hbox4)
window.AddWidget(button_clr, hbox4)
window.AddWidget(button_divide, hbox4)

# Lower HBox widgets
button_equals = Button(vbox1, window, "=", "self.parent_window.display_label.SetLabelText(eval(self.parent_window.display_label.GetLabelText()))")
window.AddWidget(button_equals, vbox1)
