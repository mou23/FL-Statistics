#!/bin/bash

projects=("aspectj" "birt" "eclipse" "jdt" "swt" "tomcat")
type=("average-precision" "reciprocal-rank")
technique=$1  # bluir, brtracer, buglocator, vsm


for proj in "${projects[@]}"; do
    mkdir -p result-${technique}
    
    command="python two_files_analyzer.py ${proj} ${technique}/${proj}-baseline-average-precision.csv ${technique}/${proj}-clean-average-precision.csv > result-${technique}/${proj}-average-precision.txt" 
    echo "Running ${proj} average-precision: $command"
    eval "$command"

    command="python two_files_analyzer.py ${proj} ${technique}/${proj}-baseline-reciprocal-rank.csv ${technique}/${proj}-clean-reciprocal-rank.csv > result-${technique}/${proj}-reciprocal-rank.txt"
    echo "Running ${proj} reciprocal-rank: $command"
    eval "$command"
done