#!/bin/bash
var=$(python --version | tr '[A-Z]' '[a-z]')
echo $var
pipenv --${var}
