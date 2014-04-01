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

class IndicatorDB:
  def RetrieveIndicatorNames(self):
    '''Retrieves a list of the names of all indicators in the database.'''
    indicatorslist = []
    con = self.Connect()
    with con:
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      try:
        cur.execute("SELECT IndicatorName FROM Indicators")
        rows = cur.fetchall()
        for row in rows:
          indicatorslist.append(row["IndicatorName"])
        return indicatorslist
      except sqlite3.OperationalError:
        print "ERROR: IndicatorDB.RetrieveIndicatorNames() failed due to operational error."
        return []
  
  def InsertDefaultIndicators(self):
    '''Inserts the info for the default indicators into the database.'''
    con = self.Connect()
    with con:
      cur = con.cursor()
      # Initial database setup
      cur.execute("DROP TABLE IF EXISTS Indicators")
      cur.execute("CREATE TABLE Indicators(IndicatorId INT PRIMARY KEY, \
                   IndicatorName TEXT, \
                   DefaultIndicator INTEGER, \
                   WebsiteUrl TEXT, \
                   RepoUrl TEXT)")
      # The default indicators are currently hard-coded here
      values = (
        ('GxPowerIndicator',True,'https://github.com/WarriorIng64/GxPowerIndicator','https://github.com/WarriorIng64/GxPowerIndicator'),
        ('GxTimeIndicator',True,'https://github.com/WarriorIng64/GxTimeIndicator','https://github.com/WarriorIng64/GxTimeIndicator'),
        ('GxBatteryIndicator',True,'https://github.com/WarriorIng64/GxBatteryIndicator','https://github.com/WarriorIng64/GxBatteryIndicator')
      )
      fields = "IndicatorName,DefaultIndicator,WebsiteUrl,RepoURL"
      for indicator in values:
        cur.executemany("INSERT INTO Indicators(" + fields + ") VALUES(?, ?, ?, ?)", (indicator,))
      con.commit()
  
  def GetIndicatorInfo(self, indicatorname):
    '''Gets the info for the given indicator name as a dictionary.'''
    con = self.Connect()
    with con:
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM Indicators WHERE IndicatorName = '" + indicatorname + "'")
      rows = cur.fetchall()
      return rows[0]
  
  def Connect(self):
    '''Connects to the database, returning the connection to it.'''
    return sqlite3.connect('indicators.db')
