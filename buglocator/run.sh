#!/bin/bash

projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
type=$1  # baseline, clean

for proj in "${projects[@]}"; do
  command="python metric_calculator.py ${proj} ../../FL-Buglocator/results-${type}/BugLocator_${proj} ../../FL-Buglocator/dataset/${proj}-updated-data.xml ${type}"
  echo "Running ${proj} ${type}: $command"
  eval "$command"
done