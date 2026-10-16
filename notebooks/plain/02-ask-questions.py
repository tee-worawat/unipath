# 02-ask-questions: plain-script copy of the notebook. Run top to bottom; it stops at the first check that fails.
# สำเนาแบบสคริปต์ รันจากบนลงล่าง และหยุดที่การตรวจแรกที่ยังไม่ผ่าน

# %% [markdown]
# # 02 · Ask the data questions / ตั้งคำถามกับข้อมูล
#
# **Goal:** answer questions about all 16 records with a loop, `in`, a counter and a tally dictionary.
# **เป้าหมาย:** ตอบคำถามเกี่ยวกับข้อมูลทั้ง 16 รายการด้วยลูป `in` ตัวนับ และดิกชันนารีนับจำนวน
#
# Predict → Run → Investigate → Modify. ✅ cells check your work.
# ทำนาย → รัน → สืบค้น → ปรับแก้ เซลล์ ✅ ใช้ตรวจงาน

# %%
# Supplied: load the programme list. / ให้มาแล้ว: โหลดรายการหลักสูตร
import json
from pathlib import Path

PROJECT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "programmes.json").is_file())
programmes = json.loads((PROJECT / "data" / "programmes.json").read_text(encoding="utf-8"))
print("Loaded", len(programmes), "records")

# %% [markdown]
# ## 1. Visit every record / ไปทีละรายการ
#
# **Predict:** how many lines will this print, and which region comes first?
#
# **ทำนาย:** จะแสดงกี่บรรทัด และภูมิภาคใดขึ้นก่อน

# %%
for programme in programmes:
    print(programme["region"], "·", programme["programme_en"])

# %% [markdown]
# ## 2. `in` asks "is it inside?" / `in` ถามว่า "อยู่ข้างในไหม"
#
# **Predict** `True` or `False` for each line before running. One line is a trap.
#
# **ทำนาย** `True` หรือ `False` ของแต่ละบรรทัดก่อนรัน มีหนึ่งบรรทัดเป็นกับดัก

# %%
game = programmes[5]
print("games" in game["interest_tags"])
print("food" in game["interest_tags"])
print("games" in game)
print("region" in game)

# %% [markdown]
# `in` on a **list** looks at the values. `in` on a **dictionary** looks only at the **keys**, so `"games" in game` is `False`.
#
# `in` กับ **รายการ** ดูที่ค่า แต่ `in` กับ **ดิกชันนารี** ดูเฉพาะ **คีย์** จึงได้ `"games" in game` เป็น `False`

# %% [markdown]
# ### Exercise 2.1 · Count / ฝึก 2.1 · นับ
#
# How many programmes are in the `"north"` region? Start the counter at 0 and add 1 inside an `if`.
#
# มีหลักสูตรใน `"north"` กี่รายการ เริ่มตัวนับที่ 0 แล้วบวก 1 ใน `if`

# %%
count_north = 0
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print(count_north)

# %%
# ✅ Check / ตรวจ
assert count_north == 4, f"Expected 4, got {count_north}. Is the + 1 inside the if? / บวก 1 อยู่ใน if หรือไม่"
print("OK")

# %% [markdown]
# ### Exercise 2.2 · Collect / ฝึก 2.2 · เก็บรวบรวม
#
# Make a list of the English names of every programme tagged `"data"`. Start with an empty list and use `.append(...)`.
#
# สร้างรายการชื่อภาษาอังกฤษของทุกหลักสูตรที่มีแท็ก `"data"` เริ่มจากรายการว่างแล้วใช้ `.append(...)`

# %%
data_names = []
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print(data_names)

# %%
# ✅ Check / ตรวจ
assert len(data_names) == 6, f"Expected 6 names, got {len(data_names)} / ควรได้ 6 ชื่อ"
assert all(isinstance(name, str) for name in data_names), "Append the name (a str), not the whole record / เพิ่มชื่อ ไม่ใช่ทั้งรายการ"
assert "Finance" in data_names and "Computer Science" in data_names
print("OK")

# %% [markdown]
# ### Exercise 2.3 · Tally by region / ฝึก 2.3 · นับแยกตามภูมิภาค
#
# A **tally dictionary** keeps one counter per key. The first time a region appears it is not a key yet, so start it at 0 before adding 1.
# **Predict** the three numbers before you write the code.
#
# **ดิกชันนารีนับจำนวน** มีตัวนับหนึ่งตัวต่อหนึ่งคีย์ ครั้งแรกที่พบภูมิภาคยังไม่มีคีย์นั้น จึงต้องเริ่มที่ 0 ก่อนบวก 1 **ทำนาย** ตัวเลขทั้งสามก่อนเขียนโค้ด

# %%
region_counts = {}
for programme in programmes:
    region = programme["region"]
    # YOUR CODE HERE / เขียนโค้ดตรงนี้
print(region_counts)

# %%
# ✅ Check / ตรวจ
assert region_counts == {"central": 7, "north": 4, "south": 5}, f"Got {region_counts}. A KeyError means the first count was not started at 0 / KeyError แปลว่ายังไม่ได้เริ่มที่ 0"
print("OK")

# %% [markdown]
# ### Exercise 2.4 · Tally the tags (a loop inside a loop) / ฝึก 2.4 · นับแท็ก (ลูปซ้อนลูป)
#
# Each record has several tags, so loop over the records and then over `interest_tags`. Shortcut: `counts.get(key, 0)` gives 0 when the key is missing.
#
# แต่ละรายการมีหลายแท็ก จึงวนรายการแล้ววน `interest_tags` ข้างใน ทางลัด: `counts.get(key, 0)` ให้ 0 เมื่อยังไม่มีคีย์

# %%
tag_counts = {}
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print(tag_counts)

# %%
# ✅ Check / ตรวจ
total_tags = sum(len(programme["interest_tags"]) for programme in programmes)
assert sum(tag_counts.values()) == total_tags, f"Every tag should be counted once: {total_tags} in total / นับทุกแท็กครั้งเดียว รวม {total_tags}"
assert tag_counts.get("technology") == 9 and tag_counts.get("games") == 1
print("OK")

# %% [markdown]
# ### Exercise 2.5 · Count what we do not know / ฝึก 2.5 · นับสิ่งที่ไม่รู้
#
# Count records whose `teaching_language` is the label `"unknown"`, and records whose `tuition_total_thb` is `None`.
#
# นับรายการที่ `teaching_language` เป็นป้าย `"unknown"` และรายการที่ `tuition_total_thb` เป็น `None`

# %%
unknown_language = 0
no_fee = 0
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print("unknown language:", unknown_language, "| no fee supplied:", no_fee)

# %%
# ✅ Check / ตรวจ
assert unknown_language == 4, f"Expected 4, got {unknown_language} / ควรได้ 4"
assert no_fee == 16, "Use `is None` for the fee / ใช้ `is None` กับค่าเรียน"
print("OK")

# %% [markdown]
# **Discuss:** what should a website show for these records? Never "English" for an unknown language, and never "0 baht" for a missing fee.
#
# **อภิปราย:** เว็บไซต์ควรแสดงอะไรกับรายการเหล่านี้ ห้ามแสดงว่า "อังกฤษ" เมื่อไม่ทราบภาษา และห้ามแสดง "0 บาท" เมื่อไม่มีข้อมูลค่าเรียน
#
# ## 3. Modify: your own question / ปรับแก้: คำถามของเรา
#
# Write one question about the data (for example: which province appears most? how many programmes are Thai-language?). Predict the answer, then write the code.
#
# ตั้งคำถามหนึ่งข้อ (เช่น จังหวัดใดมีมากที่สุด หลักสูตรภาษาไทยมีกี่รายการ) ทำนายคำตอบ แล้วเขียนโค้ด

# %%
# My question / คำถามของฉัน:
# My prediction / คำทำนาย:
