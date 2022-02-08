#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, re
import requests
from .classify import get_name, dumper

def gather_files(path, exclude):
    if type(exclude) != str: exit('check regexp in Exclude:region.')
    for file in os.listdir(path):
        if os.path.isfile(path+'/'+file): 
            with open(path+'/'+file,'r') as f:
                ret = get_name(f)
                for name in list(ret): # Dict can't be motified during iteration, so change it to list.
                    if re.search(exclude, name, re.IGNORECASE): 
                        del ret[name]
    return ret
def processor(path, out = "", exclude = '限速|游戏|game'):
    if out == "": out = path+'/region/' # Shouldnt be same as path, make duplication.
    os.makedirs(out,exist_ok=True)
    parsed = requests.get('https://raw.githubusercontent.com/tindy2013/subconverter/master/base/snippets/emoji.txt', allow_redirects=True).content.decode('utf-8')
    re_list = parsed.strip().split('\n')
    proxies_dict = gather_files(path, exclude)
    for num, re_ in list(enumerate(re_list)): # make a list of each region proxies and put them in for better flexbility.
        re_match = re_.split(',')[0]
        re_emoji = re_.split(',')[1]
        print('Regexp: ',re_emoji)
        locals()[f'list_{num}'] = []
        list_reg = locals()[f"list_{num}"] # use local() func mannally, otherwise would be recognize as str. because var is spliced by string.format.
        for proxies, line in list(proxies_dict.items()):
            if re.search(re_match,proxies):
                print('\tMatched: ', proxies)
                list_reg.append(line)
                del proxies_dict[proxies] # solve duplicate match (China regexp.)
        if len(list_reg) != 0:
            with open(out + re_emoji,'w') as f:
                dumper(list_reg, f)