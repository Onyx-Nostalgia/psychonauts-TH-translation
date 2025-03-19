<div align="center">
<img src="https://static.wikia.nocookie.net/psychonauts/images/2/21/Tumblr_m5h0k8g0kQ1qjm1bzo1_500.png/revision/latest?cb=20120822013745"
width="200" 
height="150" />
<h1>🧠 psychonauts-TH-translation 🧠</h1>

<a href="https://github.com/Onyx-Nostalgia/psychonauts-TH-translation/blob/master/README.md">EN</a> |
**TH**

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
</div>

----------------------------

Project สำหรับการแปลเกม Psychonauts เป็น**ภาษาไทย**. โดยจะเก็บรวมรวม file ที่ได้ทำการแปลบทพูดต่าง ๆ เป็น**ภาษาไทย**เอาไว้
 
Code ในการ extraction และ replacement file มีต้นแบบมาจาก [TrupSteam/psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) นำมาพัฒนาต่อเพื่อให้รองรับ python3.X

# 🧠 มีอะไรบ้าง ?
- Extract dialogues จาก file เกม (`.lub` file) ออกมาเป็น csv
- [dialogues/](/dialogues) สำหรับเก็บ file csv บทพูดต่าง ๆ ที่กำลังแปลหรือแปลเสร็จแล้ว
- [cutscenes/](/cutscenes) สำหรับเก็บ file บทพูดตามใน cutscenes เพื่อให้ง่ายต่อการแปล
- ⚠️Develop⚠️ Replace dialogues จาก csv เข้าไปใน file เกม (`.lub` file)
  - ❌💥 **อย่าใช้** ในตอนนี้ เนื่องจาก Font เกมยังไม่รองรับภาษาไทย

# 🪴 Translated Progress
<!--trans-progress-st-->
**Total**: 5/19 ![](https://geps.dev/progress/36)
|                                                                          |          |                                    |
| ------------------------------------------------------------------------ | -------- | ---------------------------------- |
| [dialogues/AS_StringTable.csv](dialogues/AS_StringTable.csv)             | 196/1002 | ![](https://geps.dev/progress/19)  |
| [dialogues/BB_StringTable.csv](dialogues/BB_StringTable.csv)             | 333/333  | ![](https://geps.dev/progress/100) |
| [dialogues/BB_StringTablePC.csv](dialogues/BB_StringTablePC.csv)         | 6/6      | ![](https://geps.dev/progress/100) |
| [dialogues/BV_StringTable.csv](dialogues/BV_StringTable.csv)             | 54/749   | ![](https://geps.dev/progress/7)   |
| [dialogues/CA_StringTable.csv](dialogues/CA_StringTable.csv)             | 624/2542 | ![](https://geps.dev/progress/24)  |
| [dialogues/CA_StringTablePC.csv](dialogues/CA_StringTablePC.csv)         | 0/12     | ![](https://geps.dev/progress/0)   |
| [dialogues/GLOBAL_StringTable.csv](dialogues/GLOBAL_StringTable.csv)     | 478/1426 | ![](https://geps.dev/progress/33)  |
| [dialogues/GLOBAL_StringTablePC.csv](dialogues/GLOBAL_StringTablePC.csv) | 0/114    | ![](https://geps.dev/progress/0)   |
| [dialogues/LL_StringTable.csv](dialogues/LL_StringTable.csv)             | 12/57    | ![](https://geps.dev/progress/21)  |
| [dialogues/LO_StringTable.csv](dialogues/LO_StringTable.csv)             | 51/245   | ![](https://geps.dev/progress/20)  |
| [dialogues/MC_StringTable.csv](dialogues/MC_StringTable.csv)             | 53/188   | ![](https://geps.dev/progress/28)  |
| [dialogues/MI_StringTable.csv](dialogues/MI_StringTable.csv)             | 1/322    | ![](https://geps.dev/progress/0)   |
| [dialogues/MI_StringTablePC.csv](dialogues/MI_StringTablePC.csv)         | 1/1      | ![](https://geps.dev/progress/100) |
| [dialogues/MM_StringTable.csv](dialogues/MM_StringTable.csv)             | 29/707   | ![](https://geps.dev/progress/4)   |
| [dialogues/NI_StringTable.csv](dialogues/NI_StringTable.csv)             | 116/116  | ![](https://geps.dev/progress/100) |
| [dialogues/SA_StringTable.csv](dialogues/SA_StringTable.csv)             | 37/171   | ![](https://geps.dev/progress/21)  |
| [dialogues/SA_StringTablePC.csv](dialogues/SA_StringTablePC.csv)         | 2/2      | ![](https://geps.dev/progress/100) |
| [dialogues/TH_StringTable.csv](dialogues/TH_StringTable.csv)             | 41/803   | ![](https://geps.dev/progress/5)   |
| [dialogues/WW_StringTable.csv](dialogues/WW_StringTable.csv)             | 0/399    | ![](https://geps.dev/progress/0)   |
<!--trans-progress-en-->

# 🧠 ตัวอย่าง dialogues csv file
สามารถไปดูได้ที่ [dialogues/](/dialogues) โดยหลัก ๆ จะมี Column ดังนี้

| id        | character | origin_dialogue      | translated_dialogue       |
| --------- | --------- | -------------------- | ------------------------- |
| CABD001RA | RA        | Dogen! Are you okay? | โดแกน! นายไม่เป็นอะไรใช่ไหม? |

**id**: จะมี 9 ตัวอักษรประกอบไปด้วย 3 UPPER Character + 3 numbers + 2 UPPER Character โดย 2 ตัวอักษรสุดท้ายเป็นตัวย่อของชื่อตัวละครที่พูด

**character**: นำมาจาก 2 ตัวอักษรท้ายของ `id` เป็นเหมือน ต่อย่อชื่อตัวละครหรือจะมองเป็น "character id" ก็ได้ โดยเราจะเก็บชื่อย่อตัวละคร และชื่อเต็มเอาไว้ใน file แยกที่ชื่อ [character_name.json](/character_name.json)

**origin_dialogue**: บทพูดต้นฉบับที่เป็นภาษาอังกฤษ ซึ่งบางบทพูดอาจจะมีอักขระพิเศษผสมอยู่ตด้วย เช่น `\n` 

**translated_dialogue**: Column สำหรับไว้เติมคำแปลภาษาไทยเข้าไป

**Note:** File CSV ใช้ delimeter `;` และ endline `\r\n`

# 🧠 Pre-request
- Install Python 3.X (recommend 3.10+)
  
**Comming Soon !!** 
- Workspace ต่าง ๆ เพื่อให้ง่ายต่อนักพัฒนา
  - Docker
  - Devcontainer

# 🧠 Extract บทพูดจาก File เกม
ตัวเกมจะเก็บ File บทพูดต่าง ๆ ไว้ใน path ประมาณนี้ `Psychonauts/WorkResource/Localization/English/**_StringTable.lub`
ซึ่งสามารถ Extract ออกมาเป็น file CSV ได้โดยใช้คำสั่ง

## Extract บทพูด 1 file
ตัวอย่าง ต้องการ file CSV บทพูดจาก `AS_StringTable.lub`
```bash
python unpack_strings.py --file AS_StringTable.lub
```
จะได้ไฟล์ `dialogues/AS_StringTable.csv`

## Extract ทั้ง Folder
ตัวอย่าง ต้องการ file CSV บทพูดทั้งหมดจาก `Psychonauts/WorkResource/Localization/English`
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English
```
จะได้ไฟล์อยู่ใน `dialogues/`

## Optional
ในบางครั้งหากคุณต้องการจะเปลี่ยน folder ปลายทางที่ต้องการจะเก็บ csv จาก `dialogues/` เป็น folder อื่น สามารถทำได้โดยใส่ flag `--dest` เช่น
```bash
python unpack_strings.py --folder Psychonauts/WorkResource/Localization/English --dest new_dialogues/
``` 
# 🧠 Extract Character Name

คำสั่งในการ extract character จากไฟล์ dialogue CSV มาเก็บไว้ใน [character_name.json](/character_name.json)
```bash
Usage: character.py save [OPTIONS]

Options:
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  -n, --name FILE                 [default: character_name.json]
  --help                          Show this message and exit.
```
ตัวอย่าง
```bash
python character.py save
```
# 🧠 Update Character Name to Dialogue CSV
หากทำการ Update ชื่อเต็ม ใน file [character_name.json](/character_name.json) แล้วต้องการ update ชื่อเต็มลงใน file dialogue CSV สามารถทำได้โดยคำสั่งต่อไปนี้
```bash
Usage: character.py update-dialogue [OPTIONS]

Options:
  -d, --dialogue-folder DIRECTORY
                                  [default: dialogues]
  -n, --name FILE                 [default: character_name.json]
  --help                          Show this message and exit.
```

ตัวอย่าง
```bash
python character.py update-dialogue
```
ตัวอย่างผลลัพธ์

สังเกตุที่ column **character**

**Before**
| id        | character | origin_dialogue | translated_dialogue |
| --------- | --------- | --------------- | ------------------- |
| ASGD027GL | GL        | Oh, no!         | โอ้, ไม่นะ!           |

**After**
| id        | character | origin_dialogue | translated_dialogue |
| --------- | --------- | --------------- | ------------------- |
| ASGD027GL | Gloria    | Oh, no!         | โอ้, ไม่นะ!           |

# 🧠 สร้างไฟล์ Cutscene Dialogue
หลักการสร้าง file cutscene dialogue คือการใช้ ไฟล์ `.dfs` ที่อยู่ใน Folder `psychonauts/WorkResource/cutscenes/prerendered/*.dfs` มาเพื่อค้นหา dialogue ในแต่ละ cutscene และไฟล์ผลลัพธ์จะถูกเก็บอยู่ใน folder `cutscenes` 

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

## Extract จากบาง cutscene
ตัวอย่างการ extract จากบางไฟล์ `.dfs` เช่น ` CABD.dfs` และ ` CABV.dfs`
```
python cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/CABD.dfs /psychonauts/WorkResource/cutscenes/prerendered/CABV.dfs
```
ไฟล์ผลลัพธ์ [cutscenes/CABD_dialogue.txt](/cutscenes/CABD_dialogue.txt) และ [cutscenes/CABD_dialogue.txt](/cutscenes/CABV_dialogue.txt)

## Extarct ทั้ง folder .dfs
```
python cutscene.py generate /psychonauts/WorkResource/cutscenes/prerendered/
```
# 🧠 Update Dialogue CSV จากคำแปลในไฟล์ Cutscene Dialogue
หากเราแปลบทพูดจากในไฟล์ cutscene dialogue ([cutscenes/*_dialogue.txt](/cutscenes/)) เรียบร้อยแล้วและต้องการ update บทพูดที่เราแปลลงไปในไฟล์ dialogue CSV (ไฟล์ที่อยู่ใน folder [dialogues/](/dialogues/))  

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
## Update ทั้งหมด
```bash
python cutscene.py update-csv --all
```

## Update จากบาง cutscene dialogue
ตัวอย่างการ update จาก ไฟล์ `cutscenes/CASA_dialogue.txt` และ `cutscenes/CASB_dialogue.txt`
```bash
python cutscene.py update-csv cutscenes/CASA_dialogue.txt cutscenes/CASB_dialogue.txt
```