from pathlib import Path

def searching_all_files(path: Path):
    dirpath = Path(path)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(str(x)))
    return file_list