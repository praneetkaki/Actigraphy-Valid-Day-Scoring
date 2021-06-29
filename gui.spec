# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Temp/praneet/Actigraphy-Valid-Day-Scoring/gui.py'],
             pathex=['C:\\Temp\\praneet\\Actigraphy-Valid-Day-Scoring'],
             binaries=[],
             datas=[('C:/Temp/praneet/Actigraphy-Valid-Day-Scoring', 'Actigraphy-Valid-Day-Scoring/')],
             hiddenimports=[],
             hookspath=[],
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
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Temp\\praneet\\Actigraphy-Valid-Day-Scoring\\exe-icon.ico')
