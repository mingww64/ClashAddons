from omc import confluX, nationAttitude, transformer
import sys

config = transformer.Kit('./omc/config.yaml')
dirx = config.parse_conf['Output Dir']
if len(sys.argv[1:]) == 0:
    # Download proxies from providers and Convert them to Clash/QuantumultX node list with the provider's name.
    config.get_providers(dirx)
    # Generate configuration from former node lists by subconverter directly.
    config.subconverter(dirx+'/quanx', dirx+'/sub')
    # Filter nodes matched to the regular expression.
    config.classifier(dirx+'/clash')
    # Classify proxy providers correspond to the region of nodes.
    nationAttitude.processor(
        dirx+'/clash', exclude=config.parse_conf['Exclude']['region'])
    # Generate proxy groups correspond to the provider's name and the region of nodes.
    mk_clash_config = confluX.Proxy(dirx+'/clash', dirx+'/Clash.yaml', config.rules, config.head,
                                    config.parse_conf['Storage'], config.parse_conf['Template']['Clash'], config.parse_conf['Exclude']['All'])
    mk_clash_config.arranger()
    mk_quanx_config = confluX.QuanX(dirx+'/quanx', dirx+'/QuanX.conf',
                                    config.parse_conf['Storage'], config.parse_conf['Template']['Quantumult X'], config.parse_conf['Exclude']['All'])
    mk_quanx_config.arranger()
else:
    for arg in sys.argv[1:]:
        if arg == '--get-providers':
            config.get_providers(dirx)
        elif arg == '--subconverter':
            config.subconverter(dirx+'/quanx', dirx)
        elif arg == '--smart_filter':
            config.classifier(dirx+'/clash')
        elif arg == '--region-spliter':
            nationAttitude.processor(
                dirx+'/clash', exclude=config.parse_conf['Exclude']['region'])
        elif arg == '--clash-arranger':
            mk_clash_config = confluX.Proxy(dirx+'/clash', dirx+'/Clash.yaml', config.rules, config.head,
                                            config.parse_conf['Storage'], config.parse_conf['Template']['Clash'], config.parse_conf['Exclude']['All'])
            mk_clash_config.arranger()
        elif arg == '--quanx-arranger':
            mk_quanx_config = confluX.QuanX(dirx+'/quanx', dirx+'/QuanX.conf',
                                            config.parse_conf['Storage'], config.parse_conf['Template']['Quantumult X'], config.parse_conf['Exclude']['All'])
            mk_quanx_config.arranger()
        else:
            print(f'option {arg} cannot be recognized.')
