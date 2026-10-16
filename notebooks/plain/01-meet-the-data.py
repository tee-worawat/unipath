# 01-meet-the-data: plain-script copy of the notebook. Run top to bottom; it stops at the first check that fails.
# สำเนาแบบสคริปต์ รันจากบนลงล่าง และหยุดที่การตรวจแรกที่ยังไม่ผ่าน

# %% [markdown]
# # 01 · Meet the data / รู้จักข้อมูล
#
# **Goal:** read one programme record and name the type of every value in it.
# **เป้าหมาย:** อ่านข้อมูลหลักสูตรหนึ่งรายการ และบอกชนิดของค่าทุกตัว
#
# **How to work:** *Predict* first and write it down. Then *Run* the cell (Shift+Enter), *Investigate* why, and *Modify*.
# A cell marked ✅ checks your work. `OK` means move on. An `AssertionError` means read its message, fix the code above, and run both cells again.
#
# **วิธีทำงาน:** ทำนายก่อนและจดไว้ แล้วรันเซลล์ (Shift+Enter) หาเหตุผล แล้วจึงแก้ เซลล์ ✅ ใช้ตรวจงาน ขึ้น `OK` ไปต่อได้ ถ้าขึ้น `AssertionError` ให้อ่านข้อความ แก้โค้ดด้านบน แล้วรันทั้งสองเซลล์อีกครั้ง
#
# The 16 records are real public programmes checked against official pages. They are a sample, not every Thai programme, and nothing here predicts admission.
# ข้อมูล 16 รายการเป็นหลักสูตรจริงที่ตรวจจากหน้าทางการ แต่เป็นเพียงตัวอย่าง ไม่ใช่ทุกหลักสูตรในไทย และไม่ได้ทำนายการรับเข้า

# %%
# Supplied: load the programme list. Run this cell first.
# ให้มาแล้ว: โหลดรายการหลักสูตร รันเซลล์นี้ก่อน
import json
from pathlib import Path

PROJECT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "programmes.json").is_file())
programmes = json.loads((PROJECT / "data" / "programmes.json").read_text(encoding="utf-8"))
print("Loaded", len(programmes), "records")

# %% [markdown]
# ## 1. A list of records / รายการของข้อมูล
#
# **Predict:** what will `type(programmes)` print? Which programme is at position `0`, and which is at `-1`?
#
# **ทำนาย:** `type(programmes)` จะแสดงอะไร หลักสูตรที่ตำแหน่ง `0` และ `-1` คืออะไร

# %%
print(type(programmes))
print(programmes[0]["programme_en"])
print(programmes[-1]["programme_en"])

# %% [markdown]
# One item of the list is one programme. It is a **dictionary**: each *key* (a name in quotes) leads to a *value*.
#
# สมาชิกหนึ่งตัวของรายการคือหลักสูตรหนึ่งหลักสูตร เป็น **ดิกชันนารี** ที่แต่ละ *คีย์* (ชื่อในเครื่องหมายคำพูด) ชี้ไปยัง *ค่า*

# %%
first = programmes[0]
print(type(first))
print(first["university_en"], "·", first["programme_en"])
print(list(first.keys()))

# %% [markdown]
# ## 2. What type is each value? / ค่าแต่ละตัวเป็นชนิดอะไร
#
# **Predict:** before running, write down the type of `province`, `interest_tags`, `tuition_total_thb` and `source_refs` in the first record.
#
# **ทำนาย:** ก่อนรัน จดชนิดของ `province` `interest_tags` `tuition_total_thb` และ `source_refs` ในรายการแรก

# %%
for key, value in first.items():
    print(f"{key:28} {type(value).__name__:9} {value!r}"[:110])

# %% [markdown]
# | Type / ชนิด | Example in our data / ตัวอย่าง | Meaning / ความหมาย |
# |---|---|---|
# | `str` | `"Chiang Mai"` | text / ข้อความ |
# | `int` | `2569` | whole number / จำนวนเต็ม |
# | `list` | `["technology", "data"]` | several values in order / หลายค่าเรียงกัน |
# | `dict` | `{"programme": "muic-cs", ...}` | named values, key → value / ค่าที่มีชื่อ |
# | `NoneType` | `None` | not supplied or unknown, **not** `0` and **not** `""` / ไม่มีข้อมูล ไม่ใช่ 0 และไม่ใช่ข้อความว่าง |
#
# A list can sit inside a dictionary: `first["interest_tags"][0]` means "the tags of the first record, then the first tag".
#
# รายการซ้อนในดิกชันนารีได้ `first["interest_tags"][0]` คือ "แท็กของรายการแรก แล้วเอาแท็กแรก"

# %% [markdown]
# ### Exercise 1.1 · Reach inside / ฝึก 1.1 · เข้าถึงข้างใน
#
# `programmes[5]` is Digital Game at Chiang Mai University. Set the three variables by indexing `game`; do not type the answers yourself.
#
# `programmes[5]` คือ Digital Game มหาวิทยาลัยเชียงใหม่ กำหนดตัวแปรทั้งสามด้วยการเข้าถึง `game` ห้ามพิมพ์คำตอบเอง

# %%
game = programmes[5]
# YOUR CODE HERE / เขียนโค้ดตรงนี้
game_province = None
game_tags = None
game_first_tag = None
print(game_province, game_tags, game_first_tag)

# %%
# ✅ Check / ตรวจ
assert game_province == "Chiang Mai", "Use game[...] with the province key / ใช้คีย์ของจังหวัด"
assert game_tags == ["games", "technology", "design"], "interest_tags is a list inside the dictionary / interest_tags เป็นรายการในดิกชันนารี"
assert game_first_tag == "games", "Index the list too; the first position is 0 / เข้าถึงรายการต่อ ตำแหน่งแรกคือ 0"
print("OK")

# %% [markdown]
# ### Exercise 1.2 · Same key, different type / ฝึก 1.2 · คีย์เดียวกัน ชนิดต่างกัน
#
# `programmes[13]` is Communication Arts at Chulalongkorn University. **Predict** the type name of each value and write it in `my_types`, then run the check. If a guess is wrong, find out why before fixing it.
#
# `programmes[13]` คือนิเทศศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย **ทำนาย** ชื่อชนิดของแต่ละค่าแล้วเขียนใน `my_types` จากนั้นรันการตรวจ ถ้าทายผิดให้หาเหตุผลก่อนแก้

# %%
chula = programmes[13]
# YOUR CODE HERE / เขียนโค้ดตรงนี้
my_types = {"province": "?", "admission_reference_year_be": "?", "tuition_total_thb": "?", "data_notes": "?"}

# %%
# ✅ Check / ตรวจ
for key, guess in my_types.items():
    actual = type(chula[key]).__name__
    assert guess == actual, f"{key}: you wrote {guess!r}, Python says {actual!r} / คุณเขียน {guess!r} แต่ Python บอก {actual!r}"
print("OK: in the first record admission_reference_year_be was None; here it is an int.")

# %% [markdown]
# ## 3. Numbers, text and unknown / ตัวเลข ข้อความ และค่าที่ไม่ทราบ
#
# **Predict:** which of these lines work and which fail?
#
# **ทำนาย:** บรรทัดใดทำงานได้ และบรรทัดใดผิดพลาด

# %%
for expression in ['2569 - 543', '"2569" - 543', 'None - 543']:
    try:
        print(expression, "→", eval(expression))
    except TypeError as error:
        print(expression, "→ TypeError:", error)

# %% [markdown]
# Two kinds of "unknown" appear in this dataset:
# - `None` means a value was not supplied, for example `tuition_total_thb`. Never show it as `0` baht.
# - The text `"unknown"` is a deliberate label from a fixed list, for example `teaching_language`. It is never the same as English.
#
# ข้อมูลนี้มี "ไม่ทราบ" สองแบบ `None` คือไม่มีข้อมูล เช่น `tuition_total_thb` ห้ามแสดงเป็น 0 บาท ส่วนข้อความ `"unknown"` เป็นป้ายจากรายการที่กำหนด เช่น `teaching_language` และไม่เท่ากับภาษาอังกฤษ

# %% [markdown]
# ### Exercise 1.3 · Convert the year / ฝึก 1.3 · แปลงปี
#
# Read Chulalongkorn's reference year (Buddhist Era) from the record, then convert it: CE = BE − 543.
#
# อ่านปีอ้างอิง (พ.ศ.) ของจุฬาฯ จากข้อมูล แล้วแปลงเป็น ค.ศ. = พ.ศ. − 543

# %%
# YOUR CODE HERE / เขียนโค้ดตรงนี้
year_be = None
year_ce = None
print(year_be, "BE =", year_ce, "CE")

# %%
# ✅ Check / ตรวจ
assert year_be == 2569, "Read the value from chula[...] / อ่านค่าจาก chula[...]"
assert year_ce == 2026, "Subtract 543 from year_be / ลบ 543 จาก year_be"
print("OK")

# %% [markdown]
# ### Exercise 1.4 · Say "unknown" honestly / ฝึก 1.4 · บอกว่าไม่ทราบอย่างตรงไปตรงมา
#
# Set `fee_text` for the first record. If the fee is `None`, say it is not supplied; otherwise show the amount. Use `is None`.
#
# กำหนด `fee_text` ของรายการแรก ถ้าค่าเรียนเป็น `None` ให้บอกว่าไม่มีข้อมูล ถ้าไม่ใช่ให้แสดงจำนวน ใช้ `is None`

# %%
first_fee = first["tuition_total_thb"]
# YOUR CODE HERE / เขียนโค้ดตรงนี้
fee_text = ""
print(fee_text)

# %%
# ✅ Check / ตรวจ
assert "not supplied" in fee_text, 'For None, include the words "not supplied" / เมื่อเป็น None ให้มีคำว่า "not supplied"'
assert "0" not in fee_text and "None" not in fee_text, "Do not show None as 0 or as the word None / ห้ามแสดงเป็น 0 หรือคำว่า None"
print("OK")

# %% [markdown]
# ## 4. Modify / ปรับแก้
#
# Choose any record number from 0 to 15. Change `pick`, predict the sentence, then run. Add one more field to the sentence.
#
# เลือกหมายเลข 0 ถึง 15 เปลี่ยน `pick` ทำนายประโยค แล้วรัน จากนั้นเพิ่มฟิลด์อีกหนึ่งตัวในประโยค

# %%
pick = 0
record = programmes[pick]
print(f"{record['programme_en']} at {record['university_en']} ({record['province']}): {', '.join(record['interest_tags'])}")
