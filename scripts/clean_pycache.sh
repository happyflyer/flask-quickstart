#!/bin/bash

rm -rf __pycache__
rm -rf */__pycache__
rm -rf */*/__pycache__
rm -rf */*/*/__pycache__
rm -f .coverage
rm -rf .pytest_cache
rm -rf tmp
rm -rf log
