# Deprecated.
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
[[ $(getconf .Enabled) != "true" ]] && echo "Update Disabled." && exit 0
server=$(getconf .SCServer)
remote_server=$(getconf .SCServerRemote)
p_name=($(echo $(getconf ".ProxyProviders|keys"|sed "s/- //")))
p_url=($(echo $(getconf .ProxyProviders.[])))
clash_args=$(echo $(getconf .ClashProviders|sed "s/: /=/")|sed "s/ /\&/g")
quanx_args=$(echo $(getconf .QuantumultXRemotes|sed "s/: /=/")|sed "s/ /\&/g")
filters="exclude=$(getconf .ExcludeExp.syntax)"
whitelist=($(echo $(getconf .ExcludeExp.whitelist.[])))
classify=($(echo $(getconf .SmartFilter.[])))
git_email=($(getconf .Git.email))
git_name=($(getconf .Git.name))
nnum=${#p_name[@]} # Numbers of providers
lnum=${#p_url[@]} # Numbers of subscribe links
checknode="The following link doesn't contain any valid node info:|No nodes were found!"
for num in $(seq 0 $nnum);do
    name="${p_name[$num]}"
    url="${p_url[$num]}"
    if [ $num == $nnum ];then
        if [ $(getconf .QuickGenQX) == true ];then QuickGen; fi
        python ./region.py
        python ./load.py
        echo "Completed. "
        git add -A
        if [ -z "$(git status -u |grep "Changes to be committed:")" ];then
            echo "Nothing Updated."
        else 
            git config --local user.email $git_email
            git config --local user.name $git_name
            git commit -m "Update Proxy Provider." -a
        fi
        exit 0
    fi

    if [[ $whitelist =~ $name ]] || [[ $filters == "null" ]];then
        echo NoFilter.
        curl -SsL "$server/sub?url=$url&$clash_args&exclude=false" -o tmpc
        curl -SsL "$server/sub?url=$url&$quanx_args&exclude=false" -o tmpq
    else
        echo WithFilter.
        curl -SsL "$server/sub?url=$url&$clash_args&$filters" -o tmpc
        curl -SsL "$server/sub?url=$url&$quanx_args&$filters" -o tmpq
    fi
    if [ -z "$(grep -E "$checknode" tmpc)" ];then # Check if any proxies available
        echo "Clash: Writing $name"
        mv -f tmpc proxies/Clash/$name
    else
        rm tmpc # Keep last file and make no change
    fi
    if [ -z "$(grep -E "$checknode" tmpq)" ];then
        echo "QuantumultX: Writing $name"
        mv -f tmpq proxies/QuantumultX/$name
    else
        rm tmpq
    fi
    [[ $classify =~ $name ]] && {
        echo "SmartFiltering Activated."
        chmod +x ./classify.py
        ./classify.py proxies/Clash/$name
    }|| echo "SmartFiltering Disabled."
done