from cx_Freeze import setup, Executable

includes = ["sys", "pickle", "os", "argparse", "PIL", "time", "math"]

exe = Executable(script = "Main.py")

setup(version = "1.0", options = {"build_exe":{"includes":includes}}, executables = [exe])
