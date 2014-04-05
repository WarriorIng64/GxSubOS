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


# Button and frame code

button_code = """
if len(self.parent_window.subprocesses) == 0:
  import setup
  self.parent_window.subprocesses = setup.Setup()
  self.parent_window.total_updates = len(self.parent_window.subprocesses)
else:
  self.parent_window.wm.ShowPopupMessage("Updates in Progress", "The current updates must complete before you can check again.")
"""

update_frame_code = """
if len(self.subprocesses) != 0:
  updates_completed = self.total_updates - len(self.subprocesses)
  self.SetStatusbarText("Updating; " + str(updates_completed) + "/" + str(self.total_updates) + " updates completed")
  for sp in self.subprocesses:
    if sp.poll() != None:
      self.subprocesses.remove(sp)
else:
  self.SetStatusbarText("Ready")
"""

# Window and UI code

window = self.CreateWindow(48, 0, 300, 100, 'Updater')
window.SetSpecificIcon("graphics/updater.png")
window.subprocesses = []
window.total_updates = 0

vbox1 = VBox(window.top_level_container, window, [])
window.AddWidget(vbox1)

button_update = Button(vbox1, window, "Update", button_code)
window.AddWidget(button_update, vbox1)

window.SetFrameCode(update_frame_code)
