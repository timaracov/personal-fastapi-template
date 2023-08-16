#!/usr/bin/bash

cd __project_name__/internal && PYTHONPATH=. poetry run pytest --cov --ignore=tests/integ/
