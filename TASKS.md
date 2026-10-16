# Student tasks / งานผู้เรียน

This skeleton runs with unfinished logic. The page opens, but searches return nothing useful until the TODOs are done. That is unfinished code, not evidence that no university fits. Use failing checks to locate missing behaviours. Do not remove tests to make the result look successful.

โครงนี้รันได้แต่กติกายังไม่เสร็จ หน้าเว็บเปิดได้แต่การค้นหายังไม่มีผลที่มีความหมายจนกว่าเติม TODO ใช้ผลการตรวจที่ไม่ผ่านช่วยหาสิ่งที่ขาด อย่าลบการตรวจเพื่อให้ดูผ่าน

## Day 1: Python rules / กติกา Python

Work through `notebooks/01`–`05` in order. Predict before each run, and treat a failing ✅ cell as a clue, not a grade.

1. `01`: name the type of every value in a record; `None` is not 0. / บอกชนิดของค่า None ไม่ใช่ 0
2. `02`: count, collect and tally with loops and `in`. / นับ เก็บ และนับแยกด้วยลูป
3. `03`: filter by hand: `and`, any-of interests, `"any"`, and the honest language rule. / กรองด้วยมือ
4. `04`: turn those rules into `shared_interests` and `find_programmes`. / เปลี่ยนกติกาเป็นฟังก์ชัน
5. `05`: paste them into `finder.py` (TODO 1–5), save, and pass `tests/test_finder.py`; run `console.py`. / ย้ายเข้า finder.py และผ่านการตรวจ

Explain one programme that stays and one that is skipped, and which line decided.

ทำสมุด 01–05 ตามลำดับ ทำนายก่อนรันทุกครั้ง เซลล์ ✅ ที่ไม่ผ่านคือเบาะแส ไม่ใช่คะแนน สุดท้ายอธิบายรายการที่เก็บกับที่ข้าม และบรรทัดใดตัดสิน

## Day 2: the backend / ส่วนหลัง

1. Run `steps/` 1–4 in order (see `steps/README.md`). Predict each page before you open it, and say which module the step plugged in. / รัน steps 1–4 ทำนายก่อนเปิด และบอกว่าขั้นนั้นเสียบโมดูลใด
2. In step 4, try `/?region=mars`. Nothing complains. That is why the real API checks values first. / ลอง region=mars ในขั้น 4 ไม่มีใครเตือน
3. TODO 6 in `preferences.py`: read the values, keep known ones, report unknown ones. / เติม TODO 6
4. Read `API.md`. Predict the JSON for `/api/programmes?interests=games&region=north` on paper. / อ่าน API.md ทำนาย JSON บนกระดาษ
5. TODO 7 in `app.py` (7a–7b) and `search.py` (7c): answer with JSON as the contract says, including status 400 for refused values. Run `python app.py`, open the URL from step 4, and check with `python -m unittest tests.test_api -v`. / เติม TODO 7 แล้วตรวจด้วย test_api
6. Use the form at `/`: it opens the raw JSON. Look at the address bar: the form wrote the URL. / ใช้ฟอร์มที่ / จะเปิด JSON ดิบ ฟอร์มเป็นผู้เขียน URL
7. Exit check without AI: trace one choice from the URL through `parse_preferences`, `search_answer` and `find_programmes` back to the JSON. Then add a `require_all=False` parameter to `find_programmes`: when it is `True`, keep only programmes that have every selected interest. All checks must still pass. Show technology + design + north with `require_all=True`. / ตรวจก่อนจบ: ไล่เส้นทาง แล้วเพิ่มพารามิเตอร์ require_all ใน find_programmes โดยการตรวจเดิมยังผ่าน

## Day 3: the frontend / ส่วนหน้า

1. Open DevTools → Console. Predict, then run the `fetch(...)` line at the top of `static/app.js`. / เปิด Console ทำนายแล้วรันคำสั่ง fetch
2. TODO 8–10 in `static/app.js`: build the query, fetch, show results and errors. Then plug the frontend in: remove the `//` from the last two lines and reload. Watch the request in DevTools → Network. / เขียน TODO 8–10 แล้วเสียบส่วนหน้า ดูคำขอในแท็บ Network
3. Design for your own audience, then wire it by hand with `STITCH.md`: get a design (Stitch export from your teacher or yourself, or `designs/practice-export.html`), move it into `static/index.html`, add the ids, names and values from the checklist, turn one sample card into `<template id="card-template">` with `data-field` marks, and delete what the API cannot supply. `test_contract` is your to-do list; the Network tab must show a fetch. Make at least one design edit yourself. / ออกแบบสำหรับกลุ่มผู้ใช้ แล้วต่อสายเองตาม STITCH.md ใช้ test_contract เป็นรายการงาน แก้แบบเองอย่างน้อยหนึ่งจุด
4. Fix the integration bug your teacher gives you, starting from the symptom and the Network tab. / แก้บั๊กการเชื่อมต่อที่ครูให้ เริ่มจากอาการและแท็บ Network
5. Exit check without AI: explain the journey from a click to the cards on screen, and predict what breaks if the API renames a field or the page renames an id. / อธิบายเส้นทางจากการคลิกถึงการ์ด และทำนายว่าถ้าเปลี่ยนชื่อฟิลด์หรือ id จะเกิดอะไร

## Day 4: the portfolio reader, then deploy / ตัวอ่านแฟ้มผลงาน แล้วเผยแพร่

1. Open `/portfolio` and read a sample from `data/portfolios/` with the offline keyword reader. Predict which interests it will find. / เปิด /portfolio อ่านแฟ้มตัวอย่าง ทำนายว่าจะพบความสนใจใด
2. TODO 11 in `ai_reader.py`: write the instructions for Claude. Read `text_preview`: that is exactly what would be sent. / เขียนคำสั่งถึง Claude ดู text_preview ว่าอะไรจะถูกส่ง
3. TODO 12 in `portfolio.py`: never trust the model. Keep a suggestion only if its quote is really in the portfolio and its tag passes `parse_preferences`. Check with `python -m unittest tests.test_portfolio -v`. / ห้ามเชื่อโมเดล ตรวจคำพูดและแท็กก่อนค้นหา
4. With your teacher's key in `.env`, compare Claude's suggestions with the offline reader's for the same sample. / เทียบผลของ Claude กับตัวอ่านคำสำคัญ
5. Deploy with `DEPLOY.md` (`AI_MODE = "offline"` on public sites) if you have an approved account; otherwise demo locally. / เผยแพร่ตาม DEPLOY.md หรือสาธิตในเครื่อง
6. Present the problem, your rule, the module map, one bug, how the AI module is checked, and how AI helped you build. / นำเสนอปัญหา กติกา แผนที่โมดูล บั๊ก วิธีตรวจโมดูล AI และการใช้ AI

The starter banner comes from `edition.py`. For your finished project you can set EDITION to "finished". This only removes the banner; it does not complete any task.

ป้ายเริ่มต้นมาจาก edition.py งานที่เสร็จแล้วตั้งเป็น "finished" ได้ การเปลี่ยนป้ายไม่ได้ทำงานแทนเรา
