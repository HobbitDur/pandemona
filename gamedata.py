import os


class GameData():
    RESOURCES_FOLDER = "Resources"
    ITEM_FILE = os.path.join(RESOURCES_FOLDER, "item.txt")
    SPELL_FILE = os.path.join(RESOURCES_FOLDER, "magic.txt")
    CARD_FILE = os.path.join(RESOURCES_FOLDER, "card.txt")

    def __init__(self):
        self.item_values = {}
        self.magic_values = {}
        self.card_values = {}
        self.load_item_data(self.ITEM_FILE)
        self.load_magic_data(self.SPELL_FILE)
        self.load_card_data(self.CARD_FILE)

    def load_card_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                split_line = el_split.split('<')
                self.card_values[int(split_line[0], 16)] = {'name': split_line[1],
                                                            'ref': str(int(split_line[0], 16)) + ":" + split_line[1]}

    def load_magic_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                split_line = el_split.split('<')
                self.magic_values[int(split_line[0], 16)] = {'name': split_line[1],
                                                             'ref': str(int(split_line[0], 16)) + ":" + split_line[1]}

    def load_item_data(self, file):
        with (open(file, "r") as f):
            file_split = f.read().split('\n')
            for el_split in file_split:
                split_line = el_split.split('<')
                self.item_values[int(split_line[0], 16)] = {'name': split_line[1],
                                                            'ref': str(int(split_line[0], 16)) + ":" + split_line[1]}
