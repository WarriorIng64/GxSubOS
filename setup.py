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
from appdb import AppDb

def Setup():
  # Sets up the necessary data for the SubOS if this is the first run.
  if(not os.path.isdir("apps")):
    # App database setup
    database = AppDB()
    database.InsertDefaultApps()
    # Create directories and retrieve default apps from Git repos
    os.makedirs("apps")
    os.makedirs("default")
    applist = database.RetrieveAppNames()
    for appname in applist:
      # Create each repo and pull
      appinfo = database.GetAppInfo(appname)
      appdir = "apps/default/" + appinfo["DirName"]
      os.makedirs(appdir)
      git.Repo.clone_from(appinfo["RepoUrl"], appdir)