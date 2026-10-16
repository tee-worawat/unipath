"""Project settings you may change.

PROGRAMME_FILE chooses the programme list for the website and API:
- "programmes.json": 16 curated, source-checked records. The default, and the one to deploy.
- "programmes-all.json": the optional MyTCAS classroom pack (see data/MYTCAS.md).
  Use it locally. Do not deploy it publicly until your teacher confirms the data terms.

ตั้งค่าไฟล์ข้อมูล ค่าเริ่มต้นคือ 16 หลักสูตรที่ตรวจแล้ว ชุด MyTCAS ใช้ในเครื่องเท่านั้นจนกว่าครูยืนยันเงื่อนไขข้อมูล

AI_MODE chooses the Day 4 portfolio reader:
- "auto": Claude when an ANTHROPIC_API_KEY is set (in .env or the environment), otherwise offline.
- "offline": a keyword reader that runs on this computer. Nothing leaves it. Use it on public sites.
- "claude": always ask Claude; without a key the offline reader answers, with a note saying so.

ตัวอ่านแฟ้มผลงานวันที่ 4: auto ใช้ Claude เมื่อมีคีย์ ไม่มีคีย์ใช้ตัวอ่านคำสำคัญในเครื่อง เว็บสาธารณะใช้ offline
"""
PROGRAMME_FILE = "programmes.json"

AI_MODE = "auto"
AI_MODEL = "claude-haiku-5-5"
MAX_UPLOAD_MB = 2
