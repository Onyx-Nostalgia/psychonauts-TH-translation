import json
import os
import re

import click

import constants
from utils.file_util import get_filenames


def get_character_ids(file_path):
    with open(file_path, mode="rb") as csvfile:
        dialogue_text = csvfile.read()
        # get id from dialouge raw text csv by regex
        pattern = r"\n[A-Za-z0-9]{4}\d{3}([A-Za-z0-9]{2});"
        character_ids = set(re.findall(pattern, dialogue_text.decode("latin-1")))
    return character_ids


def get_all_character_ids(file_paths):
    all_character_ids = set()
    for file_path in file_paths:
        new_character_ids = get_character_ids(file_path)
        all_character_ids = all_character_ids.union(new_character_ids)
    return all_character_ids


def update_character_json(character_ids, filename=constants.CHARACTER_NAME_FILE_PATH):
    new_character_ids = []

    if not os.path.exists(filename):
        with open(filename, mode="w", encoding="utf-8") as jsonfile:
            json.dump({}, jsonfile, indent=4, ensure_ascii=False)

    with open(filename, mode="r", encoding="utf-8") as jsonfile:
        character_obj = json.load(jsonfile)
        for character_id in character_ids:
            if character_id not in character_obj:
                character_obj[character_id] = {
                    "EN": character_id,
                    "TH": character_id,
                }
                new_character_ids.append(character_id)

    if new_character_ids:
        with open(filename, mode="w", encoding="utf-8") as jsonfile:
            json.dump(character_obj, jsonfile, indent=4, ensure_ascii=False)
        print(f"updated {new_character_ids} to {filename}")
    else:
        print(f"😑 nothing to update {filename}")


def get_character_names(ids=None, filename=constants.CHARACTER_NAME_FILE_PATH):
    with open(filename, mode="r", encoding="utf-8") as jsonfile:
        character_obj = json.load(jsonfile)
        if not ids:
            return character_obj
        return {id: character_obj[id] for id in ids}


def common_options(fn):
    return click.option(
        "-d",
        "--dialogue-folder",
        type=click.Path(exists=True, dir_okay=True, file_okay=False),
        default=constants.DIALOGUES_FOLDER_NAME,
        show_default=True,
    )(
        click.option(
            "-n",
            "--name",
            "filename",
            type=click.Path(exists=True, dir_okay=False, file_okay=True),
            default=constants.CHARACTER_NAME_FILE_PATH,
            show_default=True,
        )(fn)
    )


@click.group()
@click.option("--dry-run", is_flag=True, help="Dry run")
@click.pass_context
def cli(ctx, dry_run):
    dry_run_msg = f"{" (dry run) ":=^55}"
    if dry_run:
        click.echo(dry_run_msg)
    ctx.ensure_object(dict)
    ctx.obj["DRY_RUN"] = dry_run


@cli.command("save")
@common_options
def update_character_name(dialogue_folder, filename):
    file_paths = get_filenames(dialogue_folder)
    all_character_ids = get_all_character_ids(file_paths)
    update_character_json(all_character_ids, filename)


@cli.command("update-dialogue")
@common_options
def update_dialogue_character(dialogue_folder, filename):
    file_paths = get_filenames(dialogue_folder)
    character_names = get_character_names(filename=filename)
    for file_path in file_paths:

        with open(file_path, mode="rb") as csvfile:
            dialogue_text = csvfile.read()
            for character_id, character_name in character_names.items():
                character_row_pattern = ";{};"
                dialogue_text = dialogue_text.replace(
                    character_row_pattern.format(character_id).encode(),
                    character_row_pattern.format(character_name["EN"]).encode(),
                )

        with open(file_path, mode="wb") as csvfile:
            csvfile.write(dialogue_text)


if __name__ == "__main__":
    cli()
