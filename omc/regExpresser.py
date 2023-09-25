#!/usr/bin/python3
# -*- coding: utf-8 -*-

# run() ex.
# RegExp: [6x]
# <proxy group>'s <proxies>
# ChinaG's [6x]HKT --> ChinaG_6x's [6x]HKT

import re
import os
import yaml
from omc import encolored


class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
    def ignore_unknown(self, node):
        return None


SafeLoaderIgnoreUnknown.add_constructor(
    None, SafeLoaderIgnoreUnknown.ignore_unknown)


def get_proxies(content, alternative_name='proxies'):
    try:
        return yaml.load(content, Loader=SafeLoaderIgnoreUnknown)[alternative_name]
    except:
        return None


def get_name(content):
    ret = {}
    for x in yaml.load(content, Loader=SafeLoaderIgnoreUnknown)['proxies']:
        ret[x['name']] = x
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


def dumper(list_dict, file):
    _dump = dict()
    _dump['proxies'] = list_dict
    # allow_unicode = True : fix emoji and etc...
    yaml.dump(_dump, file, allow_unicode=True)


def run(regex, file_path):
    matched_proxies = {}
    unmatched_proxies = []
    matched_keyword = []
    file_name = file_path.split('/')[-1]
    encolored.Debug("Processing: ", file_path)
    rm_old(file_path)
    with open(file_path) as f:
        f = f.read()
        for x, y in get_name(f).items():
            # re.search.group() only return the first matched match.
            matched = re.search(regex, x, re.IGNORECASE)
            if matched:
                if matched.group() not in matched_keyword:
                    matched_keyword.append(matched.group())
                    matched_proxies[matched.group()] = [y]
                else:
                    matched_proxies[matched.group()] += [y]

            else:
                unmatched_proxies.append(y)
    if matched_keyword == []:
        encolored.Warn("Invaild regex: All pattern not match.", regex)
    else:
        encolored.Info('Matched: ', matched_keyword)
        # rename_original(file_path)
        for x, y in matched_proxies.items():
            with open('{}_/{}\'s {}'.format(file_path, file_name, x), 'w') as f:
                dumper(y, f)
        if unmatched_proxies != []:
            with open('{}_/{}\'s Others'.format(file_path, file_name), 'w') as f:
                dumper(unmatched_proxies, f)
