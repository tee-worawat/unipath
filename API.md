# UniPath API contract / ข้อตกลง API

The backend (`app.py`, Day 2) and the frontend (`static/`, Day 3) agree on this contract. Change it only on purpose, and update both sides and the tests together. When asking AI to generate or restyle the frontend, paste this file and say it must not change.

ส่วนหลัง (app.py วันที่ 2) และส่วนหน้า (static/ วันที่ 3) ตกลงกันตามเอกสารนี้ เปลี่ยนเมื่อตั้งใจเท่านั้น และแก้ทั้งสองฝั่งพร้อมการทดสอบ เมื่อให้ AI สร้างหรือออกแบบส่วนหน้า ให้แนบไฟล์นี้และบอกว่าห้ามเปลี่ยน

## Request / คำขอ

`GET /api/programmes?interests=games&interests=design&region=north&language=en&include_unknown=yes&limit=20`

| Parameter | Values | If missing |
|---|---|---|
| `interests` | A tag from `data/dataset-info.json › interest_tags`. Repeat the name for several interests. | No interest restriction |
| `region` | `any` or a key from `regions` | `any` |
| `language` | `any`, `th`, `en`, `th_en` or `unknown` | `any` |
| `include_unknown` | `yes` includes unresolved-language records when a language is chosen | Not included |
| `limit` | 1–200 results to send | 50 |

The form in `static/index.html` uses the same names. Without JavaScript it opens this JSON directly (Day 2); once `static/app.js` is plugged in, JavaScript sends the same request and draws cards (Day 3). The frontend must keep `id="finder-form"`, `id="status"`, `id="results"` and these field names.

ฟอร์มใน static/index.html ใช้ชื่อเดียวกัน ถ้าไม่มี JavaScript จะเปิด JSON นี้โดยตรง (วันที่ 2) เมื่อเสียบ app.js แล้ว JavaScript ส่งคำขอเดียวกันและวาดการ์ด (วันที่ 3) ส่วนหน้าต้องคง id และชื่อช่องเหล่านี้

## Success: status 200 / สำเร็จ

`count` is every match; `returned` is how many are in `results` (at most `limit`). Each result has exactly these fields:

```json
{
  "count": 1,
  "returned": 1,
  "filters": {"interests": ["games"], "region": "north", "language": "any", "include_unknown": false},
  "results": [
    {
      "id": "cmu-digital-game",
      "programme_en": "Digital Game",
      "programme_th": "เกมดิจิทัล",
      "university_en": "Chiang Mai University",
      "university_th": "มหาวิทยาลัยเชียงใหม่",
      "province": "Chiang Mai",
      "region": "north",
      "programme_format": "bilingual",
      "teaching_language": "th_en",
      "matched_interests": ["games"],
      "summary_en": "…",
      "summary_th": "…",
      "programme_url": "https://…",
      "admission_url": null,
      "admission_reference_year_be": null,
      "data_notes": ["…"]
    }
  ]
}
```

`null` means not collected or not available. It never means zero, free or eligible. `province` can be `null` in the MyTCAS pack when a campus has not been mapped.

null หมายถึงไม่ได้เก็บหรือไม่มีข้อมูล ไม่ได้แปลว่าศูนย์ ฟรี หรือมีสิทธิ์สมัคร

## Problem: status 400 / ค่าไม่ถูกต้อง

An unknown interest, region or language is refused rather than silently ignored:

```json
{"error": "invalid_preferences", "problems": ["unknown region: mars"]}
```

The frontend must check `response.ok` and show the problems to the user.

ส่วนหน้าต้องตรวจ response.ok และแสดงปัญหาให้ผู้ใช้เห็น

## Portfolio: Day 4 / แฟ้มผลงาน วันที่ 4

`POST /api/portfolio` with `multipart/form-data` (a file cannot travel in a URL):

| Field | Value |
|---|---|
| `portfolio` | A PDF, at most 10 pages and 2 MB. Read in memory, never saved. |
| `region`, `language`, `include_unknown`, `limit` | Optional, as above |

The reader suggests at most four interest tags, each with a quote from the portfolio. The server keeps a suggestion only if the quote is really in the text **and** the tag passes `parse_preferences`, the same check as a typed URL. It then searches with the kept tags. The answer has the success fields above plus:

| Field | Meaning |
|---|---|
| `reader` | `"claude"` or `"offline"` (the keyword reader) |
| `characters_read`, `text_preview` | How much text was read, and its first 300 characters: what an AI service would see |
| `evidence` | `[{"tag": "games", "quote": "…"}]`, the suggestions that were kept |
| `refused` | Problems from `parse_preferences`, e.g. `"unknown interest: astronaut"` |
| `notes` | Anything dropped or replaced, e.g. a quote that is not in the portfolio |

If no tag is kept, `count` is 0 and `results` is empty. A missing file, a non-PDF or an unreadable PDF answers status 400 with `{"error": "invalid_portfolio", "problems": [...]}`; a file over 2 MB answers 413.

ตัวอ่านแนะนำแท็กไม่เกินสี่แท็กพร้อมคำพูดจากแฟ้ม เซิร์ฟเวอร์เก็บเฉพาะคำแนะนำที่คำพูดมีจริงในแฟ้มและแท็กผ่าน parse_preferences แล้วจึงค้นหา ไม่พบแท็กใดได้ผล 0 รายการ ไฟล์ผิดได้สถานะ 400 ไฟล์ใหญ่เกิน 2 MB ได้ 413

## Stretch ideas / ต่อยอด

Change the contract first, then the code and tests: a `q` text search over Thai and English names; a `sort` option; a `university_group` filter for the MyTCAS pack.

เปลี่ยนข้อตกลงก่อน แล้วจึงแก้โค้ดและการทดสอบ เช่น ค้นหาข้อความ q การเรียง หรือกรองกลุ่มมหาวิทยาลัย
