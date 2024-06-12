import argparse
import glob
import os
import sys

from data import m000bin, BinManager, m001bin, m002bin, m003bin, m004bin
from gamedata import GameData

m000_data_list = ['t_mag_rf', 'i_mag_rf', 'f_mag_rf', 'l_mag_rf', 'time_mag_rf', 'st_mag_rf', 'supt_mag_rf', 'forbid_mag_rf']
m000_entry_list = ['offset', 'amount_received', 'input_item_id', 'l_mag_rf', 'time_mag_rf', 'st_mag_rf', 'supt_mag_rf', 'forbid_mag_rf']
input_folder = 'InputFiles'
entry_bin_file = os.path.join(input_folder, 'm000.bin')
entry_msg_file = os.path.join(input_folder, 'm000.msg')
output_folder = 'OutputFiles'
output_file = os.path.join(output_folder, 'output.txt')

# The m00x.bin files consist of a data for each abilities. Each "data (abilities) has an entry of x bytes.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pandemona", description="This program read m00x.bin files")
    args = parser.parse_args()

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Check if pandemona file exist.
    # If in the output folder there is pandemona files, it means we want to create .bin and .msg from it.
    # If the files doesn't exist, it means we want to create them first from the original files

    output_pandemona_list = glob.glob(os.path.join(output_folder, "*.pandemona"))
    if output_pandemona_list:  # Means we want to read pandemona files to write to .msg and .bin
        list_to_analyze = output_pandemona_list
        reading_pandemona = True
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
        else:
            print("Unexpected file {}".format(file))
            continue

        bin_manager = BinManager(bin_data, game_data)
        if reading_pandemona:
            bin_manager.read_pandemona_file(output_folder)
            bin_manager.write_bin_file(file.split('.')[0] + ".bin", file.split('.')[0] + ".msg")
        else:
            bin_manager.read_bin_file(file.split('.')[0] + ".bin", file.split('.')[0] + ".msg")
            bin_manager.write_pandemona_file(output_folder)
