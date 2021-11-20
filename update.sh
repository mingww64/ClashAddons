#!/bin/bash
config=./config.yaml
getconf(){
    yq e $1 $2 $config 
}
QuickGen(){
    echo QuickGenQX Activated.
    location=$(readlink -f proxies/QuantumultX/AIO)
    dir=$(dirname $location)
    rm $location
    names=$(ls $dir)
    for x in $names;do
        if [ $x == AIO ];then continue; fi
        echo -e "\n#$x" >> $location
        cat $dir/$x >> $location
    done
    curl -SsL "$server/sub?url=$location&target=quanx&config=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead%2Fsubconverter-config%40master%2Fremote-config%2Funiversal%2Furltest.ini&emoji=true" -o ./QuantumultX.conf
    sed -i "s/"$server"/"$remote_server"/g" ./QuantumultX.conf 
}
server=$(getconf .SCServer)
remote_server=$(getconf .SCServerRemote)
p_name=($(echo $(getconf ".ProxyProviders|keys"|sed "s/- //")))
p_url=($(echo $(getconf .ProxyProviders.[])))
clash_args=$(echo $(getconf .ClashProviders|sed "s/: /=/")|sed "s/ /\&/g")
quanx_args=$(echo $(getconf .QuantumultXRemotes|sed "s/: /=/")|sed "s/ /\&/g")
filters="exclude=$(getconf .ExcludeExp)"
nnum=${#p_name[@]} # Numbers of providers
lnum=${#p_url[@]} # Numbers of subscribe links
checknode="The following link doesn't contain any valid node info:|No nodes were found!"
for num in $(seq 0 $nnum);do
    if [ $num == $nnum ];then
        if [ $(getconf .QuickGenQX) == true ];then QuickGen; fi
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
    curl -SsL "$server/sub?url=${p_url[$num]}&$clash_args&$filters" -o tmpc
    curl -SsL "$server/sub?url=${p_url[$num]}&$quanx_args&$filters" -o tmpq

    if [ -z "$(grep -E "$checknode" tmpc)" ];then # Check if any proxies available
        echo "Clash: Writing ${p_name[$num]}"
        mv -f tmpc proxies/Clash/${p_name[$num]}
    else
        rm tmpc # Keep last file and make no change
    fi
    if [ -z "$(grep -E "$checknode" tmpq)" ];then
        echo "QuantumultX: Writing ${p_name[$num]}"
        mv -f tmpq proxies/QuantumultX/${p_name[$num]}
    else
        rm tmpq
    fi
done