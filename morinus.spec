# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['morinus_mac.py'],
    pathex=[],
    binaries=[],
    datas=[('Res', 'Res'), ('SWEP/Ephem', 'SWEP/Ephem'), ('Opts', 'Opts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Morinus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Res/MorinusSE.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Morinus',
)
app = BUNDLE(
    coll,
    name='Morinus.app',
    icon='Res/MorinusSE.ico',
    bundle_identifier='org.morinus.se',
)
