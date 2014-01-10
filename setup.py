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

import os, git
from appdb import AppDB

def Setup():
  # Sets up the necessary data for the SubOS if this is the first run.
  if not os.path.isdir(os.getcwd() + "/apps"):
    print "First run; setting up app database."
    # App database setup
    database = AppDB()
    database.InsertDefaultApps()
    initialwd = os.getcwd()
    # Create directories and retrieve default apps from Git repos
    os.makedirs(os.getcwd() + "/apps/default")
    os.chdir(os.getcwd() + "/apps/default")
    appswd = os.getcwd()
    applist = database.RetrieveAppNames()
    print "Need to clone " + str(len(applist)) + " default apps."
    for appname in applist:
      # Create each repo and pull
      os.chdir(appswd)
      appinfo = database.GetAppInfo(appname)
      os.system("git clone " + appinfo["RepoUrl"])