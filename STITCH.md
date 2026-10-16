# Day 3: from a design to a wired page / วันที่ 3: จากแบบหน้าเว็บสู่หน้าที่ต่อสายแล้ว

A design tool such as Google Stitch can draw a page, but it does not know your API. You wire the design to the contract in `API.md` by hand: no AI coding and no paid account. `app.js` (TODO 8–10) already talks to the API; wiring only adds HTML attributes.

เครื่องมือออกแบบอย่าง Google Stitch วาดหน้าเว็บได้ แต่ไม่รู้จัก API ของเรา เราต่อสายแบบหน้าเว็บเข้ากับข้อตกลงใน API.md เอง ไม่ใช้ AI เขียนโค้ดและไม่ต้องมีบัญชีแบบเสียเงิน app.js (TODO 8–10) คุยกับ API อยู่แล้ว การต่อสายคือเพิ่มแอตทริบิวต์ HTML เท่านั้น

## 1. Choose where the design comes from / เลือกแหล่งของแบบหน้าเว็บ

Every route is wired the same way. / ทุกทางต่อสายแบบเดียวกัน

| Route | Design | Account |
|---|---|---|
| A | Your teacher generates a Stitch design from your brief and gives you the exported HTML | None for you |
| B | You use Stitch yourself, only if you meet its current age and account rules and your school allows it | Your own Google account |
| C | `designs/practice-export.html`: a hand-made practice export that looks finished but is not wired | None |
| D | Sketch your page on paper first, then use route C and restyle it towards your sketch | None |

ทาง A ครูสร้างแบบใน Stitch จากโจทย์ของเราแล้วส่ง HTML ให้ ทาง B ใช้ Stitch เองเฉพาะเมื่อเข้าเกณฑ์อายุและบัญชีปัจจุบันและโรงเรียนอนุญาต ทาง C ใช้ไฟล์ฝึก designs/practice-export.html ทาง D ร่างบนกระดาษก่อนแล้วใช้ทาง C

## 2. The prompt card (routes A and B) / บัตรคำสั่ง

Fill in the brackets and paste the whole card. One audience, one change at a time.

```text
Design a single web page for [audience, e.g. a Grade 9 student choosing a path / a parent who reads Thai first].
It helps them explore Thai university programmes by interest. Mood: [e.g. calm and trustworthy].
The page needs, in this order:
1. A short heading and one sentence of introduction, in English and Thai.
2. 14 interest checkboxes with these labels: Technology, Design, Games, Business, Data and numbers, Science,
   Food, People, Society, Communication, Environment, Health and care, Teaching and learning, Arts and performance.
3. A Region dropdown: Any, Central including Bangkok, North, South, Northeast, East, West.
4. A Teaching language dropdown: Any, Thai including bilingual, English including bilingual, Bilingual, Unresolved.
5. A checkbox "Include programmes whose language is not confirmed", and a Search button.
6. A one-line status message, then a results area with ONE sample result card showing only:
   university name, programme name in English and Thai, province, programme format, teaching language,
   a short summary, shared interests, and a link to the official programme page.
Rules: no sign-in, no ratings, no match percentages, no prices or fees, no photos of people.
Use real checkboxes and dropdowns, and a font that can display Thai.
```

กรอกในวงเล็บแล้ววางทั้งบัตร กลุ่มผู้ใช้เดียว แก้ทีละเรื่อง ห้ามมีการเข้าสู่ระบบ คะแนน เปอร์เซ็นต์ความตรง ราคา หรือรูปคน

Export the design as **HTML** (not React or Figma) and save it as `designs/my-design.html`. Menu names change; ask your teacher if you cannot find the export. If the export loads Tailwind or fonts from the internet, the page needs internet to look right.

ส่งออกเป็น HTML (ไม่ใช่ React หรือ Figma) แล้วบันทึกเป็น designs/my-design.html ถ้าไฟล์โหลด Tailwind หรือฟอนต์จากอินเทอร์เน็ต หน้าจะสวยเมื่อมีอินเทอร์เน็ตเท่านั้น

## 3. Move the design in / ย้ายแบบเข้าโครงงาน

1. Rename `static/index.html` to `static/index-before.html` (your before picture, and a working reference).
2. Copy your design file to `static/index.html`.
3. Run the contract checks. They fail: that list is your wiring to-do list.

```sh
python -m unittest tests.test_contract -v
```

เปลี่ยนชื่อ static/index.html เป็น index-before.html คัดลอกไฟล์แบบมาเป็น static/index.html แล้วรันการตรวจข้อตกลง รายการที่ไม่ผ่านคือสิ่งที่ต้องต่อสาย

## 4. The wiring checklist / รายการต่อสาย

| In the design | Add or change | Why |
|---|---|---|
| `<head>` | `<script src="/static/app.js" defer></script>` | Plugs in the frontend module |
| The block around the controls | Make it `<form id="finder-form" method="get" action="/api/programmes">` … `</form>` | app.js listens to this form |
| Each interest checkbox | `name="interests" value="games"` (values from `API.md` / `data/dataset-info.json`) | The API reads `interests` |
| Region dropdown | `<select name="region">`, each option `value="any"`, `"north"`, … | The API refuses unknown regions (400) |
| Language dropdown | `<select name="language">`, values `any`, `th`, `en`, `th_en`, `unknown` | Same names as the URL |
| Unconfirmed-language checkbox | `name="include_unknown" value="yes"` | |
| Search button | `type="submit"`, inside the form | Sends the form |
| Status line | `id="status"` | Counts and errors appear here |
| Results area | `id="results"`, and delete the sample cards inside it | Cards are drawn here |

Missing a checkbox? Copy one and change its label and value: the checks need all 14 interests.

ขาดช่องความสนใจ ให้คัดลอกช่องเดิมแล้วแก้ป้ายและ value ต้องมีครบ 14 ช่อง

## 5. Turn one sample card into the template / ทำการ์ดตัวอย่างเป็นแม่แบบ

1. Cut ONE sample card and paste it inside `<template id="card-template">` … `</template>`, after the results area.
2. Delete its sample text and mark each place with the API field it shows:

| Mark | Meaning | Example |
|---|---|---|
| `data-field="programme_en"` | The text becomes that field | `<h3 data-field="programme_en"></h3>` |
| `data-empty="…"` | Text to show when the field is empty | `data-empty="Province not mapped"` |
| `data-link="programme_url"` | The link goes to that field | `<a data-link="programme_url">View programme</a>` |
| `data-show="teaching_language:unknown"` | Keep this element only when the field has that value | An "unconfirmed language" note |

3. Delete anything the API cannot supply or UniPath does not do: sign-in, save buttons, match percentages, rankings, prices, sample photos. Do not add them to the API.

ตัดการ์ดตัวอย่างหนึ่งใบใส่ใน template ลบข้อความตัวอย่าง แล้วระบุฟิลด์ด้วย data-field data-link data-show ลบสิ่งที่ API ไม่มีหรือ UniPath ไม่ทำ เช่น การเข้าสู่ระบบ เปอร์เซ็นต์ความตรง อันดับ ราคา

## 6. Prove it is wired / พิสูจน์ว่าต่อสายแล้ว

| Check | Wired | Not wired |
|---|---|---|
| `python -m unittest discover -s tests -v` | All pass | The failure names the missing id, name, value or field |
| Network tab after Search | A **fetch** request to `/api/programmes?…` | A **document** request, or none |
| The page | Cards appear without reloading | Raw JSON, or nothing |
| Copy the address and open it in a new tab | The same search runs again | |

| If the test says | Do this |
|---|---|
| `id="status"` not found | Add `id="status"` to the status line |
| Interest checkboxes missing: `['health']` | Add the checkbox with `value="health"` |
| `Not in API.md: ['tuition']` | Delete that `data-field`; the API has no such field |
| Keep `<template id="card-template">` | Step 5 |

Record your before/after: a screenshot of `index-before.html` and your wired page, and one sentence on what you changed for your audience.

บันทึกก่อน/หลัง: ภาพหน้าจอ index-before.html กับหน้าที่ต่อสายแล้ว และหนึ่งประโยคว่าเปลี่ยนอะไรเพื่อกลุ่มผู้ใช้
