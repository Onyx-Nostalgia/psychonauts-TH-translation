import argparse
import csv
import os
import re
import struct

import constants
from character import get_character_names
from utils.file_util import get_filenames, read_binary, save_binary

# ENCODING = 'iso8859-11'
ENCODING = 'utf-8'

class FileReader:

    def __init__(self, data):
        self.offset = 0
        self.data = data

    def skip(self, size):
        self.offset += size

    def read(self, size):
        out = self.data[int(self.offset) : int(self.offset + size)]
        self.skip(size)
        return out

    def read_int32(self):
        return struct.unpack("<I", self.read(4))[0]

    def read_byte(self):
        return struct.unpack("B", self.read(1))[0]

    def read_sign(self):
        return struct.unpack("<4s", self.read(4))[0]


##############################################################


class LuaHeader:

    def __init__(self, data):
        self.signature = data.read_sign()
        self.version = data.read_byte()
        self.endian = data.read_byte()
        self.size_int = data.read_byte()
        self.size_size_t = data.read_byte()
        self.size_of_instruction = data.read_byte()
        self.SIZE_INSTRUCTION = data.read_byte()
        self.SIZE_OP = data.read_byte()
        self.SIZE_B = data.read_byte()
        self.sizeof_number = data.read_byte()
        data.skip(self.sizeof_number * 1)

    def valid_sign(self):
        return self.signature == b"\x1bLua"

    def valid_version(self):
        return self.version == 0x40


class LuaString:

    def __init__(self, data):
        self.size = data.read_int32()
        self.str = data.read(self.size)

    def __repr__(self):
        # skip zero
        return self.str.rstrip(b"\x00").decode("latin-1")


class LocalOne:

    def __init__(self, data):
        self.name = LuaString(data)
        self.startpc = data.read_int32()
        self.endpc = data.read_int32()


class LocalsAll:

    def __init__(self, data):
        loc_vars = data.read_int32()
        self.vars = []
        for _ in range(loc_vars):
            self.vars.append(LocalOne(data))


class LuaLines:

    def __init__(self, data):
        nlineinfo = data.read_int32()
        data.skip(nlineinfo * 4)


class LuaCode:

    def __init__(self, data):
        global header
        ncode = data.read_int32()
        if ncode == 0:
            return
        data.skip(header.SIZE_INSTRUCTION / 8 * ncode)


class LuaConstants:

    def __init__(self, data):
        # strings used by the function
        self.str = []
        str_count = data.read_int32()
        for _ in range(str_count):
            self.str.append(LuaString(data))

        # numbers used by the function
        num_count = data.read_int32()
        data.skip(num_count * 4)

        # functions defined inside the function
        self.func = []
        func_count = data.read_int32()
        for _ in range(func_count):
            self.func.append(LuaFunction(data))


class LuaFunction:

    def __init__(self, data):
        self.name = LuaString(data)
        data.skip(0xD)  # func args
        self.locals = LocalsAll(data)
        self.lines = LuaLines(data)
        self.const = LuaConstants(data)
        self.code = LuaCode(data)


##############################################################


class LUBParser:

    def __init__(self):
        self.str = []
        self.re_str_id = re.compile("[0-9A-Z]{9}")
        self.character_names = get_character_names()

    def show_result(self):
        print("Parsed {} string(s)".format(len(self.str)))

    def parse(self, path, dest_folder=None):
        print("unpacking {}...".format(path))
        _bin = read_binary(path)
        reader = FileReader(_bin)
        self.parse_data(reader)
        if dest_folder:
            filename = path.split("/")[-1]
            path = os.path.join(dest_folder, filename)
        if len(self.str) == 0:
            print("No Dialogue Content.")
            return 
        self.save_csv(path)
        self.show_result()

    def parse_data(self, data):
        global header
        header = LuaHeader(data)

        if not header.valid_sign():
            raise ValueError("Invalid LUB Signature")

        if not header.valid_version():
            raise ValueError("Invalid LUB Version")

        func = LuaFunction(data)
        self.parse_func(func)

    def is_lua_str_id(self, string):
        return self.re_str_id.match(string)

    def parse_func(self, func):
        self.parse_func_str(func)

        for ffnc in func.const.func:
            self.parse_func(ffnc)

    def parse_func_str(
        self,
        func,
    ):
        last_id = None
        for fstr in func.const.str:
            fstr = str(fstr)
            if last_id is None:
                if self.is_lua_str_id(fstr):
                    last_id = fstr
            else:
                if not self.is_lua_str_id(fstr):
                    # fstr.replace('\r', '') ?
                    character = self.character_names[last_id[-2:]]["EN"]
                    final_str = "{};{};{};{}".format(last_id, character, fstr, "")
                    self.str.append(final_str)
                    last_id = None
                else:
                    last_id = fstr

    def save_csv(self, path):
        header = "id;character;origin_dialogue;translated_dialogue"
        new_path = path[:-4] + ".csv"
        # save_binary(new_path, str_data,encode="latin-1")

        # Check if the CSV file already exists and read its content
        if os.path.exists(new_path):
            with open(new_path, "r", newline="", encoding=ENCODING,errors='ignore') as csvfile:
                reader = csv.reader(
                    csvfile,
                    quoting=csv.QUOTE_MINIMAL,
                    quotechar='"',
                    escapechar="\\",
                    delimiter=";",
                )
                try:
                    existing_rows = {row[0]: row for row in reader}
                except UnicodeDecodeError:
                    print(existing_rows)
                    raise UnicodeDecodeError
        else:
            existing_rows = {}

        # Update rows with existing translations if available
        updated_rows = [header]
        for line in self.str:
            row = line.split(";")
            if row[0] in existing_rows:
                existing_row = existing_rows[row[0]]
                try:
                    row[3] = existing_row[3]  # Preserve the translated dialogue
                except IndexError:
                    print(existing_row)
                    raise IndexError
            updated_rows.append(";".join(row))

        with open(new_path, "w", newline="",encoding=ENCODING,errors='ignore') as csvfile:
            writer = csv.writer(
                csvfile,
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                escapechar="\\",
                delimiter=";",
            )
            for line in updated_rows:
                row = line.split(";")
                writer.writerow(row)


##############################################################


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Convert *.LUB files (compiled lua4) to *.CSV (plain text) files"
    )
    arg_parser.add_argument("--file", dest="lub_file_path", required=False)
    arg_parser.add_argument("--folder", dest="lub_folder_path", required=False)
    arg_parser.add_argument(
        "--dest",
        dest="dest_folder",
        required=False,
        default=constants.DIALOGUES_FOLDER_NAME,
    )
    args = arg_parser.parse_args()

    if args.lub_folder_path:
        file_paths = get_filenames(args.lub_folder_path, type=".lub")
        for file_path in file_paths:
            lub_parser = LUBParser()
            lub_parser.parse(file_path, args.dest_folder)

    elif args.lub_file_path:
        lub_parser = LUBParser()
        lub_parser.parse(args.lub_file_path, args.dest_folder)
