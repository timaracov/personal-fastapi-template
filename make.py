import os
import shutil

from pathlib import Path


TEMPLATE_NAME = "__project_name__"

FILES_WITH_TEMPLATE_INSIDE = [
    "logging.py",
    "api.py",
    "db.py",
    "pyproject.toml",
    "Dockerfile"
]

FILES_TO_IGNORE = [
    "make.py",
    "setup.py",
    "README.md",
]


def main(project_name):
    template_folder = Path(__file__).parent
    current_folder = Path(os.getcwd())

    shutil.copytree(template_folder/TEMPLATE_NAME, current_folder/project_name) 
    for file in os.listdir(template_folder):
        src = os.path.join(template_folder, file)
        if os.path.isfile(src) and file not in FILES_TO_IGNORE:
            dst = os.path.join(current_folder, file)
            shutil.copyfile(src, dst)

    to_repl = []
    for dir, dirnames, files in os.walk(current_folder):
        for dirname in dirnames:
            if TEMPLATE_NAME in dirname:
                new_name = dirname.replace(TEMPLATE_NAME, project_name)
                to_repl.append(
                    (
                        os.path.join(dir, dirname),
                        os.path.join(dir, new_name)
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
