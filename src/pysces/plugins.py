from importlib.metadata import entry_points

def load_plugins():
    eps = entry_points(gorup='pysces.plugins')
    plugins = {}
    for ep in eps:
        plugins[ep.name] = ep.load()
    return plugins


