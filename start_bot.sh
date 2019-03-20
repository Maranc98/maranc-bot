#!/bin/bash

. $(pwd)'/config.sh';

result=65;

while [ $result -eq 65 ]
do
${python_path} ${python_script}
result=$?
done
