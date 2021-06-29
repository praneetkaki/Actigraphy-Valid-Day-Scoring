from cx_Freeze import setup, Executable
  
build_options = {
    "packages":["PySimpleGUI"]
}

setup(name = "Valid Day Calculator" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("gui.py")],
      options = dict(build_exe = build_options))

