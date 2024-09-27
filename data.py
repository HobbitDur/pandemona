import binascii
import os
from dataclasses import dataclass

from FF8GameData.FF8HexReader.mngrp import Mngrp
from FF8GameData.FF8HexReader.mngrphd import Mngrphd
from FF8GameData.gamedata import GameData


@dataclass
class TypeId():
    ITEM: int = 0
    SPELL: int = 1
    CARD: int = 2


@dataclass
class Entry():
    text_offset: int = 0
    text_offset_size = 2
    amount_received: int = 0
    unk: int = 0
    element_in_id: int = 0
    amount_required: int = 0
    element_out_id: int = 0
    ENTRY_SIZE: int = 8  # Nb_element
    text = "" # Str or list to be given to bytearray


@dataclass
class Data():
    name: str
    offset: int
    description: str
    nb_entries: int
    entries: list


@dataclass
class m000bin():
    def __init__(self):
        self.name = "m000"
        self.t_mag_rf = Data(name='t_mag_rf', offset=0x0, description='Item to Thunder/Wind Magic', nb_entries=7,
                             entries=[Entry() for _ in range(7)])
        self.i_mag_rf = Data(name='i_mag_rf', offset=0x38, description='Item to Ice/Water Magic', nb_entries=7,
                             entries=[Entry() for _ in range(7)])
        self.f_mag_rf = Data(name='f_mag_rf', offset=0x70, description='Item to Fire/Flare Magic', nb_entries=10,
                             entries=[Entry() for _ in range(10)])
        self.l_mag_rf = Data(name='l_mag_rf', offset=0xC0, description='Item to Life Magic', nb_entries=21,
                             entries=[Entry() for _ in range(21)])
        self.time_mag_rf = Data(name='time_mag_rf', offset=0x168, description='Item to Time Magic', nb_entries=14,
                                entries=[Entry() for _ in range(14)])
        self.st_mag_rf = Data(name='st_mag_rf', offset=0x1D8, description='Item to Status Magic', nb_entries=17,
                              entries=[Entry() for _ in range(17)])
        self.supt_mag_rf = Data(name='supt_mag_rf', offset=0x260, description='Item to Support Magic', nb_entries=20,
                                entries=[Entry() for _ in range(20)])
        self.forbid_mag_rf = Data(name='forbid_mag_rf', offset=0x300, description='Item to Support Magic', nb_entries=6,
                                  entries=[Entry() for _ in range(6)])
        self.list_data = (self.t_mag_rf, self.i_mag_rf, self.f_mag_rf, self.l_mag_rf, self.time_mag_rf, self.st_mag_rf, self.supt_mag_rf, self.forbid_mag_rf)
        self.input_id = TypeId.ITEM
        self.output_id = TypeId.SPELL
        self.mngrp_bin_id = 106
        self.mngrp_msg_id = 111


@dataclass
class m001bin():
    def __init__(self):
        self.name = "m001"
        self.recov_med_rf = Data(name='recov_med_rf', offset=0x0, description='Item to Recovery Items', nb_entries=9,
                                 entries=[Entry() for _ in range(9)])
        self.st_med_rf = Data(name='st_med_rf', offset=0x48, description='Item to Status Removal Items', nb_entries=12,
                              entries=[Entry() for _ in range(12)])
        self.amo_rf = Data(name='amo_rf', offset=0xA8, description='Item to Ammo Item', nb_entries=16,
                           entries=[Entry() for _ in range(16)])
        self.forbid_med_rf = Data(name='forbid_med_rf', offset=0x128, description='Item to Forbidden Medicine',
                                  nb_entries=20,
                                  entries=[Entry() for _ in range(20)])
        self.gfrecov_med_rf = Data(name='gfrecov_med_rf', offset=0x1C8, description='Item to GF Recovery Items',
                                   nb_entries=12,
                                   entries=[Entry() for _ in range(12)])
        self.gfabl_med_rf = Data(name='gfabl_med_rf', offset=0x228, description='Item to GF Ability Medicine Items',
                                 nb_entries=42,
                                 entries=[Entry() for _ in range(42)])
        self.tool_rf = Data(name='tool_rf', offset=0x378, description='Item to Tool Items', nb_entries=32,
                            entries=[Entry() for _ in range(32)])
        self.list_data = (self.recov_med_rf, self.st_med_rf, self.amo_rf, self.forbid_med_rf, self.gfrecov_med_rf, self.gfabl_med_rf, self.tool_rf)
        self.input_id = TypeId.ITEM
        self.output_id = TypeId.ITEM
        self.mngrp_bin_id = 107
        self.mngrp_msg_id = 112


@dataclass
class m002bin():
    def __init__(self):
        self.name = "m002"
        self.mid_mag_rf = Data(name='mid_mag_rf', offset=0x0, description='Upgrade Magic from low level to mid level',
                               nb_entries=4,
                               entries=[Entry() for _ in range(4)])
        self.high_mag_rf = Data(name='high_mag_rf', offset=0x20,
                                description='Upgrade Magic from mid level to high level', nb_entries=6,
                                entries=[Entry() for _ in range(6)])
        self.list_data = (self.mid_mag_rf, self.high_mag_rf)
        self.input_id = TypeId.ITEM
        self.output_id = TypeId.SPELL
        self.mngrp_bin_id = 108
        self.mngrp_msg_id = 113

@dataclass
class m003bin():
    def __init__(self):
        self.name = "m003"
        self.med_lv_up = Data(name='med_lv_up', offset=0x0,
                              description='Level up low level recovery items to higher items', nb_entries=12,
                              entries=[Entry() for _ in range(12)])
        self.list_data = (self.med_lv_up,)
        self.input_id = TypeId.ITEM
        self.output_id = TypeId.ITEM
        self.mngrp_bin_id = 109
        self.mngrp_msg_id = 114


@dataclass
class m004bin():
    def __init__(self):
        self.name = "m004"
        self.card_mod = Data(name='card_mod', offset=0x0, description='Card to Items', nb_entries=110,
                             entries=[Entry() for _ in range(110)])
        self.list_data = (self.card_mod,)
        self.input_id = TypeId.CARD
        self.output_id = TypeId.ITEM
        self.mngrp_bin_id = 110
        self.mngrp_msg_id = 115


class BinManager():
    CHAR_SEP = '>'

    def __init__(self, game_data: GameData):
        self.m000bin = m000bin()
        self.m001bin = m001bin()
        self.m002bin = m002bin()
        self.m003bin = m003bin()
        self.m004bin = m004bin()
        self.bin_list = (self.m000bin, self.m001bin, self.m002bin, self.m003bin,self.m004bin)

        self.mngrp = None
        self.mngrphd = None
        self.game_data = game_data


    def read_mngrp_file(self, file_mngrp, file_mngrphd):
        file_mngrp_data = bytearray()
        with open(file_mngrp, "rb") as file:
            file_mngrp_data.extend(file.read())
        file_mngrphd_data = bytearray()
        with open(file_mngrphd, "rb") as file:
            file_mngrphd_data.extend(file.read())

        self.mngrphd = Mngrphd(game_data=self.game_data, data_hex=file_mngrphd_data)
        self.mngrp = Mngrp(game_data=self.game_data, data_hex=file_mngrp_data, header_entry_list=self.mngrphd.get_valid_entry_list())

        for bin_data in self.bin_list:
            if bin_data.input_id == TypeId.CARD:
                input_table = self.game_data.card_data_json["card_info"]
            elif bin_data.input_id == TypeId.SPELL:
                input_table = self.game_data.magic_data_json["magic"]
            elif bin_data.input_id == TypeId.ITEM:
                input_table = self.game_data.item_data_json['items']
            else:
                print("Error reading input table")
                exit(0)
            if bin_data.output_id == TypeId.CARD:
                output_table = self.game_data.card_data_json["card_info"]
            elif bin_data.output_id == TypeId.SPELL:
                output_table = self.game_data.magic_data_json["magic"]
            elif bin_data.output_id == TypeId.ITEM:
                output_table = self.game_data.item_data_json['items']
            else:
                print("Error reading output table")
                exit(0)
            file_bin_data = self.mngrp.get_section_by_id(bin_data.mngrp_bin_id).get_data_hex()
            for data in bin_data.list_data:
                index = data.offset
                for entry in data.entries:
                    entry.text_offset = int.from_bytes(bytearray(file_bin_data[index:index + 2]), byteorder='little')
                    entry.amount_received = int(file_bin_data[index + 2])
                    entry.unk = int.from_bytes(bytearray(file_bin_data[index + 3:index + 5]), byteorder='little')
                    entry.element_in_id = str(int(file_bin_data[index + 5])) + ':' + input_table[int(file_bin_data[index + 5])]['name']
                    entry.amount_required = int(file_bin_data[index + 6])
                    entry.element_out_id = str(int(file_bin_data[index + 7])) + ':' + output_table[int(file_bin_data[index + 7])]['name']
                    index += entry.ENTRY_SIZE

        for index_bin_data, bin_data in enumerate(self.bin_list):

            file_msg_data =self.mngrp.get_section_by_id(bin_data.mngrp_msg_id).get_data_hex()
            for index_data, data in enumerate(bin_data.list_data):
                for index_data_entry, data_entry in enumerate(data.entries):
                    if index_data_entry == len(data.entries)-1 and index_data == len(bin_data.list_data)-1 and index_bin_data == len(self.bin_list)-1:
                        end_offset = len(file_msg_data)
                    elif index_data_entry == len(data.entries)-1 and index_data == len(bin_data.list_data)-1:
                        end_offset = self.bin_list[index_bin_data+1].list_data[0].entries[0].text_offset
                    elif index_data_entry == len(data.entries)-1:
                        end_offset =  self.bin_list[index_bin_data].list_data[index_data+1].entries[0].text_offset
                    else:
                        end_offset= data.entries[index_data_entry + 1].text_offset
                    raw_data_text = file_msg_data[data_entry.text_offset:end_offset]
                    self.bin_list[index_bin_data].list_data[index_data].entries[index_data_entry].text = self.game_data.translate_hex_to_str(raw_data_text)

    def write_mngrp_file(self, file_mngrp, file_mngrphd):
        file_mngrp_data = bytearray()
        with open(file_mngrp, "rb") as file:
            file_mngrp_data.extend(file.read())
        file_mngrphd_data = bytearray()
        with open(file_mngrphd, "rb") as file:
            file_mngrphd_data.extend(file.read())

        self.mngrphd = Mngrphd(game_data=self.game_data, data_hex=file_mngrphd_data)
        self.mngrp = Mngrp(game_data=self.game_data, data_hex=file_mngrp_data, header_entry_list=self.mngrphd.get_valid_entry_list())


        for bin_data in self.bin_list:
            file_bin_data = bytearray()
            file_msg_data = bytearray()
            for data in bin_data.list_data:
                for entry in data.entries:
                    file_bin_data.extend(entry.text_offset)
                    file_bin_data.extend([entry.amount_received])
                    file_bin_data.extend(entry.unk)
                    file_bin_data.extend([entry.element_in_id])
                    file_bin_data.extend([entry.amount_required])
                    file_bin_data.extend([entry.element_out_id])
                    file_msg_data.extend(entry.text)

            self.mngrp.set_section_by_id(bin_data.mngrp_bin_id, file_bin_data, self.mngrphd)
            self.mngrp.set_section_by_id(bin_data.mngrp_msg_id, file_msg_data, self.mngrphd)

        with open(file_mngrp, "wb") as file:
            file.write(file_mngrp_data)

        with open(file_mngrphd, "wb") as file:
            file.write(file_mngrphd_data)

    def read_pandemona_file(self, path_input):
        current_line = 0
        text_offset = 0
        for mbin in self.bin_list:
            with open(os.path.join(path_input, mbin.name + '.pandemona'), "r", encoding="utf8") as file:
                str_read = file.readlines()
            for index_data, data in enumerate(mbin.list_data):
                current_line += 1  # Line of data description ignored
                for nb_entry, entry in enumerate(data.entries):
                    current_line += 1  # Ignoring the first line that just specify the entry index
                    # Using [:-1] to remove the \n that we manually added
                    text_read = str_read[current_line].split(f'{self.CHAR_SEP}')[1][:-1]
                    entry.text = self.game_data.translate_str_to_hex(text_read)
                    entry.text.extend([0x00])  # Adding the 0x00 that have been removed to note the end of the string
                    entry.text_offset = text_offset.to_bytes(2, byteorder='little')
                    entry.element_in_id = int(str_read[current_line + 1].split(f'{self.CHAR_SEP}')[1][:-1].split(':')[0])
                    entry.amount_required = int(str_read[current_line + 2].split(f'{self.CHAR_SEP}')[1][:-1])
                    entry.element_out_id = int(str_read[current_line + 3].split(f'{self.CHAR_SEP}')[1][:-1].split(':')[0])
                    entry.amount_received = int(str_read[current_line + 4].split(f'{self.CHAR_SEP}')[1][:-1])
                    entry.unk = int(str_read[current_line + 5].split(f'{self.CHAR_SEP}')[1][:-1]).to_bytes(2,
                                                                                                           byteorder='little')
                    text_offset += len(text_read) +1# +1 for the 0x00 that have been added.
                    current_line += 6
                current_line += 1  # The ------\n alone added

    def write_pandemona_file(self, path_output):
        str_output = ""
        for mbin in self.bin_list:
            for index_data, data in enumerate(mbin.list_data):
                str_output += f"Data n°{index_data}, name:{data.name}, data description:{data.description}\n"
                for nb_entry, entry in enumerate(data.entries):
                    str_entry = ""
                    str_entry += f"Entry n°{nb_entry}\n"
                    str_entry += f"Text{self.CHAR_SEP}{entry.text}\n"
                    str_entry += f"Input ID{self.CHAR_SEP}{entry.element_in_id}\n"
                    str_entry += f"Amount required{self.CHAR_SEP}{entry.amount_required}\n"
                    str_entry += f"Output ID{self.CHAR_SEP}{entry.element_out_id}\n"
                    str_entry += f"Amount received{self.CHAR_SEP}{entry.amount_received}\n"
                    str_entry += f"unk{self.CHAR_SEP}{entry.unk}\n"
                    str_output += str_entry
                str_output += '-----------------------------------------------------------------\n'
            with open(os.path.join(path_output, mbin.name + '.pandemona'), "w", encoding="utf8") as file:
                file.write(str_output)
