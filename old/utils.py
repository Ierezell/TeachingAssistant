import zipfile
import os
from shutil import copy2
import subprocess


def unzip(path_to_file: str, path_to_dest_folder: str):
    with zipfile.ZipFile(path_to_file, 'r') as zip_file:
        zip_file.extractall(path_to_dest_folder)


def unbundle(path_to_bundled_folder: str, path_to_unbundled_folder):

    for file in os.listdir(path_to_bundled_folder):
        dst_unbundle_file = path_to_bundled_folder+'/'+file[:-3]
        copy2(file, dst_unbundle_file)
        command = f"cd {dst_unbundle_file} && hg init && hg unbundle && hg update"
        proc = subprocess.run(command.split())
        if proc.returncode != 0:
            raise RuntimeError(f"Impossible de unbundler {file}")

# process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
