// Day 4 (supplied): send the PDF to /api/portfolio and show what came back.
// A file cannot travel in a URL, so this request uses POST with FormData.
// วันที่ 4: ส่ง PDF ไปที่ /api/portfolio ด้วย POST เพราะไฟล์ใส่ใน URL ไม่ได้

const portfolioForm = document.querySelector("#portfolio-form");
const portfolioStatus = document.querySelector("#portfolio-status");
const portfolioResults = document.querySelector("#portfolio-results");

function addText(parent, tag, text, className) {
  const element = document.createElement(tag);
  element.textContent = text; // Text, never HTML: the reply contains words from an uploaded file.
  if (className) element.className = className;
  parent.append(element);
  return element;
}

function showReading(data) {
  portfolioResults.replaceChildren();
  const reader = data.reader === "claude" ? "Claude" : "the offline keyword reader";
  portfolioStatus.textContent = `Read ${data.characters_read} characters with ${reader}. ${data.count} programmes match. / อ่านแล้ว ${data.count} หลักสูตรตรง`;
  addText(portfolioResults, "p", `Text that was read / ข้อความที่อ่าน: “${data.text_preview}…”`, "small");
  addText(portfolioResults, "h3", "Suggested interests and evidence / ความสนใจและหลักฐาน");
  const list = addText(portfolioResults, "ul", "");
  for (const item of data.evidence) {
    addText(list, "li", `${item.tag}: “${item.quote}”`);
  }
  if (!data.evidence.length) addText(list, "li", "None / ไม่พบ");
  for (const problem of data.refused) addText(portfolioResults, "p", `Refused / ไม่ใช้: ${problem}`, "notice small");
  for (const note of data.notes) addText(portfolioResults, "p", note, "notice small");
  addText(portfolioResults, "h3", "Programmes / หลักสูตร");
  const cards = addText(portfolioResults, "div", "", "results");
  for (const programme of data.results) {
    const card = addText(cards, "article", "", "programme");
    addText(card, "p", programme.university_en, "eyebrow");
    addText(card, "h3", programme.programme_en);
    addText(card, "p", `${programme.programme_th} · ${programme.university_th}`);
    addText(card, "p", `Shared interests / ความสนใจที่ตรง: ${programme.matched_interests.join(", ")}`);
    const link = addText(card, "a", "Official programme / แหล่งทางการ ↗");
    link.href = programme.programme_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  }
}

portfolioForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  portfolioStatus.textContent = "Reading… / กำลังอ่าน…";
  try {
    const response = await fetch("/api/portfolio", { method: "POST", body: new FormData(portfolioForm) });
    const data = await response.json();
    if (!response.ok) throw new Error((data.problems || ["The server could not answer."]).join("; "));
    showReading(data);
  } catch (error) {
    portfolioResults.replaceChildren();
    portfolioStatus.textContent = `Could not read the portfolio: ${error.message} / อ่านแฟ้มไม่ได้`;
  }
});
