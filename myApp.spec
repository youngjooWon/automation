# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['getImageFile.py'],
             pathex=['C:\\Users\\82107\\Desktop\\BusinessAutomation'],
             binaries=[],
             datas=[],
             hiddenimports=['Pyinstaller,moviepy.editor'],
             hookspath=['C:\\Users\\82107\\Desktop\\BusinessAutomation\\BusinessAutomation\\Lib\\site-packages\\PyInstaller\\hooks\\hook-Pyinstaller.py'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='myApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )