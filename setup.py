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
    """Run a command and stop setup if it fails."""

    print(f"\n> {' '.join(map(str, command))}")

    subprocess.check_call(
        command,
        cwd=cwd
    )


def check_command(command):
    return shutil.which(command) is not None


def check_python():
    print("Checking Python...")

    if sys.version_info < (3, 10):
        print(
            "\nERROR: Python 3.10 or newer is required."
        )
        sys.exit(1)

    print(
        f"Python {sys.version.split()[0]} OK"
    )


def check_dotnet():
    print("\nChecking .NET SDK...")

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

    print(
        f".NET SDK {result.stdout.strip()} OK"
    )


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
        "netstandard2.0"
    ], cwd=NUGET_DIR)

    return project_dir


# ============================================================
# Install LiteDB through NuGet
# ============================================================

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


# ============================================================
# Build project
# ============================================================

def build_dotnet_project(project_dir):
    print("\nBuilding temporary .NET project...")

    run([
        "dotnet",
        "build",
        "--configuration",
        "Release"
    ], cwd=project_dir)


# ============================================================
# Copy LiteDB and dependencies
# ============================================================

def copy_litedb_dependencies(project_dir):
    print("\nCopying LiteDB and dependencies...")

    output_dir = (
        project_dir
        / "bin"
        / "Release"
        / "netstandard2.0"
    )

    if not output_dir.exists():
        print(
            "\nERROR: .NET build output was not found."
        )
        sys.exit(1)

    copied = []

    # --------------------------------------------------------
    # First try the build output.
    # --------------------------------------------------------

    for dll in output_dir.glob("*.dll"):

        # The temporary project itself is not needed.
        if dll.name == "LiteDBProject.dll":
            continue

        target = LIB_DIR / dll.name

        shutil.copy2(
            dll,
            target
        )

        copied.append(dll.name)

    # --------------------------------------------------------
    # Explicitly locate System.Buffers.
    #
    # This is the dependency which caused the original error.
    # --------------------------------------------------------

    buffers_dlls = list(
        (
            Path.home()
            / ".nuget"
            / "packages"
            / "system.buffers"
        ).rglob("lib/*/System.Buffers.dll")
    )

    if buffers_dlls:
        # Prefer the newest package version available.
        buffers_dlls.sort()

        buffers_source = buffers_dlls[-1]
        buffers_target = LIB_DIR / "System.Buffers.dll"

        shutil.copy2(
            buffers_source,
            buffers_target
        )

        if "System.Buffers.dll" not in copied:
            copied.append("System.Buffers.dll")

    # --------------------------------------------------------
    # LiteDB itself must exist.
    # --------------------------------------------------------

    litedb = LIB_DIR / "LiteDB.dll"

    if not litedb.exists():

        # Fallback: search NuGet cache directly.
        nuget_package = (
            Path.home()
            / ".nuget"
            / "packages"
            / "litedb"
            / LITEDB_VERSION
            / "lib"
        )

        dlls = list(
            nuget_package.rglob("LiteDB.dll")
        )

        if not dlls:
            print(
                "\nERROR: LiteDB.dll was not found."
            )
            sys.exit(1)

        shutil.copy2(
            dlls[0],
            litedb
        )

        copied.append("LiteDB.dll")

    print("\nInstalled .NET assemblies:")

    for dll in sorted(set(copied)):
        print(f"    {dll}")


# ============================================================
# Test the complete installation
# ============================================================

def test_installation():
    print("\nTesting installation...")

    litedb_dll = LIB_DIR / "LiteDB.dll"

    if not litedb_dll.exists():
        print(
            "ERROR: LiteDB.dll is missing."
        )
        sys.exit(1)

    try:
        import psutil
        import clr

        if str(LIB_DIR) not in sys.path:
            sys.path.insert(
                0,
                str(LIB_DIR)
            )

        buffers_dll = LIB_DIR / "System.Buffers.dll"

        if buffers_dll.exists():
            print(
                "Loading System.Buffers.dll..."
            )

            clr.AddReference(
                str(buffers_dll)
            )

        print(
            "Loading LiteDB.dll..."
        )

        clr.AddReference(
            str(litedb_dll)
        )

        from LiteDB import LiteDatabase

        print("psutil OK")
        print("pythonnet OK")
        print("System.Buffers OK")
        print("LiteDB assembly OK")

        test_db = DB_DIR / "setup_test.db"

        if test_db.exists():
            test_db.unlink()

        print(
            "Opening temporary LiteDB database..."
        )

        db = LiteDatabase(
            str(test_db)
        )

        collection = db.GetCollection(
            "setup_test"
        )

        collection.Insert({
            "id": 1,
            "message": "setup test"
        })

        result = collection.FindById(1)

        if result is None:
            raise RuntimeError(
                "LiteDB test insert/read failed."
            )

        db.Dispose()

        if test_db.exists():
            test_db.unlink()

        print(
            "LiteDB database test OK"
        )

    except Exception as exc:

        print(
            "\nERROR: LiteDB/Python.NET test failed:"
        )

        print(exc)

        print(
            "\nThe LiteDB DLL or one of its dependencies "
            "could not be loaded."
        )

        sys.exit(1)


def cleanup():
    print("\nCleaning temporary files...")

    if NUGET_DIR.exists():
        shutil.rmtree(
            NUGET_DIR
        )

def main():

    print("=" * 60)
    print("Database Benchmark Setup")
    print("=" * 60)

    try:

        check_python()

        check_dotnet()

        create_directories()

        install_python_packages()

        project_dir = create_dotnet_project()

        install_litedb(
            project_dir
        )

        build_dotnet_project(
            project_dir
        )

        copy_litedb_dependencies(
            project_dir
        )

        test_installation()

        cleanup()

        print("\n" + "=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)

        print(
            "\nYou can now run:"
        )

        print(
            "    python benchmark.py"
        )

    except Exception:

        print(
            "\nSetup failed."
        )

        print(
            "Temporary files were kept in:"
        )

        print(
            f"    {NUGET_DIR}"
        )

        raise


if __name__ == "__main__":
    main()

