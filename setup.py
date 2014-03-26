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
from indicatordb import IndicatorDB

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
      loading_subprocesses.append(subprocess.Popen('git pull', shell=True))
    os.chdir(initialwd)
  return loading_subprocesses

def UpdateIndicators():
  '''Gets updates for the installed default indicators.'''
  loading_subprocesses = []
  database = IndicatorDB()
  initialwd = os.getcwd()
  indicatorswd = os.getcwd() + "/indicators/default"
  indicatorlist = database.RetrieveIndicatorNames()
  print "Checking for updates to " + str(len(indicatorlist)) + " indicators..."
  for indicatorname in indicatorlist:
    indicatorinfo = database.GetIndicatorInfo(indicatorname)
    os.chdir(indicatorswd + "/" + indicatorname)
    if platform.system() == "Windows":
      loading_subprocesses.append(subprocess.Popen('"C:\Program Files (x86)\Git\cmd\git.exe" --git-dir=' + os.getcwd() + '/.git --work-tree=' + os.getcwd() + ' pull'))
    else:
      loading_subprocesses.append(subprocess.Popen('git pull', shell=True))
    os.chdir(initialwd)
  return loading_subprocesses

def Setup():
  '''Sets up the necessary data for the SubOS if this is the first run.'''
  if (not os.path.isdir(os.getcwd() + "/apps")) or (not os.path.isdir(os.getcwd() + "/indicators")):
    loading_subprocesses = []
    initialwd = os.getcwd()
    
    # Apps first
    database = AppDB()
    appswd = initialwd + "/apps/default"
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
        loading_subprocesses.append(subprocess.Popen('"C:\Program Files (x86)\Git\cmd\git.exe" clone ' + appinfo["RepoUrl"] + ' ' + appswd + '/' + appname))
      else:
        loading_subprocesses.append(subprocess.Popen("git clone " + appinfo["RepoUrl"], shell=True))
      os.chdir(initialwd)
      
    # Indicators second
    database = IndicatorDB()
    indicatorswd = initialwd + "/indicators/default"
    print "First run; setting up indicator database."
    # Indicator database setup
    database.InsertDefaultIndicators()
    indicatorlist = database.RetrieveIndicatorNames()
    # Create directories and retrieve default indicators from Git repos
    os.makedirs(indicatorswd)
    print "Need to clone " + str(len(indicatorlist)) + " default indicators."
    for indicatorname in indicatorlist:
      # Create each repo and pull
      indicatorinfo = database.GetIndicatorInfo(indicatorname)
      os.chdir(indicatorswd)
      # If we're on Windows, use Git for Windows from https://code.google.com/p/msysgit/
      # Otherwise, assume Linux 
      if platform.system() == "Windows":
        loading_subprocesses.append(subprocess.Popen('"C:\Program Files (x86)\Git\cmd\git.exe" clone ' + indicatorinfo["RepoUrl"] + ' ' + indicatorswd + '/' + indicatorname))
      else:
        loading_subprocesses.append(subprocess.Popen("git clone " + indicatorinfo["RepoUrl"], shell=True))
      os.chdir(initialwd)
  else:
    # Apps set up from previous run; check for updates
    loading_subprocesses = UpdateApps() + UpdateIndicators()
  return loading_subprocesses
