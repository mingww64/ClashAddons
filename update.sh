#!/bin/bash
link=($(grep -o 'http.*sub.*' ./config.yaml))
name=($(grep -o './proxy_provider.*.yaml' ./config.yaml |awk -F/ '{print $3}'))
nnum=${#name[@]}
lnum=${#link[@]}
if [ $nnum != $lnum ];then
    echo "Url ≠ Name"
    exit 1
fi

for num in $(seq 0 $nnum);do
    if [ $num == $nnum ];then
        echo "Completed. "
        exit 0
    fi
    curl -SsL ${link[$num]} -o tmp
    if [ ! -z $(grep proxies tmp) ];then
        echo "Writing ${name[$num]}"
        mv tmp proxy_provider/${name[$num]}
    else
        rm tmp
    fi
done