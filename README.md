# Student edition / เวอร์ชันผู้เรียน

# UniPath Thailand

## Start in VS Code / เริ่มใน VS Code

Extract this ZIP into a new folder. Open the project folder containing `app.py` and `finder.py` in VS Code. Keep your working files separate from the original ZIP. Do not overwrite your work when resetting.

แตก ZIP ลงโฟลเดอร์ใหม่ เปิดโฟลเดอร์ที่มี app.py และ finder.py ใน VS Code เก็บงานแยกจาก ZIP เดิม อย่าทับงานเมื่อเริ่มใหม่

Python 3.10 or newer is the classroom recommendation. In VS Code, install the **Python** and **Jupyter** extensions.

แนะนำ Python 3.10 ขึ้นไป ติดตั้งส่วนขยาย Python และ Jupyter ใน VS Code

## Setup on Day 1 / ติดตั้งในวันที่ 1

Create one environment for the whole course. `requirements-dev.txt` adds the notebook kernel to Flask and pypdf. macOS / Linux:

สร้าง environment ครั้งเดียวใช้ทั้งหลักสูตร requirements-dev.txt เพิ่ม kernel สำหรับสมุดโน้ตนอกเหนือจาก Flask และ pypdf

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

Windows PowerShell (activation is not required):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Then open `notebooks/01-meet-the-data.ipynb`, click **Select Kernel** and choose `.venv`. Work through notebooks 01–05 in order (see `notebooks/README.md`). Notebook 05 moves your functions into `finder.py`; then run the console version:

จากนั้นเปิด notebooks/01-meet-the-data.ipynb เลือก kernel เป็น .venv ทำสมุด 01–05 ตามลำดับ สมุด 05 ย้ายฟังก์ชันไปไว้ใน finder.py แล้วรันคอนโซล

```sh
.venv/bin/python console.py
```

`primm_example.py` is a three-record warm-up for learners without notebook support. On Windows use `.\.venv\Scripts\python.exe` in place of `.venv/bin/python`.

primm_example.py เป็นตัวอย่างอุ่นเครื่องสามรายการสำหรับเครื่องที่ใช้สมุดโน้ตไม่ได้ Windows ใช้ .\.venv\Scripts\python.exe แทน

## Run the website (Day 2 onwards) / รันเว็บไซต์ (ตั้งแต่วันที่ 2)

```sh
.venv/bin/python app.py
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe app.py
```

Visit http://127.0.0.1:5001/ . Stop the server with Ctrl+C. The site runs locally and uses no database. Installation needs internet access; afterwards, programme matching works offline. Official source links still need internet. Only the Day 4 portfolio page can contact an AI service, and only when a key is set (see below).

เปิด http://127.0.0.1:5001/ หยุดด้วย Ctrl+C เว็บรันในเครื่อง ไม่ใช้ฐานข้อมูล ติดตั้งต้องใช้อินเทอร์เน็ต หลังติดตั้งแล้วจับคู่ข้อมูลออฟไลน์ได้ มีเพียงหน้าแฟ้มผลงานวันที่ 4 ที่ติดต่อบริการ AI ได้เมื่อตั้งคีย์ไว้

If the port is busy, run `-m flask --app app run --host 127.0.0.1 --port 5002` with the environment interpreter and visit that port.

หากพอร์ตไม่ว่าง ใช้ interpreter ของ environment รัน -m flask --app app run --host 127.0.0.1 --port 5002

## The module map / แผนที่โมดูล

Each file is a module with one job. Its functions are the plugs: what goes in and what comes out. Each day plugs in one more layer.

แต่ละไฟล์เป็นโมดูลที่มีหน้าที่เดียว ฟังก์ชันคือปลั๊ก บอกว่ารับอะไรและส่งอะไรออก แต่ละวันเสียบเพิ่มหนึ่งชั้น

```
 Day 3  FRONTEND (browser)                Day 2  BACKEND (Flask server)
 static/index.html  ─GET /api/programmes?interests=games&region=north─▶  app.py  (wiring board)
 static/app.js      ◀──────────── JSON (see API.md) ─────────────────     │ request.args
                                                                          ▼
                                                     preferences.parse_preferences(args) → (preferences, problems)
                                                                          ▼
                                                     search.search_answer(preferences, limit) → answer
                                                                          ▼
 Day 1  DATA AND LOGIC                               finder.find_programmes(programmes, ...) → results
                                                     data_loader.load_programmes() → programmes

 Day 4  static/portfolio.html ─POST /api/portfolio (PDF)─▶ portfolio.py → pdf_text → ai_reader → preferences → search
```

`API.md` is the contract between the frontend and the backend. Open http://127.0.0.1:5001/api/programmes?region=north in the browser to see the raw JSON. `steps/` rebuilds the backend one plug at a time (Day 2).

API.md คือข้อตกลงระหว่างส่วนหน้าและส่วนหลัง เปิดลิงก์ API ในเบราว์เซอร์เพื่อดู JSON ดิบ โฟลเดอร์ steps ประกอบส่วนหลังทีละปลั๊ก (วันที่ 2)

## Files / ไฟล์

- `notebooks/`: Day 1 data notebooks, from types to functions / สมุดโน้ตวันที่ 1 จากชนิดข้อมูลสู่ฟังก์ชัน
- `primm_example.py`: a three-record warm-up without notebooks / ตัวอย่างอุ่นเครื่องเมื่อไม่มีสมุดโน้ต
- `finder.py`: the student-owned Python rules (Day 1) / กติกา Python ของผู้เรียน
- `steps/`: four tiny websites that plug in one module each (Day 2) / เว็บเล็กสี่ขั้น เสียบทีละโมดูล
- `app.py`: the wiring board, with the JSON API route (Day 2) / แผงเดินสายและเส้นทาง API
- `preferences.py`: turns browser values into safe preferences (Day 2) / แปลงค่าจากเบราว์เซอร์ให้ปลอดภัย
- `search.py`: runs the search and shapes the answer API.md promises (Day 2) / ค้นหาและจัดรูปคำตอบ
- `static/index.html`, `static/app.js`, `static/style.css`: the frontend (Day 3); the result card is the `<template id="card-template">` in index.html / ส่วนหน้า การ์ดผลลัพธ์คือ template ใน index.html
- `STITCH.md`, `designs/`: wiring a generated design to the API by hand, with a practice export (Day 3) / ต่อสายแบบหน้าเว็บเข้ากับ API เอง พร้อมไฟล์ฝึก
- `portfolio.py`, `pdf_text.py`, `ai_reader.py`, `static/portfolio.html`, `static/portfolio.js`: the portfolio reader (Day 4) / ตัวอ่านแฟ้มผลงาน
- `API.md`: the frontend/backend contract / ข้อตกลง API
- `language_policy.py`, `data_loader.py`, `settings.py`, `console.py`: supplied helpers / ตัวช่วยที่ให้มา
- `data/`: public programme data, sources, fictional practice preferences and fictional sample portfolios (`data/portfolios/`) / ข้อมูลสาธารณะ ข้อมูลฝึกสมมติ และแฟ้มผลงานตัวอย่างสมมติ
- `fetch_mytcas.py`, `mytcas_rules.json`, `data/MYTCAS.md`: optional larger dataset / ชุดข้อมูลใหญ่แบบเลือกได้
- `DEPLOY.md`: putting the site online on Day 4 / การนำเว็บขึ้นออนไลน์
- `tests/`: behaviour checks, not admission predictions / การตรวจพฤติกรรม ไม่ใช่ทำนายรับเข้า

## Check your work / ตรวจการทำงาน

From this project folder, with the environment interpreter:

```sh
python -m unittest discover -s tests -v
```

`test_finder` (Day 1) and `test_contract` (Day 3) need no Flask. `test_api` (Day 2) and `test_portfolio` (Day 4) are skipped until Flask and pypdf are installed; they never contact an AI service. Run all checks after every AI edit. Passing checks the sampled behaviours, not the whole website or admission eligibility.

test_finder และ test_contract ไม่ต้องใช้ Flask ส่วน test_api และ test_portfolio จะข้ามจนกว่าติดตั้ง Flask และ pypdf และไม่ติดต่อบริการ AI รันการตรวจหลังทุกการแก้ด้วย AI ผ่านหมายถึงพฤติกรรมตัวอย่างตรง ไม่ใช่ยืนยันคุณสมบัติรับเข้า

## Data meaning / ความหมายข้อมูล

The built-in sample has 16 curated public-university programmes, not all Thai programmes. Empty interests means no interest restriction; otherwise match any shared tag. `region=any` means no region restriction. Bilingual records match English or Thai preferences. Unknown-language records appear only if explicitly included, and keep the unresolved label. No admission criteria or acceptance probabilities are supplied. Match count is preference overlap, not an admission score. An optional MyTCAS pack adds thousands of programmes for local exploration (see `data/MYTCAS.md`).

ตัวอย่างในโครงงานมี 16 หลักสูตรมหาวิทยาลัยรัฐ ไม่ใช่ทุกหลักสูตรในไทย เมื่อไม่เลือกความสนใจคือไม่จำกัด any คือไม่จำกัดภูมิภาค สองภาษาตรงตัวกรองไทยหรืออังกฤษ รายการไม่ทราบภาษารวมเมื่อเลือกเท่านั้นและต้องคงป้าย ไม่มีเกณฑ์หรือโอกาสรับเข้า ชุด MyTCAS เพิ่มหลักสูตรจำนวนมากสำหรับสำรวจในเครื่อง

## AI and ownership / AI และความเข้าใจ

Days 1–2 are done without AI, including an individual Python rule change at the end of Day 2. On Day 3, write TODO 8–10 (the fetch code) yourself. A design tool such as Stitch may then draw the page (your teacher's export, your own if you are eligible, or `designs/practice-export.html`), and you wire it to `API.md` by hand with `STITCH.md`: no AI coding or paid account is needed. If you do use an AI coding assistant, paste `API.md`, ask for one change at a time, read the changed files and run all checks (especially `test_contract`) before keeping an edit.

On Day 4 the website itself uses AI. The portfolio reader sends PDF text to Claude only when an `ANTHROPIC_API_KEY` is set; without one, the offline keyword reader answers. Copy `.env.example` to `.env` and paste the key your teacher gives you. Never commit, zip or share `.env`. Use only the fictional samples in `data/portfolios/`.

วันที่ 1–2 ไม่ใช้ AI รวมถึงการแก้กติกา Python รายบุคคลท้ายวันที่ 2 วันที่ 3 เขียน TODO 8–10 (fetch) เอง แล้วเครื่องมือออกแบบอย่าง Stitch วาดหน้าเว็บได้ (ไฟล์จากครู ของตนเองถ้าเข้าเกณฑ์ หรือ designs/practice-export.html) แล้วต่อสายเข้ากับ API.md เองตาม STITCH.md ไม่ต้องใช้ AI เขียนโค้ดหรือบัญชีเสียเงิน ถ้าใช้ผู้ช่วย AI ให้แนบ API.md แก้ทีละเรื่อง อ่านไฟล์ที่เปลี่ยน และรันการตรวจก่อนเก็บ

วันที่ 4 เว็บใช้ AI เอง ตัวอ่านแฟ้มส่งข้อความไปยัง Claude เฉพาะเมื่อมี ANTHROPIC_API_KEY ถ้าไม่มีจะใช้ตัวอ่านคำสำคัญในเครื่อง คัดลอก .env.example เป็น .env แล้ววางคีย์ที่ครูให้ ห้าม commit บีบอัด หรือแชร์ .env และใช้เฉพาะแฟ้มตัวอย่างสมมติ
