# 04-name-it-functions: plain-script copy of the notebook. Run top to bottom; it stops at the first check that fails.
# สำเนาแบบสคริปต์ รันจากบนลงล่าง และหยุดที่การตรวจแรกที่ยังไม่ผ่าน

# %% [markdown]
# # 04 · Name it: from loops to functions / ตั้งชื่อ: จากลูปสู่ฟังก์ชัน
#
# **Goal:** turn the rules from notebook 03 into functions with parameters, default values and a `return`. These are the same two functions the website will call: `shared_interests` and `find_programmes`.
# **เป้าหมาย:** เปลี่ยนกติกาจากสมุด 03 เป็นฟังก์ชันที่มีพารามิเตอร์ ค่าเริ่มต้น และ `return` ซึ่งเป็นสองฟังก์ชันเดียวกับที่เว็บไซต์จะเรียกใช้

# %%
# Supplied: load the programme list and the language helper. / ให้มาแล้ว: โหลดข้อมูลและตัวช่วยภาษา
import json
import sys
from pathlib import Path

PROJECT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "programmes.json").is_file())
programmes = json.loads((PROJECT / "data" / "programmes.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(PROJECT))
from language_policy import language_matches
print("Loaded", len(programmes), "records and language_matches")

# %% [markdown]
# ## 1. Why functions? / ทำไมต้องฟังก์ชัน
#
# In 03 you copied a loop to test `"north"` and then `"any"`. A function gives a rule a **name**, takes **parameters** (inputs) and **returns** a result. Write it once, call it many times.
# **Predict** the three results.
#
# ใน 03 เราคัดลอกลูปเพื่อทดสอบ `"north"` และ `"any"` ฟังก์ชันตั้ง **ชื่อ** ให้กติกา รับ **พารามิเตอร์** และ **คืนค่า** ผลลัพธ์ เขียนครั้งเดียวเรียกใช้ได้หลายครั้ง **ทำนาย** ผลทั้งสาม

# %%
def region_matches(programme, region):
    return region == "any" or programme["region"] == region


game = programmes[5]
print(region_matches(game, "north"))
print(region_matches(game, "south"))
print(region_matches(game, "any"))

# %% [markdown]
# ## 2. `print` is not `return` / `print` ไม่ใช่ `return`
#
# **Predict:** what is stored in `answer`?
#
# **ทำนาย:** ค่าใดถูกเก็บใน `answer`

# %%
def shout_region(programme):
    print(programme["region"].upper())


answer = shout_region(game)
print("answer is", answer)

# %% [markdown]
# `print` only shows text. Without `return`, a function gives back `None`, so code that calls it gets nothing to use.
#
# `print` แค่แสดงข้อความ ถ้าไม่มี `return` ฟังก์ชันจะคืน `None` โค้ดที่เรียกจึงไม่ได้ค่าไปใช้
#
# ### Exercise 4.1 · Your first function / ฝึก 4.1 · ฟังก์ชันแรก
#
# Write `count_in_region(programmes, region)`. It **returns** how many records pass `region_matches`. This is Exercise 2.1, with the region as a parameter.
#
# เขียน `count_in_region(programmes, region)` ที่ **คืนค่า** จำนวนรายการที่ผ่าน `region_matches` คือฝึก 2.1 แต่ภูมิภาคเป็นพารามิเตอร์

# %%
def count_in_region(programmes, region):
    count = 0
    # YOUR CODE HERE / เขียนโค้ดตรงนี้
    return count


print(count_in_region(programmes, "south"))

# %%
# ✅ Check / ตรวจ
assert count_in_region(programmes, "north") == 4
assert count_in_region(programmes, "south") == 5
assert count_in_region(programmes, "any") == 16, '"any" means every record / "any" คือทุกรายการ'
assert count_in_region([], "north") == 0, "An empty list has no records / รายการว่างไม่มีข้อมูล"
print("OK: one function, four questions.")

# %% [markdown]
# ### Exercise 4.2 · `shared_interests` / ฝึก 4.2 · `shared_interests`
#
# Return the wanted interests that appear in `programme["interest_tags"]`, **without duplicates** and in the order the learner chose them. This is the inner loop from Exercise 3.3.
#
# คืนค่าความสนใจที่ต้องการซึ่งอยู่ใน `programme["interest_tags"]` **ไม่ซ้ำกัน** และเรียงตามลำดับที่ผู้เรียนเลือก คือลูปข้างในจากฝึก 3.3

# %%
def shared_interests(wanted, programme):
    matches = []
    # YOUR CODE HERE / เขียนโค้ดตรงนี้
    return matches


print(shared_interests(["games", "food", "design"], game))

# %%
# ✅ Check / ตรวจ
assert shared_interests(["games", "design"], game) == ["games", "design"]
assert shared_interests(["design", "food", "design"], {"interest_tags": ["design"]}) == ["design"], "No duplicates / ห้ามซ้ำ"
assert shared_interests([], game) == [], "Nothing wanted, nothing shared / ไม่เลือกก็ไม่มีที่ตรง"
print("OK")

# %% [markdown]
# ### Exercise 4.3 · `find_programmes` / ฝึก 4.3 · `find_programmes`
#
# Put every rule together. The first line is identical to `finder.py`, so you can paste it into the project in notebook 05.
#
# 1. Skip a record whose region does not match. `"any"` means no restriction (Exercise 3.4).
# 2. Skip a record that fails the supplied `language_matches(programme, language, include_unknown)`. It already applies the table from Exercise 3.5.
# 3. Use `shared_interests`. If interests were chosen and none match, skip the record. If none were chosen, do not restrict.
# 4. Append `{"programme": programme, "matched_interests": matches}`; the website's search.py reads these two keys.
#
# รวมทุกกติกา บรรทัดแรกเหมือน `finder.py` จึงนำไปวางในโครงงานได้ในสมุด 05: (1) ข้ามเมื่อภูมิภาคไม่ตรง โดย `"any"` คือไม่จำกัด (2) ข้ามเมื่อไม่ผ่าน `language_matches` ที่ให้มา (3) ใช้ `shared_interests` ถ้าเลือกความสนใจแต่ไม่ตรงเลยให้ข้าม ถ้าไม่เลือกไม่จำกัด (4) เพิ่มดิกชันนารีสองคีย์นี้ที่ search.py ของเว็บไซต์ใช้

# %%
def find_programmes(programmes, wanted, region="any", language="any", include_unknown=True):
    results = []
    for programme in programmes:
        # YOUR CODE HERE / เขียนโค้ดตรงนี้
        pass
    return results


for result in find_programmes(programmes, ["technology", "design"], "north"):
    print(result["programme"]["programme_en"], result["matched_interests"])

# %%
# ✅ Check / ตรวจ: the same behaviours the project tests will check / พฤติกรรมเดียวกับที่การตรวจของโครงงานใช้
def ids(results):
    return {result["programme"]["id"] for result in results}


assert len(find_programmes(programmes, [])) == 16, "No interests and no filters keeps every record / ไม่เลือกอะไรต้องได้ทุกรายการ"
assert ids(find_programmes(programmes, ["games"], "north")) == {"cmu-digital-game"}
assert find_programmes(programmes, ["games"], "north")[0]["matched_interests"] == ["games"], "Append both keys / เพิ่มทั้งสองคีย์"
assert find_programmes(programmes, [], "south", "en", False) == [], "Unknown language must not count as English / ภาษาไม่ทราบต้องไม่นับเป็นอังกฤษ"
assert ids(find_programmes(programmes, [], "south", "en", True)) == {"psu-digital-engineering", "psu-digital-business"}
assert find_programmes(programmes, ["environment"], "north") == [], "No match is a valid answer / ไม่พบก็เป็นคำตอบที่ถูกได้"
print("OK: ready to move into finder.py")

# %% [markdown]
# ## 3. Default values and keyword arguments / ค่าเริ่มต้นและการระบุชื่ออาร์กิวเมนต์
#
# `region="any"` is a **default**: leave it out and the function uses `"any"`. You can also name an argument, for example `language="th"`.
# **Predict** the three counts.
#
# `region="any"` คือ **ค่าเริ่มต้น** ถ้าไม่ส่งจะใช้ `"any"` และยังระบุชื่ออาร์กิวเมนต์ได้ เช่น `language="th"` **ทำนาย** จำนวนทั้งสาม

# %%
print(len(find_programmes(programmes, ["food"])))
print(len(find_programmes(programmes, ["food"], language="th")))
print(len(find_programmes(programmes, ["food"], region="south", language="en")))

# %% [markdown]
# ## 4. Modify (stretch): rank the results / ปรับแก้ (ต่อยอด): เรียงผลลัพธ์
#
# Sort so programmes sharing **more** interests come first. `sort(key=...)` calls your function on each result and sorts by what it returns.
#
# เรียงให้หลักสูตรที่ตรง **มากกว่า** ขึ้นก่อน `sort(key=...)` เรียกฟังก์ชันของเรากับผลแต่ละรายการแล้วเรียงตามค่าที่คืน

# %%
def number_of_shared_interests(result):
    return len(result["matched_interests"])


ranked = find_programmes(programmes, ["technology", "design", "data"])
# YOUR CODE HERE / เขียนโค้ดตรงนี้
for result in ranked[:5]:
    print(number_of_shared_interests(result), result["programme"]["programme_en"])

# %% [markdown]
# **Explain to a partner without notes:** which line skips a record for its region? For its language? For its interests? What does the function give back when nothing matches?
#
# **อธิบายให้เพื่อนฟังโดยไม่ดูโน้ต:** บรรทัดใดข้ามรายการเพราะภูมิภาค เพราะภาษา เพราะความสนใจ และฟังก์ชันคืนอะไรเมื่อไม่มีรายการตรง
