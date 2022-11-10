#!/bin/bash
config=../exec/omc/config.yaml
getconf(){
    yq e $1 $2 $config 
}
git_email=($(getconf .Git.email))
git_name=($(getconf .Git.name))
git add -A
if [ -z "$(git status -u |grep "Changes to be committed:")" ];then
    echo "Nothing Updated."
else 
    git config --local user.email $git_email
    git config --local user.name $git_name
    git commit -m "Update Proxy Provider." -a
fi