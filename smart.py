from omc import config_read, region, load
config = config_read.pro('./omc/config.yaml')
dirx = config.parse_conf['Output Dir']
config.get_providers(dirx)
if config.parse_conf['QuickGenQX']:
    config.gen_quanx(dirx+'/quanx', '.')
config.smart_filter(dirx+'/clash')

region.processor(dirx+'/clash',exclude= config.parse_conf['Exclude']['region'])

mk_clash_config = load.Proxy(dirx+'/clash', dirx+'/test.yaml', config.rules, config.head, config.parse_conf['Storage'], config.parse_conf['Template'], config.parse_conf['Exclude']['All'])
mk_clash_config.arranger()
