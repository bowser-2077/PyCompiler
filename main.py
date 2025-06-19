import argparse
import subprocess
import os
import sys
import time
import ctypes

# Activer les couleurs ANSI sur Windows
kernel32 = ctypes.windll.kernel32
handle = kernel32.GetStdHandle(-11)
mode = ctypes.c_ulong()
kernel32.GetConsoleMode(handle, ctypes.byref(mode))
kernel32.SetConsoleMode(handle, mode.value | 0x0004)

COLORS = {
    "info": "\033[94m",
    "success": "\033[92m",
    "warning": "\033[93m",
    "error": "\033[91m",
    "reset": "\033[0m"
}

def log(msg, level="info"):
    print(f"{COLORS.get(level, COLORS['info'])}[PyCompiler] {msg}{COLORS['reset']}")
    time.sleep(1.5)

def compile_script(file, icon=None, no_cli=False, no_ui=False, onefile=True):
    # Chemin vers pyinstaller.exe local
    pyinstaller_exe = os.path.join(os.path.dirname(sys.argv[0]), "WinCompileTool.exe")

    # Vérifie si pyinstaller.exe local existe, sinon utilise 'pyinstaller' dans PATH
    if os.path.isfile(pyinstaller_exe):
        command = [pyinstaller_exe]
    else:
        command = ["WinCompileTool.exe"]

    if not os.path.isfile(file):
        log(f"Fichier introuvable: {file}", "error")
        sys.exit(1)

    if onefile:
        command.append("--onefile")
    else:
        command.append("--onedir")

    if no_cli:
        command.append("--noconsole")

    if no_ui:
        command.append("--windowed")

    if icon:
        if not os.path.isfile(icon):
            log(f"Icône introuvable: {icon}", "error")
            sys.exit(1)
        command.append(f"--icon={icon}")

    command.append(file)

    log("Lancement de la compilation...")
    log("Commande exécutée :", "warning")
    log(" ".join(command), "warning")

    subprocess.run(command)

    log("Compilation terminée !", "success")
    log("Fichiers générés dans le dossier 'dist/'", "info")

def main():
    parser = argparse.ArgumentParser(description="PyCompiler - CLI based app to compile python files")
    parser.add_argument("--compile", type=str, help=".py file to compile")
    parser.add_argument("--icon", type=str, help="Icon file to add to the compiled file")
    parser.add_argument("--nocli", action="store_true", help="No console mode")
    parser.add_argument("--noui", action="store_true", help="Compile with gui (only for tkinter/pyqt/pyside)")
    parser.add_argument("--onefile", action="store_true", help="Compile with onefile")
    parser.add_argument("--multiplefiles", action="store_true", help="Create multiple files")

    args = parser.parse_args()

    if not args.compile:
        parser.print_help()
        return

    compile_script(
        file=args.compile,
        icon=args.icon,
        no_cli=args.nocli,
        no_ui=args.noui,
        onefile=args.onefile or not args.multiplefiles
    )

if __name__ == "__main__":
    main()
    log("Don't double click on the script. Launch it via the cmd/terminal", "error")
    while True:
        time.sleep(1)

