import os
from time import sleep
from django.core.files import File
from django.template.defaultfilters import slugify
import subprocess



def create_meta_file(input_file):
    file_ext = ".mttrck" #metatrack file extension for saving metadata
    root_file_name = os.path.splitext(input_file)[0] #file name without extension

    basename=slugify(os.path.basename(root_file_name)) #prints just the basename

    directory=os.path.dirname(root_file_name)

    output_file = str(directory) + "/"+str(basename) +str(file_ext)

    with open(output_file, "wb") as output:
        """
        Open a file in the same directory as the input file and write the metadata into it
        """
        exiftool_command = ["exiftool/exiftool", input_file]
        result = subprocess.run(exiftool_command, stdout=output)

