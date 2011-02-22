#!/usr/bin/env python
# Copyright 2011 Matt Larson
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import print_function
import os
import sys
from pwd import getpwuid
import psutil

class CGroup:
    "Stores a representation of a cgroup, including children processes"
    def __init__(self, path):
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            print("Error: path does not exist", file=sys.stderr)
        self.id = os.path.basename(self.path)
        self.user = getpwuid(os.stat(self.path).st_uid).pw_name
        self.subgroups = []
        self.update()
        
    def update(self):
        "Updates processes, returns False if cgroup is no longer active, else True"
        if not os.path.isdir(self.path):
            return False
        sharefile = open(os.path.join(self.path, "cpu.shares"), 'r')
        self.shares = sharefile.readline().strip()
        sharefile.close()
        self.procs=[]
        if not os.path.isdir(self.path):
            return False
        procfile = open(os.path.join(self.path, "cgroup.procs"), 'r')
        for pid in procfile:
            try:
                self.procs.append(psutil.Process(int(pid)))
            except:
                pass
        procfile.close()
        subgroupids = []
        for i in self.subgroups:
            if not i.update():
                self.subgroups.remove(i)
            else:
                subgroupids.append(i.id)
        for i in os.listdir(self.path):
            if(os.path.isdir(os.path.join(self.path, i))
               and not i in subgroupids):
                self.subgroups.append(CGroup(os.path.join(self.path, i)))
        return True

    def __repr__(self):
        ret = ""
        ret = ret + "CGroup: " + str(self.id) + "\n"
        ret = ret + "  User: " + self.user + "\n"
        ret = ret + "  CPU Shares: " + self.shares + "\n"
        ret = ret + "  Procs:\n"
        for i in self.procs:
            try:
                ret = ret + "    " + str(i.pid) + "  " + i.name + "\n"
            except:
                pass
        if self.subgroups:
            ret = ret + "  SubCGroups:\n    "
            for i in self.subgroups:
                ret = ret + repr(i).replace("\n", "\n    ")
        ret = ret + "\n"
        return ret
