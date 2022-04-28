from string import Template
import os
import requests
import re


class Proxy:
    '''self represents the instance of the class.'''

    def __init__(self, exec_dir, output_path, rules='./template/clash/connershua/rules.yml', head='./template/clash/head.yaml', storage='https://cdn.jsdelivr.net/gh/wmyfelix/ClashAddons@OMC', template_path='./template/clash', re_exclude='🇨🇳'):
        self.storage = storage
        self.output_path = output_path
        self._All_exclude = re_exclude
        if 'http' in rules:
            self.rules = requests.get(rules).content.decode('utf-8')
        else:
            self.rules = open(rules, 'r').read()
        if 'rules:' not in self.rules:
            self.rules = 'rules:\n' + self.rules
        if 'http' in head:
            self.head = requests.get(head).content.decode('utf-8')
        else:
            self.head = open(head, 'r').read()
        names = self.__dict__
        # dynamic variable. https://www.runoob.com/w3cnote/python-dynamic-var.html
        for x in ['proxy_groups', 'proxy_providers', 'urltest']:
            template_file = template_path + '/' + x
            if os.path.isfile(template_file):
                y = open(template_file).read()
            else:
                print(f"template: {x} not exist.", exit())

            names[x] = Template(y)
        self.urltest = self.urltest.substitute(
            url='http://www.gstatic.com/generate_204', interval=300, tolerance=180)
        self.name_path, self.icon_path = self.get_filename(exec_dir)

    def get_filename(self, _dir):
        name_path, region_icons = dict(), dict()
        # recognize parrent dirs as well.
        for root, dirs, names in os.walk(_dir):
            for name in names:
                if root.split('/')[-1] == 'region':
                    # fix NT "\".
                    region_icons[name] = os.path.join(
                        root, name).replace('\\', '/')
                else:
                    # fix NT "\".
                    name_path[name] = os.path.join(
                        root, name).replace('\\', '/')
        return name_path, region_icons

    def gen_proxy_providers(self):
        ret = ""
        for x, y in self.name_path.items():
            ret += self.proxy_providers.substitute(
                name=x, location=self.storage + '/' + y)
        return ret

    def gen_all_proxies(self):
        def all_icon_proxies():
            ret = ""
            for x in self.icon_path:
                if re.search(self._All_exclude, x, re.IGNORECASE):
                    pass
                else:
                    ret += f"\t- {x}\n"
            return ret

        def all_proxies():
            ret = ""
            for v in [self.name_path, self.icon_path]:
                for x in v:
                    ret += f"\t- {x}\n"
            return ret

        def gen_rules():
            sets = re.findall('.*RULE-SET.*', self.rules)
            rules_proxies = ['Others']
            for x in sets:
                # structure: RULE-SET,rules,proxy-group
                rule_name = re.split(',', x)[-1]
                if rule_name not in rules_proxies:
                    rules_proxies.append(rule_name)
            ret = ""
            rules_proxies.sort()
            for x in rules_proxies:
                if x in ['AdBlock', 'Advertising', 'Hijacking', 'Privacy']:
                    # REJECT by default. without proxies.
                    ret += self.proxy_groups.substitute(
                        name=x, type='select', proxies="proxies:\n\t- REJECT\n\t- DIRECT\n\t- Proxy", uses='', urltest='')
                elif x in ['DIRECT', 'REJECT']:
                    continue  # Pass Bulit-in.
                elif x == 'Proxy':
                    ret += self.proxy_groups.substitute(
                        name=x, type='select', proxies='proxies:\n\t- All\n' + all_proxies()+'\n\t- DIRECT', uses='', urltest='')
                elif x in ['Domestic', 'China', 'StreamingSE']:
                    # DIRECT by default. with proxies.
                    ret += self.proxy_groups.substitute(
                        name=x, type='select', proxies='proxies:\n\t- DIRECT\n\t- Proxy\n' + all_proxies(), uses='', urltest='')
                else:
                    ret += self.proxy_groups.substitute(
                        name=x, type='select', proxies='proxies:\n\t- Proxy\n'+all_proxies() + '\n\t- DIRECT', uses='', urltest='')
            return ret
        return self.proxy_groups.substitute(name='All', type='url-test', proxies="proxies:\n" + all_icon_proxies(), uses='', urltest=self.urltest) + gen_rules()

    def gen_each_proxies(self):
        ret = ""
        for v in [self.name_path, self.icon_path]:
            for x in v:
                ret += self.proxy_groups.substitute(
                    name=x, type='url-test', proxies='', uses=f"use:\n\t- {x}", urltest=self.urltest)
        return ret
# proxy = Proxy() # instance: proxy

    def arranger(self):
        file = f"""
{self.head}
proxy-providers:
{self.gen_proxy_providers()}
proxy-groups:
{self.gen_all_proxies()}
{self.gen_each_proxies()}
{self.rules}
    """
        file = file.replace('\t', '  ')  # YAML dont support Tabulator key.
        with open(self.output_path, 'w') as f:
            f.write(file.strip())
