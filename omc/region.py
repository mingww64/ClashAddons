#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, re
import requests
def gather_files(path, exclude):
    _file = []
    for file in os.listdir(path):
        if os.path.isfile(path+'/'+file): 
            with open(path+'/'+file,'r') as f:
                f = f.readlines()
                for line in f:
                    if re.search('name:',line):
                        if type(exclude) == str:
                            if re.search(exclude, line, re.IGNORECASE):
                                pass
                            else: _file.append(line)
    return _file
def processor(path, out = "", exclude = '限速|游戏|game'):
    if out == "": out = path+'/region/' # Shouldnt be same as path, make duplication.
    os.makedirs(out,exist_ok=True)
    parsed = requests.get('https://raw.githubusercontent.com/tindy2013/subconverter/master/base/snippets/emoji.txt', allow_redirects=True).content.decode('utf-8')
    re_list = parsed.strip().split('\n')
    for num, re_ in list(enumerate(re_list)): # make a list of each region proxies and put them in for better flexbility.
        re_match = re_.split(',')[0]
        re_emoji = re_.split(',')[1]
        locals()[f'list_{num}'] = []
        list_reg = locals()[f"list_{num}"] # use local() func mannally, otherwise would be recognize as str. because var is spliced by string.format.
        for proxies in gather_files(path, exclude):
            if re.search(re_match,proxies):
                list_reg.append(proxies)
        if len(list_reg) != 0:
            with open(out + re_emoji,'w') as f:
                txt = "proxies:\n"
                for x in list_reg:
                    txt += "  " + x.strip() + '\n' # fix unexpected '\n' missing.
                f.write(txt.strip())