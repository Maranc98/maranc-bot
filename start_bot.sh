#!/bin/bash

. $(pwd)'/config.sh';

result=65;

while [ $result -eq 65 ]
do
${python_path} ${python_script};
result=$?;

if [ $result -eq 66 ];
then
  echo "Updating bot";
  git pull;
  result=65;
fi
done
