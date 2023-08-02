import os
import shutil

from pathlib import Path


TEMPLATE_NAME = "__project_name__"
FILES_WITH_TEMPLATE_INSIDE = [
    "logging.py",
    "api.py"
]


def main(project_name):
    template_folder = Path(__file__).parent
    current_folder = Path(os.getcwd())

    shutil.copytree(template_folder/TEMPLATE_NAME, current_folder/project_name) 

    to_repl = []
    for dir, dirnames, files in os.walk(current_folder/project_name):
        if TEMPLATE_NAME in dirnames:
            to_repl.append(
                (
                    os.path.join(dir, TEMPLATE_NAME),
                    os.path.join(dir, project_name)
                )
            )
        for file in files:
            if TEMPLATE_NAME in file:
                ext = "."+file.split(".")[-1]
                to_repl.append(
                    (
                        os.path.join(dir, file),
                        os.path.join(dir, project_name+ext)
                    )
                )
            if file in FILES_WITH_TEMPLATE_INSIDE:
                fpath = os.path.join(dir, file)
                with open(fpath, "r") as f:
                    file_source = f.read()
                with open(fpath, "w") as f:
                    f.write(file_source.replace(TEMPLATE_NAME, project_name))

    for from_, to_ in to_repl:
        try:
            shutil.move(from_, to_)
        except:
            continue


if __name__ == "__main__":
    from sys import argv
    try:
        project_name = argv[1]
    except:
        raise ValueError("expected argument: project_name")
    else:
        main(project_name)