# from PyInstaller.utils.hooks import collect_all

# datas, binaries, hiddenimports = collect_all('PyInstaller')

from PyInstaller.utils.hooks import copy_metadata, collect_data_files
    datas = copy_metadata('PyInstaller')
    datas += collect_data_files('PyInstaller')