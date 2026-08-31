import os
import shutil
import subprocess
import sys
from pathlib import Path


LITEDB_VERSION = "5.0.21"

ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "resources"
DB_DIR = RESOURCES / "DB"
LIB_DIR = RESOURCES / "lib"

NUGET_DIR = ROOT / ".nuget"


def run(command, cwd=None):
    print(f"> {' '.join(map(str, command))}")

    subprocess.check_call(
        command,
        cwd=cwd
    )


def check_command(command):
    return shutil.which(command) is not None


def check_python():
    print("Checking Python...")

    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or newer is required.")
        sys.exit(1)

    print(f"Python {sys.version.split()[0]} OK")


def check_dotnet():
    print("Checking .NET SDK...")

    if not check_command("dotnet"):
        print(
            "\nERROR: .NET SDK was not found.\n"
            "Please install the .NET SDK and run setup.py again."
        )

        sys.exit(1)

    result = subprocess.run(
        ["dotnet", "--version"],
        capture_output=True,
        text=True,
        check=True
    )

    print(f".NET {result.stdout.strip()} OK")


def install_python_packages():
    print("\nInstalling Python dependencies...")

    run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "psutil",
        "pythonnet"
    ])


def create_directories():
    print("\nCreating directories...")

    DB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    LIB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    NUGET_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def create_dotnet_project():
    print("\nCreating temporary .NET project...")

    project_dir = NUGET_DIR / "LiteDBProject"

    if project_dir.exists():
        shutil.rmtree(project_dir)

    run([
        "dotnet",
        "new",
        "classlib",
        "-n",
        "LiteDBProject",
        "--framework",
        "net8.0"
    ], cwd=NUGET_DIR)

    return project_dir


def install_litedb(project_dir):
    print(
        f"\nInstalling LiteDB {LITEDB_VERSION}..."
    )

    run([
        "dotnet",
        "add",
        "package",
        "LiteDB",
        "--version",
        LITEDB_VERSION
    ], cwd=project_dir)


def copy_litedb_dll(project_dir):
    print("\nLocating LiteDB.dll...")

    package_dir = (
        project_dir
        / "obj"
        / "project.assets.json"
    )

    if not package_dir.exists():
        print("ERROR: NuGet package restore failed.")
        sys.exit(1)

    nuget_package = (
        Path.home()
        / ".nuget"
        / "packages"
        / "litedb"
        / LITEDB_VERSION
        / "lib"
    )

    if not nuget_package.exists():
        print(
            "ERROR: LiteDB NuGet package was not found."
        )

        sys.exit(1)

    dlls = list(
        nuget_package.rglob("LiteDB.dll")
    )

    if not dlls:
        print(
            "ERROR: LiteDB.dll was not found."
        )

        sys.exit(1)

    source = dlls[0]
    target = LIB_DIR / "LiteDB.dll"

    shutil.copy2(
        source,
        target
    )

    print(f"Installed: {target}")


def test_installation():
    print("\nTesting installation...")

    dll = LIB_DIR / "LiteDB.dll"

    if not dll.exists():
        print("ERROR: LiteDB.dll is missing.")
        sys.exit(1)

    try:
        import psutil
        import clr

        clr.AddReference(
            str(dll)
        )

        from LiteDB import LiteDatabase

        print("psutil OK")
        print("pythonnet OK")
        print("LiteDB OK")

        # Keine DB öffnen.
        # Der eigentliche Benchmark erstellt sie.

    except Exception as exc:
        print(
            "\nERROR: LiteDB/Python.NET test failed:"
        )
        print(exc)

        sys.exit(1)


def cleanup():
    print("\nCleaning temporary files...")

    if NUGET_DIR.exists():
        shutil.rmtree(NUGET_DIR)


def main():
    print("=" * 60)
    print("Database Benchmark Setup")
    print("=" * 60)

    check_python()
    check_dotnet()

    create_directories()
    install_python_packages()

    project_dir = create_dotnet_project()

    install_litedb(project_dir)
    copy_litedb_dll(project_dir)

    cleanup()
    test_installation()

    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)

    print("\nYou can now run:")
    print("    python benchmark.py")


if __name__ == "__main__":
    main()