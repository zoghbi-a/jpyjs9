from subprocess import check_call

try:
    check_call(["node", "-v"])
    print("(jpyjs9 assist_node) Detected preinstalled node. Skipping installation.")
except:
    print("(jpyjs9 assist_node) No node detected. Attempting virtual environment install...")
    try:
        check_call(["nodeenv", "-p"])
        print("(jpyjs9 assist_node) node successfully installed into current virtual environment")
    except:
        raise ModuleNotFoundError("(jpyjs9 assist_node) Unable to install node, a required dependency. Please install node separately before continuing...")