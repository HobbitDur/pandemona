import argparse
import glob
import os
import shutil

from data import m000bin, BinManager, m001bin, m002bin, m003bin, m004bin
from gamedata import GameData

m000_data_list = ['t_mag_rf', 'i_mag_rf', 'f_mag_rf', 'l_mag_rf', 'time_mag_rf', 'st_mag_rf', 'supt_mag_rf',
                  'forbid_mag_rf']
m000_entry_list = ['offset', 'amount_received', 'input_item_id', 'l_mag_rf', 'time_mag_rf', 'st_mag_rf', 'supt_mag_rf',
                   'forbid_mag_rf']
input_folder = '1 - InputFiles'
pandemona_folder = '2 - PandemonaFiles'
output_folder = '3 - OutputFiles'

# The m00x.bin files consist of a data for each abilities. Each "data (abilities) has an entry of x bytes.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pandemona", description="This program read m00x.bin files")
    args = parser.parse_args()

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(pandemona_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Check if pandemona file exist.
    # If in the output folder there is pandemona files, it means we want to create .bin and .msg from it.
    # If the files doesn't exist, it means we want to create them first from the original files

    output_pandemona_list = glob.glob(os.path.join(pandemona_folder, "*.pandemona"))
    if len(output_pandemona_list) > 0:  # Means we want to read pandemona files to write to .msg and .bin
        list_to_analyze = output_pandemona_list
        reading_pandemona = True
        shutil.copyfile(os.path.join(input_folder, "mngrp.bin"), os.path.join(output_folder, "mngrp.bin"))
    else:  # Means we want to read .bin and .msg to create pandemona file
        list_to_analyze = glob.glob(os.path.join(input_folder, "*.bin"))
        reading_pandemona = False


    game_data = GameData()
    for file in list_to_analyze:
        if 'm000' in file:
            bin_data = m000bin()
        elif 'm001' in file:
            bin_data = m001bin()
        elif 'm002' in file:
            bin_data = m002bin()
        elif 'm003' in file:
            bin_data = m003bin()
        elif 'm004' in file:
            bin_data = m004bin()
        elif 'mngrp' in file:
            continue
        else:
            print("Unexpected file {}".format(file))
            continue

        bin_manager = BinManager(bin_data, game_data)
        file_name = file.split(os.sep)[1].split('.')[0]
        if reading_pandemona:
            bin_manager.read_pandemona_file(pandemona_folder)
            pre_file_name = os.path.join(output_folder, file_name)
            bin_manager.write_bin_file(pre_file_name + ".bin", pre_file_name + ".msg", os.path.join(output_folder, "mngrp.bin"))
        else:
            pre_file_name = os.path.join(input_folder, file_name)
            bin_manager.read_bin_file(pre_file_name + ".bin",pre_file_name + ".msg")
            bin_manager.write_pandemona_file(pandemona_folder)
