# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['getImageFile.py'],
             pathex=['C:\\Users\\82107\\Desktop\\BusinessAutomation\\pillow'],
             binaries=[],
             datas=[],
             hiddenimports=['Pyinstaller'],
             hookspath=['C:\\Users\\82107\\Desktop\\BusinessAutomation\\BusinessAutomation\\Lib\\site-packages\\PyInstaller\\hooks\\hook-grpc.py'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='myApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='myApp')
