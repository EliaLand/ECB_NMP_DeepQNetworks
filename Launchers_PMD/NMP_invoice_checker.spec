# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

env = os.environ.copy()
env["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['NMP_interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Images/icon-ECB.png', 'Images'),
        ('Images/European-Central-Bank.png', 'Images')
    ],
    hiddenimports=[
    'nltk',
    'nltk.corpus',
    'nltk.stem',
    'nltk.tokenize',
    'easyocr',
    'easyocr.utils',
    'easyocr.detection',
    'easyocr.recognition',
    'easyocr.easyocr'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NMP_invoice_checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False  # Set to True if you want to see terminal output
)