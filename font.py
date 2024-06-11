import os
class FontManagement():
    def __init__(self):
        self.translate_hex_to_str_table = []
        self.__init_hex_to_str_table()

    def __init_hex_to_str_table(self):
        with open("Resources/sysfnt.txt", "r", encoding="utf-8") as localize_file:
            self.translate_hex_to_str_table = localize_file.read()
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.replace(',",",',
                                                                                      ',";;;",')  # Handling the unique case of a "," character (which is also a separator)
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.replace('\n', '')
            self.translate_hex_to_str_table = self.translate_hex_to_str_table.split(',')
            for i in range(len(self.translate_hex_to_str_table)):
                self.translate_hex_to_str_table[i] = self.translate_hex_to_str_table[i].replace(';;;', ',')
                if self.translate_hex_to_str_table[i].count('"') == 2:
                    self.translate_hex_to_str_table[i] = self.translate_hex_to_str_table[i].replace('"', '')

    def translate_str_to_hex(self, string):
        c = 0
        str_size = len(string)
        encode_list = []
        while c < str_size:
            char = string[c]
            if char == '\n':  # \n{NewPage}\n,\n
                if '{NewPage}' in string[c + 1:c + 10]:
                    encode_list.append(0x01)
                    c += 10
                else:
                    encode_list.append(0x02)
                    c += 1
                continue
            elif char == '{':
                rest = string[c + 1:]
                index_next_bracket = rest.find('}')
                if index_next_bracket != -1:
                    substring = rest[:index_next_bracket]
                    if substring in self.CHARACTER_LIST:  # {name}
                        index_list = self.CHARACTER_LIST.index(substring)
                        if index_list < 11:
                            encode_list.extend([0x03, 0x30 + index_list])
                        elif index_list == 11:
                            encode_list.extend([0x03, 0x40])
                        elif index_list == 12:
                            encode_list.extend([0x03, 0x50])
                        elif index_list == 13:
                            encode_list.extend([0x03, 0x60])
                    elif substring in self.COLOR_LIST:  # {Color}
                        index_list = self.COLOR_LIST.index(substring)
                        encode_list.extend([0x06, 0x20 + index_list])
                    elif substring in self.LOCATION_LIST:  # {Location}
                        index_list = self.LOCATION_LIST.index(substring)
                        encode_list.extend([0x0e, 0x20 + index_list])
                    elif 'Var' in substring:
                        if len(substring) == 5:
                            if 'b' in substring:  # {Varb0}
                                encode_list.extend([0x04, int(substring[-1]) + 0x40])
                            else:  # {Var00}
                                encode_list.extend([0x04, int(substring[-1]) + 0x30])
                        else:  # {Var0}
                            encode_list.extend([0x04, int(substring[-1]) + 0x20])
                    elif 'Wait' in substring:  # {Wait000}
                        encode_list.extend([0x09, int(substring[-1]) + 0x20])
                    elif 'Jp' in substring:  # {Jp000}
                        encode_list.extend([0x1c, int(substring[-1]) + 0x20])
                    elif '{' + substring + '}' in self.translate_hex_to_str_table:  # {} at end of sysfnt
                        encode_list.append(self.translate_hex_to_str_table[self.translate_hex_to_str_table.index('{' + substring + '}')])
                    elif 'x' in substring and len(substring) == 5:  # {xffff}
                        encode_list.extend([int(substring[1:3], 16), int(substring[3:5], 16)])
                    elif 'x' in substring and len(substring) == 3:  # {xff}
                        encode_list.append(int(substring[1:3], 16))
                    c += len(substring) + 2
                    continue
            encode_list.append(self.translate_hex_to_str_table.index(char))
            c += 1
            # Jp ?
        return encode_list

    def translate_hex_to_str(self, hex_list):
        str = ""
        i = 0
        hex_size = len(hex_list)
        while i < hex_size:
            hex_val = hex_list[i]

            if hex_val == 0x00:
                pass
            elif hex_val in [0x01, 0x02]:
                str += self.translate_hex_to_str_table[hex_val]
            elif hex_val == 0x03:  # {Name}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x30 and hex_val <= 0x3a:
                        str += '{' + self.CHARACTER_LIST[hex_val - 0x30] + '}'
                    elif hex_val == 0x40:
                        str += '{' + self.CHARACTER_LIST[11] + '}'
                    elif hex_val == 0x50:
                        str += '{' + self.CHARACTER_LIST[12] + '}'
                    elif hex_val == 0x60:
                        str += '{' + self.CHARACTER_LIST[13] + '}'
                    else:
                        str += "{{x03{:02x}}}".format(hex_val)
                else:
                    str += "{x03}"
            elif hex_val == 0x04:  # {Var0}, {Var00} et {Varb0}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and i <= 0x27:
                        str += "{{Var{:02x}}}".format(hex_val - 0x20)
                    elif hex_val >= 0x30 and i <= 0x37:
                        str += "{{Var0{:02x}}}".format(hex_val - 0x30)
                    elif hex_val >= 0x40 and i <= 0x47:
                        str += "{{Varb{:02x}}}".format(hex_val - 0x40)
                    else:
                        str += "{{x04{:02x}}}".format(hex_val)

                else:
                    str += "{x04}"
            elif hex_val == 0x06:  # {Color}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and hex_val <= 0x2f:
                        str += '{' + self.COLOR_LIST[hex_val - 0x20] + '}'
                    else:
                        str += "{{x06{:02x}}}".format(hex_val)
                else:
                    str += "{x06}"
            elif hex_val == 0x09:  # {Wait000}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        str += "{{Wait{:03}}}".format(hex_val - 0x20)
                    else:
                        str += "{{x09{:02x}}}".format(hex_val)
                else:
                    str += "{x06}"
            elif hex_val == 0x0e:  # {Location}
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20 and hex_val <= 0x27:
                        str += '{' + self.LOCATION_LIST[hex_val - 0x20] + '}'
                    else:
                        str += "{{x0e{:02x}}}".format(hex_val)
                else:
                    str += "{x0e}"
            elif hex_val >= 0x019 and hex_val <= 0x1b:  # jp19, jp1a, jp1b
                i += 1
                if i < len(hex_list):
                    old_hex_val = hex_val
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        character = None  # To be changed, caract(index, oldIndex-0x18);
                    else:
                        character = None
                    if not character:
                        character = "{{x{:02x}{:02x}}}".format(old_hex_val, hex_val)
                    str += character
                else:
                    str += "{{x{:02x}}}".format(hex_val)
            elif hex_val == 0x1c:  # addJp
                i += 1
                if i < hex_size:
                    hex_val = hex_list[i]
                    if hex_val >= 0x20:
                        str += "{{Jp{:03}}}".format(hex_val - 0x20)
                    else:
                        str += "{{x1c{:02x}}}".format(hex_val)
                else:
                    str += "{x1c}"
            elif hex_val >= 0x05 and hex_val <= 0x1f:
                i += 1
                if i < hex_size:
                    str += "{{x{:02x}{:02x}}}".format(hex_val, hex_list[i])
                else:
                    str += "{{x{:02x}}}".format(hex_val)
            else:
                character = self.translate_hex_to_str_table[hex_val]  # To be done
                if not character:
                    character = "{{x{:02x}}}".format(hex_val)
                str += character
            i += 1
        return str