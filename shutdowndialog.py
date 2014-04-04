# This file is part of GxSubOS.
# Copyright (C) 2014 Christopher Kyle Horton <christhehorton@gmail.com>

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

shutdown_dialog_width = 400
shutdown_dialog_height = 200
shutdown_dialog_x = pygame.display.Info().current_w / 2 - shutdown_dialog_width / 2
shutdown_dialog_y = pygame.display.Info().current_h / 2 - shutdown_dialog_height / 2

shutdown_dialog = self.CreateWindow(shutdown_dialog_x, shutdown_dialog_y, shutdown_dialog_width, shutdown_dialog_height, 'Shutdown')
shutdown_dialog.icon_image = pygame.image.load("graphics/shutdown.png")

vbox1 = VBox(shutdown_dialog.top_level_container, shutdown_dialog, [])
shutdown_dialog.AddWidget(vbox1)

top_label = Label(vbox1, shutdown_dialog, "Are you sure you want to shutdown GxSubOS?")
shutdown_dialog.AddWidget(top_label, vbox1)

hbox_buttons = HBox(vbox1, shutdown_dialog, [])
hbox_buttons.RequestHeight(64)
shutdown_dialog.AddWidget(hbox_buttons, vbox1)

yes_button = Button(hbox_buttons, shutdown_dialog, "Yes", "pygame.quit();sys.exit()")
no_button = Button(hbox_buttons, shutdown_dialog, "No", "self.parent_window.window_closed = True")
shutdown_dialog.AddWidget(yes_button, hbox_buttons)
shutdown_dialog.AddWidget(no_button, hbox_buttons)
