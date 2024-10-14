<center>
<img src="https://static.wikia.nocookie.net/psychonauts/images/2/21/Tumblr_m5h0k8g0kQ1qjm1bzo1_500.png/revision/latest?cb=20120822013745"
width="200" 
height="150" />
<h1>🧠 psychonauts-TH-translation 🧠</h1>

<a href="https://github.com/Onyx-Nostalgia/psychonauts-TH-translation/blob/master/README.md">EN</a> |
**TH**

<img src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
</center>

----------------------------

Project สำหรับการแปลเกม Psychonauts เป็น**ภาษาไทย**. โดยจะเก็บรวมรวม file ที่ได้ทำการแปลบทพูดต่าง ๆ เป็น**ภาษาไทย**เอาไว้
 
Code ในการ extraction และ replacement file มีต้นแบบมาจาก [TrupSteam/psychonauts-translator](https://github.com/TrupSteam/psychonauts-translator) นำมาพัฒนาต่อเพื่อให้รองรับ python3.X

# 🧠 มีอะไรบ้าง ?
- Extract dialogues จาก file เกม (`.lub` file) ออกมาเป็น csv
- [dialogues/](/dialogues) สำหรับเก็บ file csv บทพูดต่าง ๆ ที่กำลังแปลหรือแปลเสร็จแล้ว
- [cutscenes/](/cutscenes) สำหรับเก็บ file บทพูดตามใน cutscenes เพื่อให้ง่ายต่อการแปล
- ⚠️Develop⚠️ Replace dialogues จาก csv เข้าไปใน file เกม (`.lub` file)
  - ❌💥 **อย่าใช้** ในตอนนี้ เนื่องจาก Font เกมยังไม่รองรับภาษาไทย

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