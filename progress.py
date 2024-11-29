import csv

import constants
from utils.file_util import get_filenames
import click


def get_progress(filename):

    if not filename.endswith(".csv"):
        raise ValueError("File must be a csv file")

    count = 0
    with open(filename, "r", encoding="ISO-8859-1") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        nums = count = 0
        for row in reader:
            nums += 1
            if row["translated_dialogue"] != "":
                count += 1
    try:
        percent = float(count / nums) * 100
    except ZeroDivisionError:
        percent = 100

    result = (filename, count, nums, percent)
    return result


def display(result):
    filename, count, nums, percent = result
    if percent >= 80:
        bg_color = "green"
        emoji = "🦄"
    elif 80 > percent >= 60:
        bg_color = "bright_blue"
        emoji = "🐯"
    elif 60 > percent >= 40:
        bg_color = "yellow"
        emoji = "🐔"
    else:
        bg_color = "red"
        emoji = "🦠"
    click.secho(f"{emoji} ", nl=False)
    click.secho(f"{filename:40s}", nl=False, bg=bg_color)
    click.secho(f"({count}/{nums})".ljust(10), nl=False, bg=bg_color)
    click.secho(f"{percent:.2f} %".rjust(10), nl=False, bg=bg_color)
    click.secho(f" {emoji}")


def __format_table_markdown(results):
    col_num = len(results[0])
    max_chars = [0] * col_num
    for result in results:
        for i in range(col_num):
            max_chars[i] = (
                len(result[i]) if max_chars[i] < len(result[i]) else max_chars[i]
            )

    headers = []
    for t in [" ", "-"]:
        _header = []
        for max_char in max_chars:
            _header.append(t * max_char)
        text = "| " + " | ".join(_header) + " |"
        headers.append(text)

    rows = []
    for result in results:
        cols = []
        for i in range(col_num):
            col = f" {result[i]:<{max_chars[i]}} "
            cols.append(col)
        _cols = "|".join(cols)
        row = "|" + _cols + "|"
        rows.append(row)
    res = headers + rows
    res = "\n".join(res)
    return res


def generate_markdown(results):
    total_nums = len(results)
    done_count = 0
    sum_percent = 0
    row_tables = []
    for result in results:
        filename, count, nums, percent = result
        _percent = int(percent)
        col_1 = f"[{filename}]({filename})"
        col_2 = f"{count}/{nums}"
        col_3 = f"![](https://geps.dev/progress/{_percent})"
        _row_table = (col_1, col_2, col_3)
        row_tables.append(_row_table)

        done_count += 1 if percent == 100 else 0
        sum_percent += percent

    total_percent = float(sum_percent / total_nums)
    _total_percent = int(total_percent)
    markdown = f"**Total**: {done_count}/{total_nums} ![](https://geps.dev/progress/{_total_percent})\n"
    table_markdown = __format_table_markdown(row_tables)
    markdown = markdown + table_markdown
    return markdown


@click.command("update-markdown")
@click.argument(
    "filename", required=False, type=click.Path(exists=True), default="README.md"
)
@click.option(
    "-d",
    "--dialogue-folder",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    default=constants.DIALOGUES_FOLDER_NAME,
    show_default=True,
)
def update_progress_markdown(
    filename: str = "README.md", dialogue_folder: str = constants.DIALOGUES_FOLDER_NAME
):
    """
    Update the translation progress in markdown file.

    FILENAME: file path of markdown file, default is `README.md`

    -d, --dialogue-folder: folder path of dialogue csv files, default is `dialogues/`

    This function will generate markdown table of translation progress from dialogue csv files
    and replace the table in markdown file between `<!--trans-progress-st-->` and `<!--trans-progress-en-->`
    """
    results = _dialogue_progress(dialogue_folder)
    markdown = generate_markdown(results)
    start_marker = "<!--trans-progress-st-->"
    end_marker = "<!--trans-progress-en-->"
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
        _start_index = text.find(start_marker)
        end_index = text.find(end_marker)
        if _start_index == -1 or end_index == -1:
            print(
                f"😑 not found template mark in markdown: '{start_marker}' and '{end_marker}'"
            )
            return
        start_index = _start_index + len(start_marker)

        new_text = text[: start_index + 1] + markdown + "\n" + text[end_index:]

    with open(filename, "w", encoding="utf-8") as write_file:
        write_file.write(new_text)
    print("👍 DONE!: update progress markdown")


def _dialogue_progress(dialogue_folder: str = constants.DIALOGUES_FOLDER_NAME):
    file_paths = get_filenames(dialogue_folder)
    results = [get_progress(file_path) for file_path in file_paths]
    results = sorted(results, key=lambda x: x[0])
    return results


@click.command("display-all")
@click.argument(
    "dialogue_folder",
    required=False,
    type=click.Path(exists=True, file_okay=False),
    default=constants.DIALOGUES_FOLDER_NAME,
)
def display_all_progress(dialogue_folder: str = constants.DIALOGUES_FOLDER_NAME):
    """
    Displays the progress of all translations in the given dialogue folder.

    Args:
        dialogue_folder: The path to the folder containing the dialogue files (.csv), default is `dialogues/`
    """
    results = _dialogue_progress(dialogue_folder)
    for result in results:
        display(result)


@click.command("display")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def display_progress(filename):
    """
    Displays the progress of translation in the given filename.

    Args:
        filename: The path to the dialogue file (.csv)
    """
    result = get_progress(filename)
    display(result)


@click.group()
def cli():
    pass


def main():
    """
    Entry point of this script.

    Updates the progress markdown in the README.md.
    """
    cli.add_command(update_progress_markdown)
    cli.add_command(display_all_progress)
    cli.add_command(display_progress)
    cli()


if __name__ == "__main__":
    main()
