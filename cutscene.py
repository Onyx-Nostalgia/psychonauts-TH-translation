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
        with open(filename, mode="rb") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id in dialogue_ids:
            if dialogue_id in dialogue_stack:
                continue
            start_index = csv_text.find(dialogue_id.encode())
            end_index = csv_text.find(b"\n", start_index)
            if start_index != -1 and end_index != -1:
                dialogue = csv_text[start_index:end_index]
                dialogue_stack[dialogue_id] = dialogue.split(b";")
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                return dialogue_stack

    # case id in .dfs not found in any dialogues
    difference_dialogues = set(dialogue_ids) - set(dialogue_stack.keys())
    print("   🤔 {} dialogue not found.".format(", ".join(difference_dialogues)))
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
    pattern = re.sub(
        r"\\\{([a-zA-Z0-9]{2,4})_Character\\\}", r"(?P<\1_Character>.[^:]*)", pattern
    )
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
    language_types = list(map(str.upper, character_names[character_id].keys()))
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
        en_dialogue = dialogues[dialogue_id][2].decode("latin-1")
        th_dialogue = dialogues[dialogue_id][3].decode()
    if exist_cutscene_dialogues:
        exist_cutscene_dialogue = exist_cutscene_dialogues[dialogue_id]
        th_dialogue = th_dialogue or exist_cutscene_dialogue["TH_Dialogue"]
    return {"EN_Dialogue": en_dialogue, "TH_Dialogue": th_dialogue}


def generate_dest_file_path(file_path, dest_folder):
    filename = file_path.split("/")[-1]
    if filename.endswith(".dfs"):
        filename = filename[:-4] + "_dialogue.txt"
        dest_file_path = os.path.join(dest_folder, filename)
    return dest_file_path


def __create_cutscene_dialogue(
    file_path,
    dest_folder=constants.CUTSCENES_FOLDER_NAME,
    dialogue_folder=constants.DIALOGUES_FOLDER_NAME,
    dry_run=False,
):
    dest_file_path = generate_dest_file_path(file_path, dest_folder)
    string_template = get_template()
    dfs_rows = read_dfs(file_path)
    dialogue_ids = [_id for _id, _ in dfs_rows]
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
            dfs=dfs, **character_cutscene, **dialogue_cutscene
        )
        result.append(text)

    if not dry_run:
        with open(dest_file_path, mode="w") as f:
            text = "".join(result)
            f.write(text)
    print("✅ Created/Updated {}".format(dest_file_path))


def write_csv_dialogue(csv_text, filename, dry_run=False):
    if not filename.endswith(".csv"):
        click.echo(f"🤔 {filename} is not a csv file.")
        return
    if not dry_run:
        with open(filename, mode="wb") as csvfile:
            csvfile.write(csv_text)
    click.echo(f"✅ Updated {filename}")


def __update_th_dialogue(dialogue_id, csv_text, cutscene_dialogue):
    start_index = csv_text.find(dialogue_id.encode())
    end_index = csv_text.find("\n".encode(), start_index)
    if start_index != -1 and end_index != -1:
        th_start_index = csv_text.rfind(";".encode(), start_index, end_index)

        # replace th dialogue from cutscene_dialogue to dialogue csv
        th_dialogue = cutscene_dialogue["TH_Dialogue"]
        if th_dialogue:
            csv_text = (
                csv_text[: th_start_index + 1]
                + th_dialogue.encode()
                + csv_text[end_index:]
            )
        rows = csv_text[start_index : th_start_index + 1] + th_dialogue.encode()
        return csv_text, rows
    return csv_text, None


def __update_csv(
    file_path,
    string_template,
    dialogue_folder=constants.DIALOGUES_FOLDER_NAME,
    dry_run=False,
):
    """
    Output: {dialogue_id: dialogue_id;character_id;origin_dialogue;translated_dialogue;}
    """
    cutscene_dialogues = extract_cutscene_dialogue(file_path, string_template)
    dialogue_ids = cutscene_dialogues.keys()
    dialogue_stack = {}
    filenames = get_filenames(dialogue_folder)
    for filename in filenames:
        is_found = False
        with open(filename, mode="rb") as csvfile:
            csv_text = csvfile.read()
        for dialogue_id, cutscene_dialogue in cutscene_dialogues.items():
            if dialogue_id in dialogue_stack:
                continue
            csv_text, _th_dialogue = __update_th_dialogue(
                dialogue_id, csv_text, cutscene_dialogue
            )
            if _th_dialogue:
                is_found = True
                dialogue_stack[dialogue_id] = _th_dialogue
            if set(dialogue_stack.keys()) == set(dialogue_ids):
                write_csv_dialogue(csv_text, filename, dry_run=dry_run)
                return dialogue_stack
        if is_found:
            write_csv_dialogue(csv_text, filename, dry_run=dry_run)

    # case id in cutscene not found in any dialogues
    difference_dialogues = set(dialogue_ids) - set(dialogue_stack.keys())
    print("   🤔 {} dialogue not found.".format(", ".join(difference_dialogues)))
    return dialogue_stack


@click.group()
@click.option("--dry-run/--no-dry-run", default=False, help="Dry run")
@click.pass_context
def cli(ctx, dry_run):
    dry_run_msg = f"{" (dry run) ":=^55}"
    if dry_run:
        click.echo(dry_run_msg)
    ctx.ensure_object(dict)
    ctx.obj["DRY_RUN"] = dry_run


@cli.command(
    context_settings={"ignore_unknown_options": True},
    name="generate",
    short_help="Generate cutscene dialogue",
)
@click.argument("file-path", type=click.Path(exists=True), nargs=-1)
@click.option(
    "-c",
    "--cutscene-folder",
    "--dest-folder",
    type=click.Path(exists=True, file_okay=False),
    default=constants.CUTSCENES_FOLDER_NAME,
    show_default=True,
)
@click.option(
    "-d",
    "--dialogue-folder",
    type=click.Path(exists=True, file_okay=False),
    default=constants.DIALOGUES_FOLDER_NAME,
    show_default=True,
)
@click.pass_context
def generate_cutscene(ctx, file_path, cutscene_folder, dialogue_folder):
    """Generate cutscene dialogue

    FILE_PATH: .dfs file path or folder path e.g.\n
     - file path: cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/CABD.dfs\n
     - folder path: cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/
    """
    for _file_path in file_path:
        if os.path.isfile(_file_path):
            __create_cutscene_dialogue(
                file_path=_file_path,
                dest_folder=cutscene_folder,
                dialogue_folder=dialogue_folder,
                dry_run=ctx.obj["DRY_RUN"],
            )

        elif os.path.isdir(_file_path):
            for filename in get_filenames(_file_path, type=".dfs"):
                __create_cutscene_dialogue(
                    file_path=filename,
                    dest_folder=cutscene_folder,
                    dialogue_folder=dialogue_folder,
                    dry_run=ctx.obj["DRY_RUN"],
                )


@cli.command(
    context_settings={"ignore_unknown_options": True},
    short_help="Update cutscene to csv dialogue",
)
@click.argument("file-path", required=False, type=click.Path(exists=True), nargs=-1)
@click.option(
    "--all",
    "_all",
    is_flag=True,
    help=f"Update all cutscene in folder '{constants.CUTSCENES_FOLDER_NAME}'",
)
@click.option(
    "-d",
    "--dialogue-folder",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    default=constants.DIALOGUES_FOLDER_NAME,
    show_default=True,
)
@click.pass_context
def update_csv(ctx, file_path, dialogue_folder, _all):
    """Update cutscene to csv dialogue

    FILE_PATH: file path or folder path of cutscene e.g.\n
     - file path: cutscene.py update-csv cutscenes/CASA_dialogue.txt cutscenes/CABA_dialogue.txt\n
     - folder path: cutscene.py update-csv cutscenes
    """
    string_template = get_template()
    if not file_path and not _all:
        raise click.UsageError("🤔 Please specify: FILE_PATH / --all")
    if _all:
        for filename in get_filenames(
            constants.CUTSCENES_FOLDER_NAME, type="_dialogue.txt"
        ):
            __update_csv(
                filename,
                string_template,
                dialogue_folder=dialogue_folder,
                dry_run=ctx.obj["DRY_RUN"],
            )
            return

    for _file_path in file_path:
        if os.path.isfile(_file_path):
            __update_csv(
                _file_path,
                string_template,
                dialogue_folder=dialogue_folder,
                dry_run=ctx.obj["DRY_RUN"],
            )

        elif os.path.isdir(_file_path):
            for filename in get_filenames(_file_path, type="_dialogue.txt"):
                __update_csv(
                    filename,
                    string_template,
                    dialogue_folder=dialogue_folder,
                    dry_run=ctx.obj["DRY_RUN"],
                )


if __name__ == "__main__":
    cli()
