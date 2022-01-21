from omc import config_read, region, load
config = config_read.pro('./omc/config.yaml')
dirx = 'proxies'
config.get_providers(dirx)
if config.parse_conf['QuickGenQX']:
    config.gen_quanx(dirx+'/quanx', '.')
config.smart_filter(dirx+'/clash')

region.processor(dirx+'/clash')

mk_clash_config = load.Proxy(dirx+'/clash', 'test.yaml')
mk_clash_config.arranger()
