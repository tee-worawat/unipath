# 05-move-it-to-a-file: plain-script copy of the notebook. Run top to bottom; it stops at the first check that fails.
# สำเนาแบบสคริปต์ รันจากบนลงล่าง และหยุดที่การตรวจแรกที่ยังไม่ผ่าน

# %% [markdown]
# # 05 · Move it into the project / ย้ายเข้าโครงงาน
#
# **Goal:** put your functions into `finder.py`, so the console, the project checks and tomorrow's website all use the same code.
# **เป้าหมาย:** นำฟังก์ชันไปไว้ใน `finder.py` เพื่อให้คอนโซล การตรวจของโครงงาน และเว็บไซต์พรุ่งนี้ใช้โค้ดชุดเดียวกัน
#
# A notebook is a scratchpad. The website and the tests import functions from **files**, so code left only in a notebook cell never reaches the website.
# สมุดโน้ตเป็นที่ทดลอง เว็บไซต์และการตรวจนำเข้าฟังก์ชันจาก **ไฟล์** โค้ดที่อยู่ในเซลล์อย่างเดียวจึงไปไม่ถึงเว็บไซต์
#
# **Steps / ขั้นตอน**
# 1. Open `finder.py` in the project folder (one level above `notebooks/`). / เปิด `finder.py` ในโฟลเดอร์โครงงาน
# 2. TODO 1: replace the loop body in `shared_interests` with your code from Exercise 4.2. / แทนที่ TODO 1 ด้วยโค้ดจากฝึก 4.2
# 3. TODO 2–5: complete `find_programmes` with your four steps from Exercise 4.3. Keep the first line (`def find_programmes(...)`) unchanged. / เติม TODO 2–5 ด้วยสี่ขั้นจากฝึก 4.3 และคงบรรทัดแรกไว้
# 4. Save the file (Ctrl+S or Cmd+S), then run the cells below. After every change to `finder.py`, save and run them again. / บันทึกไฟล์แล้วรันเซลล์ด้านล่าง ทุกครั้งที่แก้ให้บันทึกแล้วรันใหม่

# %%
# Supplied: load finder.py again so your latest saved version is used.
# ให้มาแล้ว: โหลด finder.py ใหม่เพื่อใช้ฉบับที่บันทึกล่าสุด
import importlib
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "programmes.json").is_file())
sys.path.insert(0, str(PROJECT))
import finder
importlib.reload(finder)
from data_loader import load_json

programmes = load_json("programmes.json")
print("Using", Path(finder.__file__).name, "from", PROJECT.name)

# %% [markdown]
# ## 1. Quick check / ตรวจเร็ว
#
# **Predict:** which programme should northern games return? / **ทำนาย:** เกม + ภาคเหนือควรได้หลักสูตรใด

# %%
results = finder.find_programmes(programmes, ["games"], "north")
for result in results:
    print(result["programme"]["programme_en"], result["matched_interests"])
print(len(results), "result(s)")

# %%
# ✅ Check / ตรวจ
assert [r["programme"]["id"] for r in results] == ["cmu-digital-game"], "finder.py still differs from notebook 04. Did you save the file and run the cell above again? / บันทึกไฟล์และรันเซลล์ด้านบนใหม่แล้วหรือยัง"
print("OK")

# %% [markdown]
# ## 2. Run the project checks / รันการตรวจของโครงงาน
#
# These are the same checks your teacher uses. A `FAIL` names the behaviour that is still missing; read it before changing code. Never delete a check to make it pass.
#
# เป็นการตรวจชุดเดียวกับที่ครูใช้ `FAIL` บอกพฤติกรรมที่ยังขาด อ่านก่อนแก้โค้ด ห้ามลบการตรวจเพื่อให้ผ่าน

# %%
sys.modules.pop("test_finder", None)
suite = unittest.defaultTestLoader.discover(str(PROJECT / "tests"), pattern="test_finder.py", top_level_dir=str(PROJECT / "tests"))
checks = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)

# %%
# ✅ Check / ตรวจ
assert checks.testsRun == 6, "Expected six finder checks / ควรมีการตรวจหกข้อ"
assert checks.wasSuccessful(), "Read the FAIL lines above, fix finder.py, save, and run from the top of this notebook / อ่านบรรทัด FAIL แก้ finder.py บันทึก แล้วรันใหม่ตั้งแต่ต้น"
print("OK: finder.py passes every Day 1 check.")

# %% [markdown]
# ## 3. Run the console program / รันโปรแกรมคอนโซล
#
# `console.py` imports `find_programmes` from `finder.py`, just as the website's `search.py` will tomorrow. **Predict** its output: interests technology + design, region north.
#
# `console.py` นำเข้า `find_programmes` จาก `finder.py` เหมือนที่ `search.py` ของเว็บไซต์จะทำพรุ่งนี้ **ทำนาย** ผลลัพธ์ของเทคโนโลยี + ออกแบบ ภาคเหนือ

# %%
run = subprocess.run([sys.executable, "console.py"], cwd=PROJECT, capture_output=True, text=True, encoding="utf-8")
print(run.stdout or run.stderr)

# %% [markdown]
# ## 4. Exit check: explain on your own / ตรวจก่อนจบ: อธิบายด้วยตนเอง
#
# Without notes or AI, tell your teacher:
# 1. One programme that stays and one that is skipped for a search you choose, and which line of `finder.py` decided.
# 2. Why an unknown-language record never appears as English.
# 3. What `find_programmes` returns when nothing matches, and why that is not an error.
#
# Write your answer to 1 in `WORKBOOK.md`, item 3. Tomorrow, the website's backend calls this same `find_programmes` for every URL a browser sends.
#
# อธิบายให้ครูฟังโดยไม่ดูโน้ตและไม่ใช้ AI: (1) หลักสูตรที่เก็บและที่ข้ามจากการค้นหาที่เลือก และบรรทัดใดใน `finder.py` ตัดสิน (2) ทำไมรายการที่ไม่ทราบภาษาไม่แสดงเป็นอังกฤษ (3) `find_programmes` คืนอะไรเมื่อไม่มีรายการตรง และทำไมไม่ใช่ข้อผิดพลาด เขียนข้อ 1 ใน `WORKBOOK.md` ข้อ 3 พรุ่งนี้ส่วนหลังของเว็บไซต์จะเรียก `find_programmes` เดียวกันนี้ทุกครั้งที่เบราว์เซอร์ส่ง URL มา
