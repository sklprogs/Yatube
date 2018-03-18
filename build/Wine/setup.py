from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ['re','PIL._tkinter_finder']
                    ,excludes = []
                    )

executables = [Executable ('Yatube.py'
                          ,base       = 'Win32GUI'
                          ,icon       = 'resources\icon_64x64_yatube.ico'
                          ,targetName = 'yatube.exe'
                          )
              ]

setup (name        = 'Yatube'
      ,version     = '1'
      ,description = 'Youtube Client'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
