# -*- mode: python ; coding: utf-8 -*-

added_files = [('pong/ding.mp3','pong'),('*.ttf','.'),('pong/presets/*','pong/presets'),('text/instructions.md','text'),('text/version.md','text'),('game_list.dat','.'),('Pong/*.py','pong'),('SpaceRace/*.py','spacerace'),('settings_default.dat','.'),('*.jpg','.'),('SpaceRace/presets/*.dat','spacerace/presets'),('SpaceRace/sprites/Ship/*','spacerace/sprites/ship'),('SpaceRace/sprites/Asteroid/*','spacerace/sprites/asteroid'),('SpaceRace/sprites/Asteroid_old/*','spacerace/sprites/asteroid_old'),('SpaceRace/sprites/Burst/*','spacerace/sprites/burst'),('SpaceRace/sprites/Canister/*','spacerace/sprites/canister')]
paths=['Pong']

a = Analysis(
    ['browgames'],
    pathex=paths,
    binaries=[],
    datas=added_files,
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
    a.binaries,
    a.datas,
    [],
    name='browgames',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='browgames',
)
