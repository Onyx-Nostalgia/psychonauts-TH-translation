<div align="center">
<img src="https://static.wikia.nocookie.net/psychonauts/images/2/21/Tumblr_m5h0k8g0kQ1qjm1bzo1_500.png/revision/latest?cb=20120822013745"
width="200" 
height="150" />
<h1>🧠 psychonauts-TH-translation 🧠</h1>

<b>EN</b> |
<a href="https://github.com/Onyx-Nostalgia/psychonauts-TH-translation/blob/master/docs/README-TH.md">TH</a>

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
</div>

----------------------------

It is a translation of the game Psychonauts into **Thai**. It will collect the Dialogues files that have been translated into **Thai**.

The extraction code and replacement code are originally from [TrupSteam/psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) and have been further developed to support python3.X.

# 🧠 What have we here ?
- Extract dialogues from game file (`.lub` file) to csv
- [dialogues/](/dialogues) to store csv file of dialogues that are being translated or have been translated
- [cutscenes/](/cutscenes) to store dialogue files according to cutscenes for easy translation
- ⚠️Develop⚠️ Replace dialogues from csv into game file (`.lub` file)
  - ❌💥 Do not use at this time because the game font does not support Thai language.

# 🪴 Translated Progress
<!--trans-progress-st-->
**Total**: 10/28 ![](https://geps.dev/progress/42)
|                                                                          |          |                                    |
| ------------------------------------------------------------------------ | -------- | ---------------------------------- |
| [dialogues/CA_StringTablePC.csv](dialogues/CA_StringTablePC.csv)         | 0/12     | ![](https://geps.dev/progress/0)   |
| [dialogues/SA_StringTable.csv](dialogues/SA_StringTable.csv)             | 33/171   | ![](https://geps.dev/progress/19)  |
| [dialogues/SA_StringTablePC.csv](dialogues/SA_StringTablePC.csv)         | 2/2      | ![](https://geps.dev/progress/100) |
| [dialogues/LL_StringTablePC.csv](dialogues/LL_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/WW_StringTablePC.csv](dialogues/WW_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/CA_StringTable.csv](dialogues/CA_StringTable.csv)             | 399/2542 | ![](https://geps.dev/progress/15)  |
| [dialogues/MI_StringTablePC.csv](dialogues/MI_StringTablePC.csv)         | 0/1      | ![](https://geps.dev/progress/0)   |
| [dialogues/GLOBAL_StringTable.csv](dialogues/GLOBAL_StringTable.csv)     | 56/1428  | ![](https://geps.dev/progress/3)   |
| [dialogues/LO_StringTablePC.csv](dialogues/LO_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/MM_StringTable.csv](dialogues/MM_StringTable.csv)             | 29/707   | ![](https://geps.dev/progress/4)   |
| [dialogues/LO_StringTable.csv](dialogues/LO_StringTable.csv)             | 51/245   | ![](https://geps.dev/progress/20)  |
| [dialogues/LL_StringTable.csv](dialogues/LL_StringTable.csv)             | 2/57     | ![](https://geps.dev/progress/3)   |
| [dialogues/MM_StringTablePC.csv](dialogues/MM_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/MI_StringTable.csv](dialogues/MI_StringTable.csv)             | 0/322    | ![](https://geps.dev/progress/0)   |
| [dialogues/MC_StringTable.csv](dialogues/MC_StringTable.csv)             | 53/188   | ![](https://geps.dev/progress/28)  |
| [dialogues/WW_StringTable.csv](dialogues/WW_StringTable.csv)             | 0/399    | ![](https://geps.dev/progress/0)   |
| [dialogues/NI_StringTablePC.csv](dialogues/NI_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/BV_StringTable.csv](dialogues/BV_StringTable.csv)             | 56/750   | ![](https://geps.dev/progress/7)   |
| [dialogues/AS_StringTable.csv](dialogues/AS_StringTable.csv)             | 196/1002 | ![](https://geps.dev/progress/19)  |
| [dialogues/AS_StringTablePC.csv](dialogues/AS_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/BB_StringTable.csv](dialogues/BB_StringTable.csv)             | 30/333   | ![](https://geps.dev/progress/9)   |
| [dialogues/NI_StringTable.csv](dialogues/NI_StringTable.csv)             | 58/116   | ![](https://geps.dev/progress/50)  |
| [dialogues/TH_StringTable.csv](dialogues/TH_StringTable.csv)             | 41/803   | ![](https://geps.dev/progress/5)   |
| [dialogues/BV_StringTablePC.csv](dialogues/BV_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/MC_StringTablePC.csv](dialogues/MC_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/TH_StringTablePC.csv](dialogues/TH_StringTablePC.csv)         | 0/0      | ![](https://geps.dev/progress/100) |
| [dialogues/BB_StringTablePC.csv](dialogues/BB_StringTablePC.csv)         | 0/6      | ![](https://geps.dev/progress/0)   |
| [dialogues/GLOBAL_StringTablePC.csv](dialogues/GLOBAL_StringTablePC.csv) | 4/116    | ![](https://geps.dev/progress/3)   |
<!--trans-progress-en-->

# 🧠 Sample Dialogues csv file
see sample in [dialogues/](/dialogues)

| id        | character | origin_dialogue      | translated_dialogue       |
| --------- | --------- | -------------------- | ------------------------- |
| CABD001RA | RA        | Dogen! Are you okay? | โดแกน! นายไม่เป็นอะไรใช่ไหม? |

**id**: There will be 9 characters consisting of 3 UPPER Characters + 3 numbers + 2 UPPER Characters, where the last 2 characters are an abbreviation of the name of the character being spoken.

**character**: It is derived from the last two characters of `id` and is like an abbreviation of the character name or you can view it as a "character id". We will store the character abbreviation and the full name in a separate file named [character_name.json](/character_name.json).

**origin_dialogue**: The original English dialogue, some of which may contain special characters such as `\n`.

**translated_dialogue**: Column for adding Thai translations

**Note:** File CSV use delimeter `;` and endline `\r\n`

# 🧠 Pre-request
- Install Python 3.X (recommend 3.10+)

**Comming Soon !!** 
- Workspace to Easy Development
  - Docker
  - Devcontainer

# 🧠 Extract dialogue from game file
The game will store dialogue files in a path like this `Psychonauts/WorkResource/Localization/English/**_StringTable.lub`
Which can be extracted into a CSV file using the command

## Extract each dialogue file
Example: Need a CSV file of dialogue from `AS_StringTable.lub`
```bash
python unpack_strings.py --file AS_StringTable.lub
```
You will get a file `dialogues/AS_StringTable.csv`

## Extract all file in folder
Example: Need a CSV file of all dialogues from `Psychonauts/WorkResource/Localization/English`
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English
```
The file will be in `dialogues/`

## Optional
Sometimes if you want to change the destination folder where you want to save the csv from `dialogues/` to another folder, you can do it by adding the `--dest` flag, for example:
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English --dest new_dialogues/
```

# 🧠 Extract Character Name

Command to extract character from dialogue CSV file and store in [character_name.json](/character_name.json)
```bash
Usage: character.py save [OPTIONS]

Options:
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  -n, --name FILE                 [default: character_name.json]
  --help                          Show this message and exit.
```
Example
```bash
python character.py save
```
# 🧠 Update Character Name to Dialogue CSV

If you update the full name in the file [character_name.json](/character_name.json) and want to update the full name in the dialogue CSV file, you can do so with the following command.
```bash
Usage: character.py update-dialogue [OPTIONS]

Options:
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  -n, --name FILE                 [default: character_name.json]
  --help                          Show this message and exit.
```

Example
```bash
python character.py update-dialogue
```
Sample result

Notice the column **character**

**Before**
| id        | character | origin_dialogue | translated_dialogue |
| --------- | --------- | --------------- | ------------------- |
| ASGD027GL | GL        | Oh, no!         | โอ้, ไม่นะ!           |

**After**
| id        | character | origin_dialogue | translated_dialogue |
| --------- | --------- | --------------- | ------------------- |
| ASGD027GL | Gloria    | Oh, no!         | โอ้, ไม่นะ!           |

# 🧠 Create Cutscene Dialogue Files
The principle of creating cutscene dialogue file is to use `.dfs` file in Folder `psychonauts/WorkResource/cutscenes/prerendered/*.dfs` to search for dialogue in each cutscene and the result file will be stored in folder `cutscenes`.

```bash
Usage: cutscene.py generate [OPTIONS] [FILE_PATH]...

  Generate cutscene dialogue

  FILE_PATH: .dfs file path or folder path e.g.

   - file path: cutscene.py generate
   /psychonauts/WorkResource/cutscenes/prerendered/CABD.dfs

   - folder path: cutscene.py generate
   /psychonauts/WorkResource/cutscenes/prerendered/

Options:
  -c, --cutscene-folder, --dest-folder DIRECTORY
                                  [default: cutscenes]
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  --help                          Show this message and exit.
```

## Extract from some cutscene
Example of extracting from some `.dfs` files such as `CABD.dfs` and `CABV.dfs`.
```
python cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/CABD.dfs /psychonauts/WorkResource/cutscenes/prerendered/CABV.dfs
```
Result file [cutscenes/CABD_dialogue.txt](/cutscenes/CABD_dialogue.txt) and [cutscenes/CABD_dialogue.txt](/cutscenes/CABV_dialogue.txt)

## Extarct all folder .dfs
```
python cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/
```
# 🧠 Update Dialogue CSV from Cutscene Dialogue
If we have translated the dialogue from the cutscene dialogue file ([cutscenes/*_dialogue.txt](/cutscenes/)) and want to update the translated dialogue into the dialogue CSV file (the file is in the folder [dialogues/](/dialogues/)).

```bash
Usage: cutscene.py update-csv [OPTIONS] [FILE_PATH]...

  Update cutscene to csv dialogue

  FILE_PATH: file path or folder path of cutscene e.g.

   - file path: cutscene.py update-csv cutscenes/CASA_dialogue.txt

   - folder path: cutscene.py update-csv cutscenes

Options:
  --all                           Update all cutscene in folder 'cutscenes'
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  --help                          Show this message and exit.
```
## Update all
```bash
python cutscene.py update-csv --all
```

## Update from some cutscene dialogue
Example of updating from `cutscenes/CASA_dialogue.txt` and `cutscenes/CASB_dialogue.txt`
```bash
python cutscene.py update-csv cutscenes/CASA_dialogue.txt cutscenes/CASB_dialogue.txt
```

