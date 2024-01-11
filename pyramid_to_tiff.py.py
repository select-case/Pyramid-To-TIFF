import tkinter as tk
from tkinter import filedialog
import os

def convert_pyr_to_tif(pyr_levels, tif_name):
    level_dirs = os.listdir(pyr_levels)
    level_dirs = [int(level) for level in level_dirs]
    max_level = max(level_dirs)

    c_max = 0
    r_max = 0
    base_level = os.path.join(pyr_levels, str(max_level))
    for src_image in os.listdir(base_level):
        if '.webp' in src_image:
            name, ext = src_image.split(".")
            c, r = name.split("_")
            c, r = int(c), int(r)
            c_max = max(c_max, c)
    c_max = c_max + 1

    cd_cmd = "cd "+base_level
    vips_cmd = "vips arrayjoin \"$(ls *.webp | sort -t_ -k2g -k1g)\" " + tif_name + "[tile,pyramid,compression=jpeg] --across " +  str(c_max)
    composite_cmd = cd_cmd + " && " + vips_cmd
    tif_creation = os.system(composite_cmd)
    return tif_creation


# if __name__ == "__main__":

#     parser = ArgumentParser(description="Convert pyramid base directory to tiff")

#     parser.add_argument(dest="case_dir", help="Directory with all the cases", metavar="$CASE_DIR$")
#     parser.add_argument(dest="tif_dir", help="Destination directory to store tiff", metavar="$TIFF_DIR$")
#     args = parser.parse_args()

def convert(case_dir, tif_dir):

    for case in os.listdir(case_dir):
        if os.path.exists(os.path.join(case_dir, case, "pyramid", "tiles.dzi")):
            tif_name = os.path.join(tif_dir, case + ".tif")
            if not os.path.exists(tif_name):
                try:
                    result = convert_pyr_to_tif(os.path.join(case_dir, case, "pyramid", "tiles_files"), tif_name)
                    print("Tif creation successful with case {}".format(tif_name))
                except Exception as e:
                    print("Tif creation failed with exception {}".format(e))
            else:
                print ("Tif file already exist with name {}".format(tif_name))

def select_case_dir():
    case_dir = filedialog.askdirectory()
    case_dir_entry.delete(0, tk.END)
    case_dir_entry.insert(0, case_dir)

def select_tif_dir():
    tif_dir = filedialog.askdirectory()
    tif_dir_entry.delete(0, tk.END)
    tif_dir_entry.insert(0, tif_dir)

def start_conversion():
    case_dir = case_dir_entry.get()
    tif_dir = tif_dir_entry.get()
    if case_dir and tif_dir:
        status_label.config(text="Conversion started")
        convert(case_dir, tif_dir)
        status_label.config(text="Conversion completed")
    else:
        print("Please select case directory and tiff directory")

app = tk.Tk()
app.title("Pyramid to TIFF Converter")

tk.Label(app, text="Case Directory").pack()
case_dir_entry = tk.Entry(app, width=50)
case_dir_entry.pack()

case_dir_button = tk.Button(app, text="Select Case Directory", command=select_case_dir)
case_dir_button.pack()

tk.Label(app, text="TIFF Directory").pack()
tif_dir_entry = tk.Entry(app, width=50)
tif_dir_entry.pack()

tif_dir_button = tk.Button(app, text="Select TIFF Directory", command=select_tif_dir)
tif_dir_button.pack()

convert_button = tk.Button(app, text="Start Conversion", command=start_conversion)
convert_button.pack()

status_label = tk.Label(app, text="")
status_label.pack()

app.mainloop()
