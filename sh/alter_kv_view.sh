#!/usr/bin/env bash

if ! [ -d venv  ] ; then
        mkdir venv
        virtualenv venv
        source venv/bin/activate
        pip install -r config/requirements.txt
else
        source venv/bin/activate
fi


echo alter_kv_view "${1}" "${2}"

python core/alter_kv_view.py "${1}" "${2}"

