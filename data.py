import os
from FF8GameData.FF8HexReader.mngrp import Mngrp
from FF8GameData.FF8HexReader.mngrphd import Mngrphd
from FF8GameData.gamedata import GameData
from FF8GameData.m00x.dataclass import m000bin, m001bin, m002bin, m003bin, m004bin, TypeId


class BinManager:
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
