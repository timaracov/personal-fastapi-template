#!/usr/bin/bash

poetry run black --check --diff --color __project_name__
poetry run flake8 --config=./__project_name__/configs/.flake8 __project_name__
