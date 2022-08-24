#!/usr/bin/bash
# Copyright 2019 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

SOURCE_PATH='/home/iguazio/parquez'

if ! [ -d venv  ] ; then
        mkdir venv
        virtualenv venv
        source venv/bin/activate
        pip install -r config/requirements.txt
else
        source venv/bin/activate
fi

python ${SOURCE_PATH}/parquez.py ${1} ${2} ${3} ${4} ${5} ${6} ${7} ${8} ${9} ${10} ${11} ${12} ${13} ${14}

