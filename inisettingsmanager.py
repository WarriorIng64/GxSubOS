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

import sys, os, ConfigParser

class INISettingsManager:

  def __init__(self):
    self.config = ConfigParser.ConfigParser()
    self.ini_file_opened = False

  def CheckIfINIFileExists(self, filename):
    # Returns true iff the given INI file exists.
    if os.path.isfile(filename):
      try:
        open(filename)
      except IOError:
        print("WARNING: '" + filename + "' does not exist.")
        return False
      return True
    print("WARNING: '" + filename + "' does not exist.")
    return False


  def OpenINIFile(self, filename):
    # Opens the file, assuming it exists
    try:
      self.config.readfp(open(filename))
      self.ini_file_opened = True
    except ConfigParser.Error:
      print("ERROR: '" + filename + "' could not be opened successfully.")
    except IOError:
      print("ERROR: '" + filename + "' could not be opened successfully.")

  def GetSections(self):
    # Gets the sections from the currently-opened INI file.
    sections = []
    if self.ini_file_opened:
      try:
        sections = self.config.sections()
        return sections
      except ConfigParser.Error:
        print("ERROR: could not retrieve sections from opened INI file.")
    else:
      print("WARNING: No INI file opened for retrieving sections.")
      return sections

  def GetValue(self, section, option):
    # Returns the value from the specified section and option.
    value = None
    if self.ini_file_opened:
      try:
        value = self.config.get(section, option)
        return sections
      except ConfigParser.Error:
        print("ERROR: could not get ('" + section + "','" + option + "') from opened INI file.")
    else:
      print("WARNING: No INI file opened for getting value.")
      return value
      
