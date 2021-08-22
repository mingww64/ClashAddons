#!/bin/bash
link=($(grep -o 'http.*sub.*' ./Orginal.yaml))
name=($(grep -o './proxy_provider.*.yaml' ./Orginal.yaml |awk -F/ '{print $3}'))
nnum=${#name[@]}
lnum=${#link[@]}
if [ $nnum != $lnum ];then
    echo "Url ≠ Name"
    exit 1
fi

for num in $(seq 0 $nnum);do
    if [ $num == $nnum ];then
        echo "Completed. "
        git add -A
        if [ -z "$(git status -u |grep "Changes to be committed:")" ];then
            echo "Nothing Updated."
        else 
            git config --local user.email "felicia@realnet.ml"
            git config --local user.name "FeliciaWen"
            git commit -m "Update Proxy Provider." -a
        fi
        exit 0
    fi
    curl -SsL ${link[$num]} -o tmp
    if [ ! -z "$(grep proxies tmp)" ];then
        echo "Writing ${name[$num]}"
        mv tmp proxy_provider/${name[$num]}
    else
        rm tmp
    fi
done