#!/usr/bin/python3

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ['re','PIL._tkinter_finder','hashlib']
                    ,excludes = []
                    )

executables = [Executable ('yatube.py'
                          ,base       = 'Console'
                          ,icon       = 'resources/icon_64x64_yatube.gif'
                          ,targetName = 'yatube'
                          )
              ]

setup (name        = 'Yatube'
      ,version     = '1'
      ,description = 'Youtube Client'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
