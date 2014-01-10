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

import sys
import MySQLdb as mdb

# This module was constructed with the help of this online tutorial:
# http://zetcode.com/db/mysqlpython/

class AppDB:
  def __init__(self):
    self.con = None
    self.Connect()
    with self.con:
      cur = self.con.cursor()
      cur.execute("USE GxSubOS")
  
  def __del__(self):
    self.Disconnect()
  
  def RetrieveAppNames(self):
    '''Retrieves a list of the names of all apps in the database.'''
    appslist = []
    cur = self.con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT AppName FROM Apps")
    rows = cur.fetchall()
    for row in rows:
      appslist.append(row["AppName"])
    return appslist
  
  def InsertDefaultApps(self):
    '''Inserts the info for the default apps into the database.'''
    cur = self.con.cursor()
    # Initial database setup
    cur.execute("USE GxSubOS")
    cur.execute("DROP TABLE IF EXISTS Apps")
    cur.execute("CREATE TABLE Apps(AppId INT PRIMARY KEY AUTO_INCREMENT, \
                 AppName VARCHAR(20), \
                 DefaultApp BOOLEAN, \
                 CurVersion VARCHAR(3), \
                 UpdateVersion VARCHAR(3), \
                 WebsiteUrl VARCHAR(2083), \
                 RepoUrl VARCHAR(2083))")
    # The default apps are currently hard-coded here
    fields = "AppName,DefaultApp,CurVersion,UpdateVersion,WebsiteUrl,RepoURL"
    values = "'GxCalculator',true,'0.1','0.1','https://github.com/WarriorIng64/GxCalculator','https://github.com/WarriorIng64/GxCalculator.git'"
    cur.execute("INSERT INTO Apps(" + fields + ") VALUES(" + values + ")")
  
  def GetAppInfo(self, appname):
    '''Gets the info for the given app name as a dictionary.'''
    cur = self.con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Apps WHERE AppName = '" + appname + "'")
    rows = cur.fetchall()
    return rows[0]
  
  def Connect(self):
    '''Connects to the database.'''
    self.con = mdb.connect('localhost', 'GxSubOSUser', 'GxSubOSPassword', 'GxSubOS')
  
  def Disconnect(self):
    '''Disconnects from the database.'''
    self.con.close()
