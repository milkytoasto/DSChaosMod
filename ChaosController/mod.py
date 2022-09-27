from DarkSoulsRemastered.Effects import WarpToBonfire
from pymem import Pymem, process
from pymem.exception import ProcessNotFound
from utils.ProcessTitles import ProcessTitles


def main():
    process_title = ProcessTitles.DSR
    try:
        pm = Pymem(process_title)
    except ProcessNotFound:
        print(f"Process {process_title} not found")
        return

    module = process.module_from_name(pm.process_handle, process_title)
    WarpToBonfire.start(pm, module)


if __name__ == "__main__":
    main()
