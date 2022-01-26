from string import Template
import os, requests, re
class Proxy:
  '''self represents the instance of the class.'''
#  rules = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Rule.yaml').content.decode('utf-8')
#  head = requests.get('https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Head_dns.yaml').content.decode('utf-8')
  rules = requests.get('https://cdn.jsdelivr.net/gh/lhie1/Rules@master/Clash/Rule.yaml').content.decode('utf-8').replace('https://raw.lhie1.com/lhie1/Rules', 'https://cdn.jsdelivr.net/gh/lhie1@Rules')
  head = requests.get('https://cdn.jsdelivr.net/gh/lhie1/Rules@master/Clash/Head_dns.yaml').content.decode('utf-8')
#  storage = 'https://cdn.jsdelivr.net/gh/wmyfelix/ClashAddons@OMC'
#  storage = 'https://raw.githubusercontent.com/wmyfelix/ClashAddons/OMC'
  def __init__(self, exec_dir, output_path, stroage = 'https://cdn.jsdelivr.net/gh/wmyfelix/ClashAddons@OMC', template_path = './template/clash'):
    self.storage = stroage
    self.output_path = output_path
    names = self.__dict__
    for x in ['proxy_groups','proxy_providers','urltest']: # dynamic variable. https://www.runoob.com/w3cnote/python-dynamic-var.html
      template_file = template_path +'/'+ x
      if os.path.isfile(template_file):
        y = open(template_file).read()
      else: print(f"template: {x} not exist.",exit())

      names[x] = Template(y)
    self.urltest = self.urltest.substitute(url = 'http://www.gstatic.com/generate_204', interval = 300, tolerance = 180)
    self.name_path= self.get_filename(exec_dir)
  def get_filename(self,_dir):
    name_path = dict()
    for root, dirs, names in os.walk(_dir): # recognize parrent dirs as well.
        for name in names:
            name_path[name] = os.path.join(root,name).replace('\\','/') # fix NT "\".
    return name_path
  def gen_proxy_providers(self):
    ret = ""
    for x, y in self.name_path.items():
      ret += self.proxy_providers.substitute(name = x, location = self.storage +'/'+ y)
    return ret
  def gen_all_proxies(self):
    def all_proxies():
      ret = ""
      for x in self.name_path:
          ret += f"\t- {x}\n"
      return ret
    def gen_rules():
      sets = re.findall('.*RULE-SET.*',self.rules)
      rules_proxies = ['Others']
      for x in sets:
        rule_name = re.split(',',x)[-1] # structure: RULE-SET,rules,proxy-group
        if rule_name not in rules_proxies:
          rules_proxies.append(rule_name)
      ret = ""
      rules_proxies.sort()
      for x in rules_proxies:
        if x == 'AdBlock': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = "proxies:\n\t- REJECT\n\t- DIRECT\n\t- Proxy", uses = '', urltest = '')
        elif x == 'DIRECT': continue
        elif x == 'Proxy': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- All\n' + all_proxies()+'\n\t- DIRECT', uses = '', urltest = '')
        elif x == 'Domestic': ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- DIRECT\n\t- Proxy\n' + all_proxies(), uses = '', urltest = '')
        else: ret += self.proxy_groups.substitute(name = x, type = 'select', proxies = 'proxies:\n\t- Proxy\n'+all_proxies() + '\n\t- DIRECT', uses = '', urltest = '')
      return ret
    return self.proxy_groups.substitute(name = 'All', type = 'url-test', proxies = "proxies:\n" + all_proxies(), uses = '', urltest = self.urltest) + gen_rules()
  def gen_each_proxies(self):
    ret = ""
    for x in self.name_path:
      ret += self.proxy_groups.substitute(name = x, type = 'url-test', proxies = '', uses = f"use:\n\t- {x}", urltest = self.urltest)
    return ret
#proxy = Proxy() # instance: proxy
  def arranger(self):
    file = f"""
{self.head}
proxy-providers:
{self.gen_proxy_providers()}
proxy-groups:
{self.gen_all_proxies()}
{self.gen_each_proxies()}
rules:
{self.rules}
    """
    file = file.replace('\t','  ') # YAML dont support Tabulator key.
    with open(self.output_path ,'w') as f:
      f.write(file.strip())