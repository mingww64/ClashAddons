#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import os
import yaml


def get_name(content):
    ret = {}
    for x in yaml.safe_load(content)['proxies']:
        ret[x['name']] = x
    print(ret)
    return ret


def rename_original(path):
    _file_All = path + '_All'
    if os.path.exists(_file_All):
        os.remove(_file_All)
    os.rename(path, _file_All)


def rm_old(path):
    exec_path = path + '_'
    if os.path.isdir(exec_path):
        for root, dirs, files in os.walk(exec_path):
            for file in files:
                os.remove(os.path.join(root, file))
            for dirc in dirs:
                os.remove(os.path.join(root, dirc))
    else:
        os.makedirs(exec_path)


def dumper(iter):
    lines = '\n  - '.join(iter)
    return 'proxies:\n  - ' + lines


def run(syx, file_path):
    _in = {}
    _plain = []
    _matched_list = []
    file_name = file_path.split('/')[-1]
    print("processing: ", file_path)
    rm_old(file_path)
    with open(file_path) as f:
        f = f.read()
        for x, y in get_name(f).items():
            matched = re.search(syx, x)
            if matched:
                if matched.group() not in _matched_list:  # re.search.group() only return the first match ?
                    _matched_list.append(matched.group())
                    _in[matched.group()] = [y]
                else:
                    _in[matched.group()] += [y]

            else:
                _plain.append(y)
    if _matched_list == []:
        print("pattern cannot be matched.")
    else:
        print('Matched: ', _matched_list)
        # rename_original(file_path)
        for x, y in _in.items():
            with open('{}_/{}_{}'.format(file_path, file_name, x), 'w') as f:
                _dump = dict()
                _dump['proxies'] = y
                yaml.dump(_dump, f, default_flow_style=False,
                          allow_unicode=True)
        with open('{}_/{}_plain'.format(file_path, file_name), 'w') as f:
            _dump = dict()
            _dump['proxies'] = _plain
            yaml.dump(_dump, f, default_flow_style=False, allow_unicode=True)
