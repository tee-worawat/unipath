# 03-filter-by-hand: plain-script copy of the notebook. Run top to bottom; it stops at the first check that fails.
# สำเนาแบบสคริปต์ รันจากบนลงล่าง และหยุดที่การตรวจแรกที่ยังไม่ผ่าน

# %% [markdown]
# # 03 · Filter by hand / กรองข้อมูลด้วยมือ
#
# **Goal:** keep only the records that pass a rule, then combine rules: `and`, "any of these interests", "no restriction", and an honest language rule.
# **เป้าหมาย:** เก็บเฉพาะรายการที่ผ่านกติกา แล้วรวมกติกา: `and` "ตรงความสนใจข้อใดข้อหนึ่ง" "ไม่จำกัด" และกติกาภาษาที่ตรงไปตรงมา
#
# Every rule here becomes part of `find_programmes` in notebook 04.
# ทุกกติกาในสมุดนี้จะกลายเป็นส่วนหนึ่งของ `find_programmes` ในสมุด 04

# %%
# Supplied: load the programme list. / ให้มาแล้ว: โหลดรายการหลักสูตร
import json
from pathlib import Path

PROJECT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "programmes.json").is_file())
programmes = json.loads((PROJECT / "data" / "programmes.json").read_text(encoding="utf-8"))
print("Loaded", len(programmes), "records")

# %% [markdown]
# ## 1. The filter pattern / รูปแบบการกรอง
#
# empty list → loop → `if` → `append`
#
# **Predict:** which programme names will print?
#
# รายการว่าง → ลูป → `if` → `append` **ทำนาย:** จะแสดงชื่อหลักสูตรใดบ้าง

# %%
south_food = []
for programme in programmes:
    if programme["region"] == "south" and "food" in programme["interest_tags"]:
        south_food.append(programme)
for programme in south_food:
    print(programme["programme_en"], "·", programme["province"])

# %% [markdown]
# **Investigate:** change `and` to `or`. Predict how many records you will get, then run it. Change it back afterwards.
#
# **สืบค้น:** เปลี่ยน `and` เป็น `or` ทำนายว่าจะได้กี่รายการ แล้วรัน จากนั้นเปลี่ยนกลับ
#
# ### Exercise 3.1 · Keep whole records / ฝึก 3.1 · เก็บทั้งรายการ
#
# Make `north`, a list of the **whole records** (dictionaries) in the `"north"` region. The website needs every field later, not just the name.
#
# สร้าง `north` เป็นรายการของ **ข้อมูลทั้งรายการ** (ดิกชันนารี) ในภูมิภาค `"north"` เพราะเว็บต้องใช้ทุกฟิลด์ ไม่ใช่แค่ชื่อ

# %%
north = []
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print(len(north), [programme["id"] for programme in north])

# %%
# ✅ Check / ตรวจ
assert len(north) == 4, f"Expected 4 records, got {len(north)} / ควรได้ 4 รายการ"
assert all(isinstance(p, dict) and p["region"] == "north" for p in north), "Append the whole record / เพิ่มทั้งรายการ"
print("OK")

# %% [markdown]
# ### Exercise 3.2 · Two rules at once / ฝึก 3.2 · สองกติกาพร้อมกัน
#
# Keep the `id` of each programme in the `"central"` region **and** tagged `"science"`. Predict the count first.
#
# เก็บ `id` ของหลักสูตรในภูมิภาค `"central"` **และ** มีแท็ก `"science"` ทำนายจำนวนก่อน

# %%
central_science = []
# YOUR CODE HERE / เขียนโค้ดตรงนี้
print(central_science)

# %%
# ✅ Check / ตรวจ
assert central_science == ["muic-computer-science", "muic-food-science", "chula-psychology", "ku-environmental-engineering"], f"Got {central_science}"
print("OK")

# %% [markdown]
# ### Exercise 3.3 · Any of several interests / ฝึก 3.3 · ตรงความสนใจข้อใดข้อหนึ่ง
#
# A learner chooses several interests. Keep a programme if it shares **at least one**. For each programme, build `matched`: the wanted interests found in its tags.
# An empty list counts as `False` in an `if`, so `if matched:` means "at least one matched".
#
# ผู้เรียนเลือกหลายความสนใจ เก็บหลักสูตรที่ตรง **อย่างน้อยหนึ่งข้อ** สำหรับแต่ละหลักสูตรให้สร้าง `matched` คือความสนใจที่พบในแท็ก รายการว่างนับเป็น `False` ใน `if` ดังนั้น `if matched:` แปลว่า "ตรงอย่างน้อยหนึ่งข้อ"

# %%
wanted = ["games", "food"]
any_match = []
for programme in programmes:
    matched = []
    # YOUR CODE HERE / เขียนโค้ดตรงนี้
    if matched:
        any_match.append(programme["id"])
print(any_match)

# %%
# ✅ Check / ตรวจ
assert any_match == ["muic-food-science", "cmu-digital-game", "psu-food-nutrition"], f"Got {any_match}"
print("OK")

# %% [markdown]
# ### Exercise 3.4 · "any" means no restriction / ฝึก 3.4 · "any" คือไม่จำกัด
#
# When a learner does not choose a region, the website sends `"any"`. Write **one** skip rule with `continue` that works for both `"north"` and `"any"`.
# `continue` jumps straight to the next record.
#
# เมื่อผู้เรียนไม่เลือกภูมิภาค เว็บจะส่ง `"any"` เขียนกติกาข้าม **หนึ่ง** ข้อด้วย `continue` ที่ใช้ได้ทั้ง `"north"` และ `"any"` คำสั่ง `continue` ข้ามไปยังรายการถัดไปทันที

# %%
kept_counts = {}
for region in ["north", "any"]:
    kept = []
    for programme in programmes:
        # YOUR CODE HERE / เขียนโค้ดตรงนี้
        kept.append(programme["id"])
    kept_counts[region] = len(kept)
print(kept_counts)

# %%
# ✅ Check / ตรวจ
assert kept_counts == {"north": 4, "any": 16}, f"Got {kept_counts}. Skip only when a region is chosen and differs / ข้ามเฉพาะเมื่อเลือกภูมิภาคแล้วไม่ตรง"
print("OK: we ran the same rule twice by copying a loop. Notebook 04 gives it a name.")

# %% [markdown]
# ### Exercise 3.5 · An honest language rule / ฝึก 3.5 · กติกาภาษาที่ตรงไปตรงมา
#
# | Record says / ข้อมูลระบุ | Learner wants English / ต้องการอังกฤษ |
# |---|---|
# | `"en"` | ✅ confirmed / ยืนยัน |
# | `"th_en"` (bilingual / สองภาษา) | ✅ confirmed under this dataset's policy / ยืนยันตามกติกาชุดข้อมูลนี้ |
# | `"th"` | ❌ skip / ข้าม |
# | `"unknown"` | only if `include_unknown`, and kept **unresolved** / เฉพาะเมื่อเลือกให้รวม และคงสถานะ **ยังไม่ยืนยัน** |
#
# A programme with an "international" format but unknown language is **not** confirmed English.
#
# หลักสูตรรูปแบบ "นานาชาติ" ที่ไม่ทราบภาษา **ไม่ใช่** ภาษาอังกฤษที่ยืนยันแล้ว

# %%
wanted_language = "en"
include_unknown = True
confirmed = []
unresolved = []
for programme in programmes:
    language = programme["teaching_language"]
    # YOUR CODE HERE / เขียนโค้ดตรงนี้
print("Confirmed:", confirmed)
print("Unresolved:", unresolved)

# %%
# ✅ Check / ตรวจ
assert "psu-digital-engineering" not in confirmed, "International format does not prove English / รูปแบบนานาชาติไม่ได้ยืนยันว่าสอนภาษาอังกฤษ"
assert len(confirmed) == 7, f"Expected 7 confirmed (en + bilingual), got {len(confirmed)} / ควรยืนยันได้ 7"
assert len(unresolved) == 4, f"Expected 4 unresolved, got {len(unresolved)} / ควรมี 4 รายการที่ยังไม่ยืนยัน"
print("OK")

# %% [markdown]
# ## 2. Investigate: `break` versus `continue` / สืบค้น: `break` กับ `continue`
#
# **Predict:** what prints? Then swap `break` for `continue` and predict again.
#
# **ทำนาย:** จะแสดงอะไร แล้วลองเปลี่ยน `break` เป็น `continue` และทำนายอีกครั้ง

# %%
first_north = None
for programme in programmes:
    if programme["region"] == "north":
        first_north = programme["programme_en"]
        break
print(first_north)

# %% [markdown]
# `break` stops the whole loop: good for finding one record, wrong for a filter that must check them all.
#
# `break` หยุดลูปทั้งหมด เหมาะกับการหาหนึ่งรายการ แต่ผิดสำหรับการกรองที่ต้องตรวจทุกรายการ
