import sys
from pathlib import Path

py_path = sys.executable
current_path = Path('.').absolute()
cmd = f"alias datareport=\"{py_path} -m dataprofile.cli_report\""

dotfiles = ['.zshrc', '.bashrc', '.bash_profile']

for file in dotfiles:
    dotfile = Path(Path().home(), file)
    try:
        with open(dotfile, "a") as f:
            f.write(cmd)
            print(f"successfully create the cmd alias datareport in {dotfile}")
            break
    except:
        pass
