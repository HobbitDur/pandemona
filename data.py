import binascii
import os
from dataclasses import dataclass

from font import FontManagement


@dataclass
class Entry():
    text_offset: int = 0
    text_offset_size = 2
    amount_received: int = 0
    unk: int = 0
    entry_id: int = 0
    amount_required: int = 0
    output_id: int = 0
    ENTRY_SIZE: int = 8  # Nb_element
    text: str = ""


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
        self.t_mag_rf = Data(name='t_mag_rf', offset=0x0, description='Item to Thunder/Wind Magic', nb_entries=7, entries=[Entry() for _ in range(7)])
        self.i_mag_rf = Data(name='i_mag_rf', offset=0x38, description='Item to Ice/Water Magic', nb_entries=7, entries=[Entry() for _ in range(7)])
        self.f_mag_rf = Data(name='f_mag_rf', offset=0x70, description='Item to Fire/Flare Magic', nb_entries=10, entries=[Entry() for _ in range(10)])
        self.l_mag_rf = Data(name='l_mag_rf', offset=0xC0, description='Item to Life Magic', nb_entries=10, entries=[Entry() for _ in range(10)])
        self.time_mag_rf = Data(name='time_mag_rf', offset=0x168, description='Item to Time Magic', nb_entries=14, entries=[Entry() for _ in range(14)])
        self.st_mag_rf = Data(name='st_mag_rf', offset=0x1D8, description='Item to Status Magic', nb_entries=17, entries=[Entry() for _ in range(17)])
        self.supt_mag_rf = Data(name='supt_mag_rf', offset=0x260, description='Item to Support Magic', nb_entries=20, entries=[Entry() for _ in range(20)])
        self.forbid_mag_rf = Data(name='forbid_mag_rf', offset=0x300, description='Item to Support Magic', nb_entries=6, entries=[Entry() for _ in range(6)])
        self.list_data = (self.t_mag_rf, self.i_mag_rf, self.f_mag_rf, self.l_mag_rf, self.time_mag_rf, self.st_mag_rf, self.supt_mag_rf, self.forbid_mag_rf)


@dataclass
class m001bin():
    def __init__(self):
        self.name = "m001"
        self.recov_med_rf = Data(name='recov_med_rf', offset=0x0, description='Item to Recovery Items', nb_entries=9, entries=[Entry() for _ in range(9)])
        self.st_med_rf = Data(name='st_med_rf', offset=0x48, description='Item to Status Removal Items', nb_entries=12, entries=[Entry() for _ in range(12)])
        self.amo_rf = Data(name='amo_rf', offset=0xA8, description='Item to Ammo Item', nb_entries=16, entries=[Entry() for _ in range(16)])
        self.forbid_med_rf = Data(name='forbid_med_rf', offset=0x128, description='Item to Forbidden Medicine', nb_entries=20, entries=[Entry() for _ in range(20)])
        self.gfrecov_med_rf = Data(name='gfrecov_med_rf', offset=0x1C8, description='Item to GF Recovery Items', nb_entries=12, entries=[Entry() for _ in range(12)])
        self.gfabl_med_rf = Data(name='gfabl_med_rf', offset=0x228, description='Item to GF Ability Medicine Items', nb_entries=42, entries=[Entry() for _ in range(42)])
        self.tool_rf = Data(name='tool_rf', offset=0x378, description='Item to Tool Items', nb_entries=32, entries=[Entry() for _ in range(32)])
        self.list_data = (self.recov_med_rf, self.st_med_rf, self.amo_rf, self.forbid_med_rf, self.gfrecov_med_rf, self.gfabl_med_rf, self.tool_rf)


@dataclass
class m002bin():
    def __init__(self):
        self.name = "m002"
        self.mid_mag_rf = Data(name='mid_mag_rf', offset=0x0, description='Upgrade Magic from low level to mid level', nb_entries=4, entries=[Entry() for _ in range(4)])
        self.high_mag_rf = Data(name='high_mag_rf', offset=0x20, description='Upgrade Magic from mid level to high level', nb_entries=6, entries=[Entry() for _ in range(6)])
        self.list_data = (self.mid_mag_rf, self.high_mag_rf)


@dataclass
class m003bin():
    def __init__(self):
        self.name = "m003"
        self.med_lv_up = Data(name='med_lv_up', offset=0x0, description='Level up low level recovery items to higher items', nb_entries=12,
                              entries=[Entry() for _ in range(12)])
        self.list_data = (self.med_lv_up,)


@dataclass
class m004bin():
    def __init__(self):
        self.name = "m004"
        self.card_mod = Data(name='card_mod', offset=0x0, description='ICard to Items', nb_entries=110, entries=[Entry()] * 110)
        self.list_data = (self.card_mod,)


class BinManager():
    CHAR_SEP = '>'

    def __init__(self, bin):
        self.bin = bin
        self.file_bin_data = bytearray()
        self.file_msg_data = bytearray()
        self.font_mgmt = FontManagement()

    def read_bin_file(self, file_bin, file_msg):
        print("readbilfine")
        with open(file_msg, "rb") as file:
            while char := file.read(1):
                self.file_msg_data.extend(char)
        with open(file_bin, "rb") as file:
            for char in file:
                self.file_bin_data.extend(char)

        for data in self.bin.list_data:
            index = data.offset
            for entry in data.entries:
                entry.text_offset = int.from_bytes(bytearray(self.file_bin_data[index:index + 2]), byteorder='little')
                entry.amount_received = int(self.file_bin_data[index + 2])
                entry.unk = int.from_bytes(bytearray(self.file_bin_data[index + 3:index + 5]), byteorder='little')
                entry.input_id = int(self.file_bin_data[index + 5])
                entry.amount_required = int(self.file_bin_data[index + 6])
                entry.output_id = int(self.file_bin_data[index + 7])
                raw_data_text = self.file_msg_data[entry.text_offset:self.file_msg_data.index(bytes([0]), entry.text_offset)]
                entry.text = self.font_mgmt.translate_hex_to_str(raw_data_text)
                index += entry.ENTRY_SIZE



    def write_bin_file(self, file_bin, file_msg):
        for data in self.bin.list_data:
            for entry in data.entries:
                self.file_bin_data.extend(entry.text_offset)
                self.file_bin_data.extend([entry.amount_received])
                self.file_bin_data.extend(entry.unk)
                self.file_bin_data.extend([entry.input_id])
                self.file_bin_data.extend([entry.amount_required])
                self.file_bin_data.extend([entry.output_id])
                self.file_msg_data.extend(entry.text)

        with open(file_bin, "wb") as file:
            file.write(self.file_bin_data)
        with open(file_msg, "wb") as file:
            file.write(self.file_msg_data)

    def read_pandemona_file(self, path_input):
        with open(os.path.join(path_input, self.bin.name + '.pandemona'), "r") as file:
            str_read = file.readlines()

        current_line = 0
        for index_data, data in enumerate(self.bin.list_data):
            current_line+=1 # Line of data description ignored
            for nb_entry, entry in enumerate(data.entries):
                current_line += 1  # Ignoring the first line that just specify the entry index
                print(str_read[current_line])
                print(str_read[current_line].split(f'{self.CHAR_SEP}')[1])
                entry.text = self.font_mgmt.translate_str_to_hex(str_read[current_line].split(f'{self.CHAR_SEP}')[1])
                entry.text_offset = int(str_read[current_line + 1].split(f'{self.CHAR_SEP}')[1]).to_bytes(2, byteorder='little')
                entry.amount_received = int(str_read[current_line + 2].split(f'{self.CHAR_SEP}')[1])
                entry.unk = int(str_read[current_line + 3].split(f'{self.CHAR_SEP}')[1]).to_bytes(2, byteorder='little')
                entry.input_id = int(str_read[current_line + 4].split(f'{self.CHAR_SEP}')[1])
                entry.amount_required = int(str_read[current_line + 5].split(f'{self.CHAR_SEP}')[1])
                entry.output_id = int(str_read[current_line + 6].split(f'{self.CHAR_SEP}')[1])
                current_line += 7

    def write_pandemona_file(self, path_output):
        print("Writing pandeoma file")
        str_output = ""
        for index_data, data in enumerate(self.bin.list_data):
            str_output+=  f"Data n°{index_data}, name:{data.name}, data description:{data.description}\n"
            for nb_entry, entry in enumerate(data.entries):
                str_entry = ""
                str_entry += f"Entry n°{nb_entry}\n"
                str_entry += f"Text{self.CHAR_SEP}{entry.text}\n"
                str_entry += f"Text offset (don't touch if you don't know what you are doing){self.CHAR_SEP}{entry.text_offset}\n"
                str_entry += f"Amount received{self.CHAR_SEP}{entry.amount_received}\n"
                str_entry += f"unk{self.CHAR_SEP}{entry.unk}\n"
                str_entry += f"Input ID{self.CHAR_SEP}{entry.input_id}\n"
                str_entry += f"Amount required{self.CHAR_SEP}{entry.amount_required}\n"
                str_entry += f"Output ID{self.CHAR_SEP}{entry.output_id}\n"
                str_output+=str_entry
        with open(os.path.join(path_output, self.bin.name + '.pandemona'), "w") as file:
            file.write(str_output)
