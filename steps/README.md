# Day 2 steps / ขั้นวันที่ 2

Each step is a small website that plugs in one more module. Run them from the project folder, one at a time, and **predict before you open the page**. Stop each server with Ctrl+C before starting the next.

แต่ละขั้นเป็นเว็บเล็ก ๆ ที่เสียบโมดูลเพิ่มทีละตัว รันจากโฟลเดอร์โครงงานทีละขั้น ทำนายก่อนเปิดหน้าเว็บ และหยุดด้วย Ctrl+C ก่อนขั้นถัดไป

| Step | Run | Plugs in / เสียบ |
|---|---|---|
| 1 | `python -m steps.step1_hello` | Flask: the browser asks, the server answers / เบราว์เซอร์ถาม เซิร์ฟเวอร์ตอบ |
| 2 | `python -m steps.step2_data` | `data_loader`: the answer becomes JSON data / คำตอบเป็น JSON |
| 3 | `python -m steps.step3_finder` | `finder` (Day 1): a fixed search / การค้นหาที่กำหนดไว้ |
| 4 | `python -m steps.step4_url` | `request.args`: the URL chooses the search / URL เลือกการค้นหา |
| 5 | `python app.py` | `preferences` + `search`: your TODO 6 and 7, the real API / TODO 6 และ 7 คือ API จริง |

Step 4 trusts whatever the URL says. Try `/?region=mars`: the answer is simply empty, and nobody is told why. Step 5 adds the safety check (TODO 6) and answers with status 400 instead (TODO 7).

ขั้น 4 เชื่อทุกค่าใน URL ลอง /?region=mars ผลว่างเปล่าโดยไม่มีใครรู้สาเหตุ ขั้น 5 เพิ่มการตรวจ (TODO 6) และตอบสถานะ 400 (TODO 7)

Use the same interpreter as the website, for example `.venv/bin/python -m steps.step1_hello` (Windows: `.\.venv\Scripts\python.exe -m steps.step1_hello`).
