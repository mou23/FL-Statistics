#!/bin/bash

projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
xml_files=("AspectJ.xml" "Birt.xml" "Eclipse_Platform_UI.xml" "JDT.xml" "SWT.xml" "Tomcat.xml")
type=$1  # baseline, clean

for i in "${!projects[@]}"; do
  proj="${projects[$i]}"
  xml_file="${xml_files[$i]}"
  command="python evaluator.py ../../dream_loc/${proj}_ranked_result_mapped.csv ../../dream_loc/data/reports/${xml_file} > ${type}_${proj}.txt"
  echo "Running ${proj} ${type}: $command"
  eval "$command"
done