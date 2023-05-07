# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[ ('C:/Users/n4ze3/personal/img-pdf-py/icons/*.ico', 'icons')],
    hiddenimports=['pkg_resources.py2_warn','win32timezone','six','packaging','packaging.version','webbrowser','kivy','enchant'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='imgtopdf',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons\\icon.ico'],
)
