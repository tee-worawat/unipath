# Deploy your website / นำเว็บขึ้นออนไลน์

Day 4. Written 12 October 2026. Hosting sites change their screens and rules, so your teacher checks these steps before class.

วันที่ 4 เขียนเมื่อ 12 ตุลาคม 2026 หน้าจอและกติกาของผู้ให้บริการเปลี่ยนได้ ครูตรวจขั้นตอนก่อนเรียน

## Before you start / ก่อนเริ่ม

- You need your own account on the hosting site. Follow your school's rules and get parent or guardian permission. Use a school-approved email. / ต้องมีบัญชีของตนเอง ทำตามกติกาโรงเรียนและขออนุญาตผู้ปกครอง ใช้อีเมลที่โรงเรียนอนุญาต
- Run all checks locally first: `python3 -m unittest discover -s tests -v`. / รันการตรวจทั้งหมดในเครื่องก่อน
- Deploy with `PROGRAMME_FILE = "programmes.json"` in `settings.py`. Do not put the MyTCAS pack on a public website until your teacher confirms the data terms. / ใช้ข้อมูล 16 รายการเมื่อเผยแพร่ ห้ามนำชุด MyTCAS ขึ้นเว็บสาธารณะจนกว่าครูยืนยัน
- Your website is public. Never add names, photos, grades or anything personal. / เว็บเป็นสาธารณะ ห้ามใส่ข้อมูลส่วนตัว

## Option A: PythonAnywhere (main route) / ทางหลัก

PythonAnywhere's free Beginner account hosts one Flask web app and needs no GitHub account. Its terms did not state a minimum age when checked on 12 October 2026. Free web apps stop after about a month unless you log in and extend them.

บัญชีฟรีรองรับเว็บ Flask หนึ่งเว็บ ไม่ต้องใช้ GitHub ตรวจเงื่อนไขเมื่อ 12 ต.ค. 2026 ไม่พบการระบุอายุขั้นต่ำ เว็บฟรีหยุดทำงานประมาณหนึ่งเดือนหากไม่เข้าไปต่ออายุ

1. Set `AI_MODE = "offline"` in `settings.py`. Zip your project folder without `.venv` and `.env`. Sign up for a Beginner account. / ตั้ง AI_MODE = "offline" บีบอัดโฟลเดอร์ (ไม่รวม .venv และ .env) แล้วสมัครบัญชี Beginner
2. **Files** tab: upload the ZIP. Open a **Bash console** and unzip it, for example `unzip student.zip -d unipath`. Note the folder that contains `app.py`, e.g. `/home/YOURNAME/unipath/student`. / อัปโหลด ZIP เปิด Bash console แล้วแตกไฟล์ จดโฟลเดอร์ที่มี app.py
3. In the same console, create an environment and install Flask and pypdf: / สร้าง environment และติดตั้ง Flask กับ pypdf

   ```sh
   mkvirtualenv --python=/usr/bin/python3.13 unipath
   pip install -r ~/unipath/student/requirements.txt
   ```

4. **Web** tab → **Add a new web app** → **Manual configuration** → the same Python version. Do not choose the Flask quick-start: it creates a different app. / เลือก Manual configuration และ Python รุ่นเดียวกัน ไม่เลือก Flask quick-start
5. In **Virtualenv**, enter `unipath`. Open the **WSGI configuration file** link and replace everything with: / ใส่ unipath ในช่อง Virtualenv แล้วแก้ไฟล์ WSGI เป็น

   ```python
   import sys
   path = "/home/YOURNAME/unipath/student"
   if path not in sys.path:
       sys.path.insert(0, path)
   from app import app as application
   ```

6. Press **Reload** and visit `https://YOURNAME.pythonanywhere.com/`. / กด Reload แล้วเปิดเว็บ

### The portfolio reader online / ตัวอ่านแฟ้มผลงานบนเว็บ

A public website can be used by anyone. If it held the class API key, strangers could spend it. **Deploy with `AI_MODE = "offline"` in `settings.py`**: the portfolio page then uses the keyword reader, and nothing is sent to an AI service. Never upload `.env`.

เว็บสาธารณะใครก็ใช้ได้ ถ้ามีคีย์ API ของห้อง คนอื่นจะใช้คีย์นั้นได้ จึงตั้ง AI_MODE = "offline" ใน settings.py ก่อนเผยแพร่ ห้ามอัปโหลดไฟล์ .env

Your teacher may switch Claude on for a short showcase: in the WSGI file, above `from app import app as application`, they add `import os` and `os.environ["ANTHROPIC_API_KEY"] = "..."` with a key that has a spending limit, set `AI_MODE = "auto"`, press Reload, and remove the key afterwards. PythonAnywhere's free accounts can reach `api.anthropic.com` (it was on their list of allowed sites when checked on 13 October 2026). This step is for the teacher only.

ครูอาจเปิด Claude ช่วงนำเสนอสั้น ๆ โดยใส่คีย์ที่จำกัดค่าใช้จ่ายในไฟล์ WSGI แล้วลบออกภายหลัง บัญชีฟรีเรียก api.anthropic.com ได้ (ตรวจเมื่อ 13 ต.ค. 2026) ขั้นนี้สำหรับครูเท่านั้น

### Production check / ตรวจหลังขึ้นออนไลน์

- Search with a normal input, a no-result input and an unresolved-language input. / ลองกรณีทั่วไป ไม่มีผล และภาษาไม่ทราบ
- Open `/portfolio` and read one sample PDF from `data/portfolios/`. The page should say it used the offline keyword reader. / เปิด /portfolio อ่านไฟล์ตัวอย่าง หน้าเว็บต้องบอกว่าใช้ตัวอ่านคำสำคัญ
- Open DevTools → Network: the request goes to `/api/programmes?...` and answers 200. Try `/api/programmes?region=mars`: it should answer 400. / ตรวจ Network ว่าเรียก API และได้ 200 ลอง region=mars ต้องได้ 400
- Open the site on a phone. / เปิดบนมือถือ
- `debug` stays `False`. Never add passwords or keys to your code or your ZIP. / ห้ามเปิด debug และห้ามใส่รหัสผ่านหรือคีย์ในโค้ดหรือ ZIP

If you see "Something went wrong" or a 502 error, open the **error log** link on the Web tab and read the last lines. The most common causes are a wrong path in the WSGI file, a missing package in the environment, or a file uploaded to a different folder.

หากเห็นข้อผิดพลาดหรือ 502 เปิด error log บนแท็บ Web แล้วอ่านบรรทัดสุดท้าย สาเหตุที่พบบ่อยคือพาธใน WSGI ผิด ไม่ได้ติดตั้งแพ็กเกจ หรืออัปโหลดผิดโฟลเดอร์

## Other hosts / ทางเลือกอื่น

- **Render** (needs a GitHub account; GitHub requires age 13+). Render's own age terms were not verified on 12 October 2026. Your teacher must check before use. / ต้องมีบัญชี GitHub (13 ปีขึ้นไป) ยังไม่ได้ตรวจเงื่อนไขอายุของ Render
- **Vercel** is not suitable for this class: its terms require users to be at least 16. / Vercel ไม่เหมาะ เพราะกำหนดอายุ 16 ปีขึ้นไป
- No account? Show the local website on your laptop. Deployment is a bonus, not part of the core assessment. / ไม่มีบัญชีให้สาธิตในเครื่อง การเผยแพร่เป็นงานเสริม ไม่ใช่การประเมินหลัก
