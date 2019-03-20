#!/bin/bash

. $(pwd)'/config.sh';

result=65;

while [ $result -ne 60 ]
do
${python_path} ${python_script};
result=$?;

echo "Acting according to result "$result;

if [ $result -eq 66 ];
then
  echo "Updating bot";
  git pull;
fi

done
