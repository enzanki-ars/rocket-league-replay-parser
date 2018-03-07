def get_assets_path():
    import os
    import sys

    import rocketleaguereplayanalysis.assets

    if getattr(sys, 'frozen', False):
        assets_path = os.path.join(sys._MEIPASS, 'assets')
    else:
        assets_path = os.path.join(
                rocketleaguereplayanalysis.assets.__path__[0])

    available_assets = []

    for file in os.listdir(assets_path):
        if file.endswith('.json'):
            available_assets.append(file[:-1 * len('.json')])

    return assets_path, available_assets
