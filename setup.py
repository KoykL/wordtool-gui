from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
includes = ["lxml._elementpath",
            "lxml.etree",
            "inspect",
            "gzip",
            "gevent.ssl"]
buildOptions = dict(
    packages = [], excludes = [],
    includes=includes, compressed=True, bin_excludes=["libsystem_network.dylib", "libobjc.A.dylib"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('wordtool.py', base=base)
]

setup(name='wordtool',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
