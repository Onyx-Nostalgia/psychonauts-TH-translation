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
    print(f"{filename:40s}", end="")
    print(f"({count}/{nums})".ljust(10), end="")
    print(f"{percent:.2f} %".rjust(10))


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


@click.command()
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
    filename="README.md", dialogue_folder: str = constants.DIALOGUES_FOLDER_NAME
):
    results = _dialogue_progress(dialogue_folder)
    markdown = generate_markdown(results)
    start_marker = "<!--trans-progress-st-->"
    end_marker = "<!--trans-progress-en-->"
    with open(filename, "r") as f:
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

    with open(filename, "w") as write_file:
        write_file.write(new_text)
    print("👍 DONE!: update progress markdown")


def _dialogue_progress(dialogue_folder: str = constants.DIALOGUES_FOLDER_NAME):
    file_paths = get_filenames(dialogue_folder)
    results = [get_progress(file_path) for file_path in file_paths]
    return results


def display_progress():
    results = _dialogue_progress()
    for result in results:
        display(result)


if __name__ == "__main__":
    update_progress_markdown()
