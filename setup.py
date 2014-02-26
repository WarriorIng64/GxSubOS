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

import os, platform, subprocess
from appdb import AppDB

def UpdateApps():
  '''Gets updates for the installed default apps.'''
  loading_subprocesses = []
  database = AppDB()
  initialwd = os.getcwd()
  appswd = os.getcwd() + "/apps/default"
  applist = database.RetrieveAppNames()
  print "Checking for updates to " + str(len(applist)) + " apps..."
  for appname in applist:
    appinfo = database.GetAppInfo(appname)
    os.chdir(appswd + "/" + appname)
    if platform.system() == "Windows":
      loading_subprocesses.append(subprocess.Popen('"C:\Program Files (x86)\Git\cmd\git.exe" --git-dir=' + os.getcwd() + '/.git --work-tree=' + os.getcwd() + ' pull'))
    else:
      pull_success = os.system("git pull")
    os.chdir(initialwd)
  return loading_subprocesses

def Setup():
  '''Sets up the necessary data for the SubOS if this is the first run.'''
  if not os.path.isdir(os.getcwd() + "/apps"):
    database = AppDB()
    initialwd = os.getcwd()
    appswd = os.getcwd() + "/apps/default"
    print "First run; setting up app database."
    # App database setup
    database.InsertDefaultApps()
    applist = database.RetrieveAppNames()
    # Create directories and retrieve default apps from Git repos
    os.makedirs(appswd)
    print "Need to clone " + str(len(applist)) + " default apps."
    for appname in applist:
      # Create each repo and pull
      appinfo = database.GetAppInfo(appname)
      os.chdir(appswd)
      # If we're on Windows, use Git for Windows from https://code.google.com/p/msysgit/
      # Otherwise, assume Linux 
      if platform.system() == "Windows":
        clone_success = os.system('"C:\Program Files (x86)\Git\cmd\git.exe" clone ' + appinfo["RepoUrl"])
      else:
        clone_success = os.system("git clone " + appinfo["RepoUrl"])
      if clone_success != 0:
        print "ERROR: Could not clone " + appname + "."
      os.chdir(initialwd)
      return []
  else:
    # Apps set up from previous run; check for updates
    return UpdateApps()
