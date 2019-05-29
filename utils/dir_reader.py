from pathlib import Path

def read_directories_recursive(root_path, max_iter=-1, current_iter=0, prefix=""):
    print(prefix + str(root_path))
    for entry in root_path.iterdir():
        prefix = prefix + "-"
        current_iter = current_iter + 1 
        print(prefix + entry.name)
        if max_iter == -1 or (current_iter < max_iter):
            if entry.is_dir():
                read_directories_recursive(entry, max_iter, current_iter, prefix)
