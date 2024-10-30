import argparse
import os
import re

import click

import constants
from update_character import get_character_names
from utils.file_util import get_filenames


def get_template(file_path=constants.CUTSCENES_TEMPLATE_PATH):

    with open(file_path, mode="r") as f:
        text = f.read()
    start_marker = "<--start-template-->"
    end_marker = "<--end-template-->"
    start_length = len(start_marker)
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    string_template = text[start_index + start_length + 1 : end_index]
    return string_template


def read_dfs(file_path):
    with open(file_path, mode="r") as f:
        raw_rows = f.readlines()

    return [
        (raw_row[: constants.DIALOGUE_ID_LENGTH].upper(), raw_row)
        for raw_row in raw_rows
    ]


def get_dialogue(dialogue_ids, folder_path):
    """
    Output: {dialogue_id: [dialogue_id,character_id,origin_dialogue,translated_dialogue]}
    """
    dialogue_stack = {}
    filenames = get_filenames(folder_path)
    for filename in filenames:
        with open(filename, mode="r", encoding="latin-1") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id in dialogue_ids:
            if dialogue_id in dialogue_stack:
                continue
            start_index = csv_text.find(dialogue_id)
            end_index = csv_text.find("\n", start_index)
            if start_index != -1 and end_index != -1:
                dialogue = csv_text[start_index:end_index]
                dialogue_stack[dialogue_id] = dialogue.split(";")
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                return dialogue_stack

    # case id in .dfs not found in any dialogues
    difference_dialogues = set(dialogue_ids) - set(dialogue_stack.keys())
    print("🤔 {} dialogue not found.".format(", ".join(difference_dialogues)))
    return dialogue_stack


def map_cutscene_dialogues(cutscene_dialogues):
    return {
        dialogue["dfs"][: constants.DIALOGUE_ID_LENGTH].upper(): dialogue
        for dialogue in cutscene_dialogues
    }


def extract_cutscene_dialogue(file_path, template):
    if not os.path.exists(file_path):
        return
    with open(file_path, mode="r") as f:
        cutscene_text = f.read()
    pattern = re.escape(template)
    pattern = re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>.*)", pattern)
    cutscene_dialogues = [
        match.groupdict() for match in re.finditer(pattern, cutscene_text)
    ]
    cutscene_dialogues = map_cutscene_dialogues(cutscene_dialogues)
    return cutscene_dialogues


def __validate_character_cutscene(
    dialogue_id, exist_cutscene_dialogues, character_names
):
    character_id = dialogue_id[-2:]
    language_types = list(map(str.upper,character_names[character_id].keys()))
    character_obj = dict()
    for language in language_types:
        _character = character_names[character_id].get(language, character_id)
        _text = f"{language}_Character"
        character_obj[_text] = _character
        
        if exist_cutscene_dialogues:
            exist_cutscene_dialogue = exist_cutscene_dialogues[dialogue_id]
            if (
                _character == character_id
                and exist_cutscene_dialogue[_text] != character_id
            ):
                character_obj[_text] = exist_cutscene_dialogue[_text]
    return character_obj


def __validate_dialogue_cutscene(dialogue_id, exist_cutscene_dialogues, dialogues):
    en_dialogue = ""
    th_dialogue = ""
    if dialogue_id in dialogues:
        en_dialogue = dialogues[dialogue_id][2]
        th_dialogue = dialogues[dialogue_id][3].encode("latin-1").decode("utf-8")
    if exist_cutscene_dialogues:
        exist_cutscene_dialogue = exist_cutscene_dialogues[dialogue_id]
        th_dialogue = th_dialogue or exist_cutscene_dialogue["TH_Dialogue"]
    return {"EN_Dialogue": en_dialogue, "TH_Dialogue": th_dialogue}

def generate_dest_file_path(file_path,dest_folder):
    filename = file_path.split("/")[-1]
    if filename.endswith(".dfs"):
        filename = filename[:-4] + "_dialogue.txt"
        dest_file_path = os.path.join(dest_folder, filename)
    return dest_file_path  
      
      
def create_cutscene_dialogue(
    file_path,
    dest_folder=constants.CUTSCENES_FOLDER_NAME,
    dialogue_folder=constants.DIALOGUES_FOLDER_NAME,
    dry_run=False,
):
    dest_file_path = generate_dest_file_path(file_path,dest_folder)
    string_template = get_template()
    dfs_rows = read_dfs(file_path)
    dialogue_ids=[_id for _id, _ in dfs_rows]
    dialogues = get_dialogue(dialogue_ids, folder_path=dialogue_folder)
    exist_cutscene_dialogues = extract_cutscene_dialogue(
        dest_file_path, string_template
    )
    character_names = get_character_names()
    result = []
    for dialogue_id, dfs_row in dfs_rows:
        dfs = dfs_row.strip()
        character_cutscene = __validate_character_cutscene(
            dialogue_id, exist_cutscene_dialogues, character_names
        )
        dialogue_cutscene = __validate_dialogue_cutscene(
            dialogue_id, exist_cutscene_dialogues, dialogues
        )
        text = string_template.format(
            dfs=dfs,
            **character_cutscene,
            **dialogue_cutscene
        )
        result.append(text)

    if not dry_run:
        with open(dest_file_path, mode="w") as f:
            text = "".join(result)
            f.write(text)
    print("🤩 Created/Updated {}".format(dest_file_path))

def write_csv_dialogue(csv_text,filename,dry_run=False):
    if not filename.endswith(".csv"):
        click.echo(f"🤔 {filename} is not a csv file.")
        return
    if not dry_run:
        with open(filename, mode="wb") as csvfile:
            csvfile.write(csv_text)
    click.echo(f"🤩 Updated {filename}")

def __update_csv(file_path, string_template, dialogue_folder=constants.DIALOGUES_FOLDER_NAME,dry_run=False):
    """
    Output: {dialogue_id: dialogue_id;character_id;origin_dialogue;translated_dialogue;}
    """
    cutscene_dialogues = extract_cutscene_dialogue(
        file_path, string_template
    )
    dialogue_ids = cutscene_dialogues.keys()
    dialogue_stack = {}
    filenames = get_filenames(dialogue_folder)
    for filename in filenames:
        is_found = False
        with open(filename, mode="rb") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id,cutscene_dialogue in cutscene_dialogues.items():
            if dialogue_id in dialogue_stack:
                continue
            start_index = csv_text.find(dialogue_id.encode())
            end_index = csv_text.find("\n".encode(), start_index)
            if start_index != -1 and end_index != -1:
                is_found = True
                th_start_index = csv_text.rfind(";".encode(),start_index,end_index)
                
                # replace th dialogue from cutscene_dialogue to dialogue csv
                th_dialogue = cutscene_dialogue["TH_Dialogue"].lstrip()
                if th_dialogue:
                    csv_text = csv_text[:th_start_index+1] + th_dialogue.encode() + csv_text[end_index:]
                dialogue_stack[dialogue_id] = csv_text[start_index:th_start_index+1]+ th_dialogue.encode()
                
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                write_csv_dialogue(csv_text, filename, dry_run=dry_run)
                return dialogue_stack
        if is_found:
            write_csv_dialogue(csv_text, filename, dry_run=dry_run)
            
    # case id in cutscene not found in any dialogues
    difference_dialogues = set(dialogue_ids) - set(dialogue_stack.keys())
    print("🤔 {} dialogue not found.".format(", ".join(difference_dialogues)))
    return dialogue_stack
    
@click.group()
@click.option("--dry-run/--no-dry-run",default=False,help="Dry run")
@click.pass_context
def cli(ctx,dry_run):
    if dry_run:
        click.echo(f"{" (dry run) ":=^55}")
    ctx.ensure_object(dict)
    ctx.obj['DRY_RUN'] = dry_run

@cli.command()
@click.option("--all/--no-all","_all",default=False,help=f"Update all cutscene in folder '{constants.CUTSCENES_FOLDER_NAME}'")
@click.option('-f','--file-path',type=click.Path(exists=True,file_okay=True,dir_okay=True),help="cutscene file/folder path",multiple=True)
@click.option("-d","--dialogue-folder",type=click.Path(exists=True,dir_okay=True,file_okay=False),default=constants.DIALOGUES_FOLDER_NAME,show_default=True)
@click.pass_context
def update_csv(ctx,file_path,dialogue_folder=constants.DIALOGUES_FOLDER_NAME,_all=False):
    string_template = get_template()
    if not file_path and not _all:
        click.echo(f"🤔 Please specify\n -f <FILE_NAME>/<FOLDER_NAME> or use --all")
        return
    if _all:
        for filename in get_filenames(constants.CUTSCENES_FOLDER_NAME,type="_dialogue.txt"):
            __update_csv(filename, string_template, dialogue_folder=dialogue_folder,dry_run=ctx.obj['DRY_RUN'])
            
    else:
        for _file_path in file_path:
            if os.path.isfile(_file_path):
                __update_csv(_file_path, string_template, dialogue_folder=dialogue_folder, dry_run=ctx.obj['DRY_RUN'])
            
            elif os.path.isdir(_file_path):
                for filename in get_filenames(file_path,type="_dialogue.txt"):
                    __update_csv(filename, string_template, dialogue_folder=dialogue_folder,dry_run=ctx.obj['DRY_RUN'])
            
    if ctx.obj['DRY_RUN']:
        click.echo(f"{" (dry run) ":=^55}")
    

if __name__ == "__main__":
    cli(obj={})
    # arg_parser = argparse.ArgumentParser(
    #     description="Create cutscenes dialogues from *.dfs files"
    # )
    # arg_parser.add_argument("--file", dest="dfs_file_path", required=False)
    # arg_parser.add_argument("--folder", dest="dfs_folder_path", required=False)
    # arg_parser.add_argument(
    #     "--dest",
    #     dest="dest_folder",
    #     required=False,
    #     default=constants.CUTSCENES_FOLDER_NAME,
    # )
    # arg_parser.add_argument(
    #     "--dialogue-folder",
    #     dest="dialogue_folder",
    #     required=False,
    #     default=constants.DIALOGUES_FOLDER_NAME,
    # )
    # arg_parser.add_argument("--dry-run", required=False, action="store_true")
    # args = arg_parser.parse_args()

    # if args.dfs_file_path:
    #     create_cutscene_dialogue(
    #         args.dfs_file_path,
    #         args.dest_folder,
    #         dialogue_folder=args.dialogue_folder,
    #         dry_run=args.dry_run,
    #     )

    # elif args.dfs_folder_path:
    #     file_paths = get_filenames(args.dfs_folder_path, type=".dfs")
    #     for file_path in file_paths:
    #         create_cutscene_dialogue(
    #             file_path,
    #             args.dest_folder,
    #             dialogue_folder=args.dialogue_folder,
    #             dry_run=args.dry_run,
    #         )
        
    # if args.dry_run:
    #     print(f"{" (dry run) ":=^55}")
