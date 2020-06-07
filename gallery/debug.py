#!/usr/bin/bash

export FLASK_APP=user_management.py
export FLASH_ENV=development
flask run --host=0.0.0.0
