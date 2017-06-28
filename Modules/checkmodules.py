import importlib
import sys


def check_version():
    if(sys.version_info < (3, 4, 0)):
        return (False, "You need Python 3.4 or later to run this project")
    else:
        return (True, "Python minimum version requirement satisfied")


def check_lib(package_name, package_version):

    try:
        package = importlib.import_module(package_name)
        installed_version = package.__version__ .rstrip()
        minimum_version = package_version.rstrip()
        if(not(installed_version >= minimum_version)):
            raise Exception("Module name: {} installed but Minimum version: {} required. Found version: {}".format(
                package_name, minimum_version, installed_version))
    except ImportError:
        return (False, "Module name: {} not installed !!".format(package_name))
    except Exception as error:
        return (False, error.args[0])
    else:
        return (True, "Module name: {} installed with minimum version requirement satisfied.".format(
            package_name))


if __name__ == "__main__":
    check_modules()
