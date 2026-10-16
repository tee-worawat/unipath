# Day 1 notebooks / สมุดโน้ตวันที่ 1

Work through them in order. Each one ends with code you will reuse in the next.

ทำตามลำดับ แต่ละสมุดจบด้วยโค้ดที่ใช้ต่อในสมุดถัดไป

| Notebook | You learn / สิ่งที่เรียน | Ends with / จบด้วย |
|---|---|---|
| `01-meet-the-data.ipynb` | `str`, `int`, `list`, `dict`, `None`; indexing | Reading any field safely / อ่านฟิลด์ได้อย่างปลอดภัย |
| `02-ask-questions.ipynb` | loops, `in`, counters, tally dictionaries | Counting what we do not know / นับสิ่งที่ไม่รู้ |
| `03-filter-by-hand.ipynb` | filter pattern, `and`, any-of, `continue`, honest language rule | Every rule the finder needs / ทุกกติกาที่ตัวค้นหาต้องใช้ |
| `04-name-it-functions.ipynb` | parameters, `return`, defaults | `shared_interests` and `find_programmes` |
| `05-move-it-to-a-file.ipynb` | files, imports, project checks | `finder.py` passing every Day 1 check / ผ่านการตรวจวันที่ 1 |

## Open in VS Code / เปิดใน VS Code

1. Install the **Python** and **Jupyter** extensions in VS Code. / ติดตั้งส่วนขยาย Python และ Jupyter
2. Create the project environment and install the notebook kernel (see the project README, "Setup"). / สร้าง environment และติดตั้ง kernel ตาม README
3. Open a `.ipynb` file, click **Select Kernel** (top right) and choose the `.venv` environment. / เลือก kernel เป็น `.venv`
4. Run one cell with **Shift+Enter**. Run cells from the top; after restarting, use **Run All** above the cell you are on. / รันทีละเซลล์ด้วย Shift+Enter รันจากบนลงล่าง

A ✅ cell checks your work. Do not edit or delete it.

เซลล์ ✅ ใช้ตรวจงาน อย่าแก้หรือลบ

## No notebook support? / ใช้สมุดโน้ตไม่ได้

`plain/` holds the same exercises as ordinary Python files. Edit one in VS Code and run it from the project folder, for example `python notebooks/plain/01-meet-the-data.py`. It stops at the first check that fails.

โฟลเดอร์ `plain/` มีแบบฝึกเดียวกันเป็นไฟล์ Python ธรรมดา แก้ใน VS Code แล้วรันจากโฟลเดอร์โครงงาน เช่น `python notebooks/plain/01-meet-the-data.py` จะหยุดที่การตรวจแรกที่ยังไม่ผ่าน
