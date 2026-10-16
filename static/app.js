// Day 3: the frontend module. The browser asks the Flask API for data, then draws the results itself.
// Until the last lines plug it in, the form simply opens the raw JSON (that is how Day 2 uses it).
// วันที่ 3: ส่วนหน้า เบราว์เซอร์ขอข้อมูลจาก API แล้ววาดผลลัพธ์เอง ก่อนเสียบบรรทัดท้ายไฟล์ ฟอร์มจะเปิด JSON ดิบ

const form = document.querySelector("#finder-form");
const statusBox = document.querySelector("#status");
const resultsBox = document.querySelector("#results");
const cardTemplate = document.querySelector("#card_template_2");

// Before TODO 8: open the browser DevTools Console and predict, then run:
//   fetch("/api/programmes?interests=games&region=north").then(r => r.json()).then(console.log)
// ก่อนเริ่ม: เปิด Console ทำนายผล แล้วรันคำสั่งด้านบน

function buildQuery(formElement) {
  const params = new URLSearchParams();
  // console.log(new FormData(formElement))
  // for (const [name, value] of new FormData(formElement)) {
  //   params.append(name, value);
  // }
  for (const [name, value] of new FormData(formElement)){
    params.append(name,value);
  }
  console.log("log",params.toString());
  
  return params.toString();
  //throw new Error("TODO 8 in static/app.js: build the query string");
}

async function fetchProgrammes(query) {
  // calling the api 
  const response = await fetch(`/api/programmes?${query}`);
  console.log("response", response)
  const data = await response.json()
  if (!response.ok){
    throw new Error((data.problems || ["The server could not answer."]).join("; "));
  }
  return data

  // const data = await response.json();
  // if (!response.ok) {
  //   throw new Error((data.problems || ["The server could not answer."]).join("; "));
  // }
  // return data;
  // throw new Error("TODO 9 in static/app.js: fetch from the API");
}

function showResults(data) {
  resultsBox.replaceChildren();
  statusBox.textContent = data.returned < data.count
    ? `${data.count} results, showing the first ${data.returned} / ผลลัพธ์`
    : `${data.count} results / ผลลัพธ์`;
  if (data.count === 0) {
    const empty = document.createElement("p");
    empty.className = "notice";
    empty.textContent = "No results from this sample. Try another filter. This does not mean Thailand has no suitable programmes. / ไม่พบจากตัวอย่างนี้ ลองตัวกรองอื่น";
    resultsBox.append(empty);
  }
  for (const programme of data.results) {
    resultsBox.append(programmeCard(programme));
  }
}

// Supplied: one result card, copied from <template id="card-template"> in index.html.
// The design lives in the HTML, so a card designed elsewhere (for example in Stitch) is wired by
// marking its elements with data-field, data-link and data-show: no JavaScript changes needed.
// Data is written with textContent (never innerHTML).
// การ์ดผลลัพธ์คัดลอกจาก template ใน index.html แบบการ์ดอยู่ใน HTML จึงต่อการ์ดที่ออกแบบไว้ได้ด้วย data-field โดยไม่ต้องแก้ JavaScript
function programmeCard(programme) {
  const card = cardTemplate.content.firstElementChild.cloneNode(true);
  // for (const element of card.querySelectorAll("[data-show]")) {
  //   const [field, wanted] = element.dataset.show.split(":");
  //   if (String(programme[field]) !== wanted) element.remove();
  // }

  for (const element of card.querySelectorAll("[data-field]")) {
    const value = programme[element.dataset.field];
    const text = Array.isArray(value) ? value.join(" · ") : value;
    // if (element.dataset.field == 'region'){
    //   text= text.toUpperCase();
    // }
    if (text !== null && text !== undefined && text !== "") element.textContent = text;
    else if (element.dataset.empty) element.textContent = element.dataset.empty;
    else element.remove();
  }
  // const data_interest = programme['interest_tags']
  // document.querySelector("#interests").replaceChildren(
  //   ...data_interest.map((interest) => {
  //     const badge = document.createElement("span");
  //     badge.className =
  //       "px-2 py-0.5 bg-orange-50 text-brand-700 border border-orange-200/60 rounded-md text-[11px] font-medium";
  //     badge.textContent = interest;
  //     return badge;
  //   })
  // );
  // for (const element of card.querySelector("[data-interest")){
  //   const value = programme[element.dataset.field];
  //   for( const v of value){
  //     add("span",value)
  //   }
  // // }
  // for (const link of card.querySelectorAll("[data-link]")) {
  //   const url = programme[link.dataset.link];
  //   if (url) link.href = url;
  //   else link.remove();
  // }
  return card;
}

// Search without leaving the page.
async function handleSearch(event) {
  event.preventDefault(); // Stay on this page: JavaScript will fetch the data instead.
  const query = buildQuery(form);
  history.replaceState(null, "", `?${query}`); // Keep a shareable address.
  statusBox.textContent = "Loading… / กำลังโหลด…";
  try {
    showResults(await fetchProgrammes(query));
  } catch (error) {
    resultsBox.replaceChildren();
    statusBox.textContent = `Could not load results: ${error.message} / โหลดผลลัพธ์ไม่ได้`;
  }
}

// Supplied: a shared address such as /?interests=games&region=north fills the form and searches.
function restoreFromAddress() {
  const params = new URLSearchParams(location.search);
  if (!params.size) return;
  for (const box of form.querySelectorAll("input[type=checkbox]")) {
    box.checked = params.getAll(box.name).includes(box.value);
  }
  for (const select of form.querySelectorAll("select")) {
    if (params.has(select.name)) select.value = params.get(select.name);
  }
  form.requestSubmit();
}

// Plug the frontend in: after TODO 8–10, remove the // from the next two lines and reload.
// The form then stays on this page instead of opening the raw JSON.
// เสียบส่วนหน้า: เมื่อเสร็จ TODO 8–10 ให้ลบ // หน้าสองบรรทัดถัดไปแล้วโหลดหน้าใหม่
form.addEventListener("submit", handleSearch);
restoreFromAddress();
