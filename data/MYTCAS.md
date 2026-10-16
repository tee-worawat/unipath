# Optional MyTCAS classroom pack / ชุดข้อมูล MyTCAS (ทางเลือก)

The built-in `programmes.json` has 16 hand-checked programmes. The MyTCAS pack has thousands, built from the public MyTCAS course index by `fetch_mytcas.py`.

ข้อมูลในโครงงานมี 16 หลักสูตรที่ตรวจด้วยมือ ชุด MyTCAS มีหลายพันหลักสูตร สร้างจากดัชนีหลักสูตรสาธารณะของ MyTCAS

## Get it / วิธีได้ข้อมูล

- From your teacher: put `programmes-all.json` in this `data/` folder. / รับไฟล์จากครูแล้ววางในโฟลเดอร์ data
- Or build it yourself with internet: `python3 fetch_mytcas.py`. / หรือสร้างเองด้วยคำสั่งนี้เมื่อมีอินเทอร์เน็ต

Then set `PROGRAMME_FILE = "programmes-all.json"` in `settings.py` and restart the server. The checks in `tests/` keep using the 16 curated records, so their expected numbers do not change.

จากนั้นตั้งค่าใน settings.py แล้วเริ่มเซิร์ฟเวอร์ใหม่ การตรวจยังใช้ 16 รายการเดิม

## What the fields mean / ความหมาย

| From MyTCAS (as published) | Our editorial guesses (mytcas_rules.json) |
|---|---|
| University, campus, faculty, programme names, MyTCAS programme type, cost note (`cost_text_th`), programme page link | `province`, `region`, `interest_tags`, `university_group`, `teaching_language` derived from the programme type |

- A Thai-type programme is recorded as Thai teaching. International and bilingual types stay `unknown` for language: the label alone does not prove English. / หลักสูตรไทยบันทึกว่าสอนภาษาไทย นานาชาติและสองภาษายังเป็น unknown
- `province` is `null` where a campus is not mapped yet. That is a gap in our rules, not missing campuses. / จังหวัด null คือยังไม่ได้จับคู่วิทยาเขต
- The cost note is text copied from MyTCAS. It is not verified and is not total tuition. / ข้อความค่าใช้จ่ายคัดจาก MyTCAS ยังไม่ตรวจ ไม่ใช่ค่าเล่าเรียนรวม
- Names are as universities typed them, including spacing and spelling mistakes. Spotting and fixing them is a good data-cleaning task. / ชื่อเป็นไปตามที่มหาวิทยาลัยกรอก รวมถึงคำผิด เป็นแบบฝึกทำความสะอาดข้อมูลที่ดี
- Universities keep adding programmes during the admissions year, so coverage changes. Check the official programme page before deciding anything. / มหาวิทยาลัยเพิ่มหลักสูตรตลอดปี ตรวจหน้าทางการก่อนตัดสินใจ

## Rules for use / ข้อกำหนด

Use it on your own laptop for learning. Do not publish it on a public website until your teacher confirms the data terms. It contains no admission criteria, scores or chances, and a match never means you are eligible.

ใช้ในเครื่องเพื่อการเรียน ห้ามเผยแพร่บนเว็บสาธารณะจนกว่าครูยืนยัน ไม่มีเกณฑ์ คะแนน หรือโอกาสรับเข้า การจับคู่ไม่ได้แปลว่ามีสิทธิ์สมัคร

Source: MyTCAS course index (https://course.mytcas.com/), operated for TCAS admissions. / แหล่งข้อมูล: ดัชนีหลักสูตร MyTCAS
