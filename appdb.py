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

import sys
import sqlite3

# This module was constructed with the help of this online tutorial:
# http://zetcode.com/db/sqlitepythontutorial/

class AppDB:
  def RetrieveAppNames(self):
    '''Retrieves a list of the names of all apps in the database.'''
    appslist = []
    con = self.Connect()
    with con:
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      try:
        cur.execute("SELECT AppName FROM Apps")
        rows = cur.fetchall()
        for row in rows:
          appslist.append(row["AppName"])
        return appslist
      except sqlite3.OperationalError:
        print "ERROR: AppDB.RetrieveAppNames() failed due to operational error."
        return []
  
  def InsertDefaultApps(self):
    '''Inserts the info for the default apps into the database.'''
    con = self.Connect()
    with con:
      cur = con.cursor()
      # Initial database setup
      cur.execute("DROP TABLE IF EXISTS Apps")
      cur.execute("CREATE TABLE Apps(AppId INT PRIMARY KEY, \
                   AppName TEXT, \
                   DefaultApp INTEGER, \
                   CurVersion TEXT, \
                   UpdateVersion TEXT, \
                   WebsiteUrl TEXT, \
                   RepoUrl TEXT)")
      # The default apps are currently hard-coded here
      values = (
        ('GxCalculator',True,'0.1','0.1','https://github.com/WarriorIng64/GxCalculator','https://github.com/WarriorIng64/GxCalculator.git'),
        ('GxWidgetTest',True,'0.1','0.1','https://github.com/WarriorIng64/GxWidgetTest','https://github.com/WarriorIng64/GxWidgetTest.git'),
        ('GxText',True,'0.1','0.1','https://github.com/WarriorIng64/GxText','https://github.com/WarriorIng64/GxText.git'),
        ('GxUpdater',True,'0.1','0.1','https://github.com/WarriorIng64/GxUpdater','https://github.com/WarriorIng64/GxUpdater.git')
      )
      fields = "AppName,DefaultApp,CurVersion,UpdateVersion,WebsiteUrl,RepoURL"
      for app in values:
        cur.executemany("INSERT INTO Apps(" + fields + ") VALUES(?, ?, ?, ?, ?, ?)", (app,))
      con.commit()
  
  def GetAppInfo(self, appname):
    '''Gets the info for the given app name as a dictionary.'''
    con = self.Connect()
    with con:
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM Apps WHERE AppName = '" + appname + "'")
      rows = cur.fetchall()
      return rows[0]
  
  def Connect(self):
    '''Connects to the database, returning the connection to it.'''
    return sqlite3.connect('apps.db')
