# -*- mode: python -*-

block_cipher = None
import os

basepath = os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd())))

a = Analysis(['rcm_client_qt.py'],
             pathex=[os.path.join(basepath, 'RCM/rcm/server')],
             binaries=[],
             datas=[('gui/icons/*.png', 'gui/icons/'),
                    (os.path.join(basepath, 'turbovnc'), 'turbovnc')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='rcm_client_qt',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='rcm_client_qt')