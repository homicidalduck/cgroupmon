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

import re

class Config:
    def __init__(self, configfile = None):
        self.settings = {}
        if configfile != None:
            self.loadconfig(configfile)

    def loadconfig(self, configfile):
        f = open(configfile)
        configtext = f.read()
        f.close()
        pattern = re.compile(r'\s*([\S]*)\s*=\s*([\S]*)')
        tuples = re.findall(pattern, configtext)
        for term in tuples:
            self.settings[term[0].lower()] = term[1].lower()
