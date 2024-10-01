import argparse
import glob
import os
import shutil

from FF8GameData.gamedata import GameData
from data import m000bin, BinManager, m001bin, m002bin, m003bin, m004bin

input_folder = '1 - InputFiles'
pandemona_folder = '2 - PandemonaFiles'
output_folder = '3 - OutputFiles'

# The m00x.bin files consist of a data for each ability. Each "data (abilities) has an entry of x bytes.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pandemona", description="This program read m00x.bin files")
    args = parser.parse_args()

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(pandemona_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Check if pandemona file exist.
    # If in the output folder there is pandemona files, it means we want to create .bin and .msg from it.
    # If the files don't exist, it means we want to create them first from the original files

    output_pandemona_list = glob.glob(os.path.join(pandemona_folder, "*.pandemona"))
    if len(output_pandemona_list) > 0:  # Means we want to read pandemona files to write to .msg and .bin
        list_to_analyze = output_pandemona_list
        reading_pandemona = True
        shutil.copyfile(os.path.join(input_folder, "mngrp.bin"), os.path.join(output_folder, "mngrp.bin"))
        shutil.copyfile(os.path.join(input_folder, "mngrphd.bin"), os.path.join(output_folder, "mngrphd.bin"))
    else:  # Means we want to read .bin and .msg to create pandemona file
        list_to_analyze = glob.glob(os.path.join(input_folder, "*.bin"))
        reading_pandemona = False


    game_data = GameData("FF8GameData")
    game_data.load_item_data()
    game_data.load_magic_data()
    game_data.load_card_data()

    bin_manager = BinManager(game_data)
    if reading_pandemona:
        bin_manager.read_pandemona_file(pandemona_folder)
        bin_manager.write_mngrp_file(os.path.join(output_folder, "mngrp.bin"), os.path.join(output_folder, "mngrphd.bin"))
    else:
        bin_manager.read_mngrp_file(os.path.join(input_folder, "mngrp.bin"), os.path.join(input_folder, "mngrphd.bin"))
        bin_manager.write_pandemona_file(pandemona_folder)
