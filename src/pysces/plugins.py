from importlib.metadata import entry_points

def load_plugins():
    eps = entry_points(group='pysces.plugins')
    plugins = {}
    if len(eps) == 0:
        print("No plugins found.")
        return plugins
    
    print("Loading Plugins:")
    print('-'*80)
    for ep in eps:
        success_msg = 'Success'
        try:
            plugins[ep.name] = ep.load()
        except:
            success_msg = 'Failed'
        print(f'    {ep.name + ":":20s} {ep.value:40s} {success_msg}')
    
    print('-'*80)

    return plugins


