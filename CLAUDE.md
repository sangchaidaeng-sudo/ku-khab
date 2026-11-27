# CLAUDE.md — คาบ (ku-khab)

เว็บจัดตารางเรียนฟรีสำหรับนิสิต ม.เกษตรศาสตร์ (KU) ทำขึ้นแทน KU Get Reg ซึ่งปิด 1 ธ.ค. 2569
- เว็บจริง: https://ku-khab.vercel.app (Vercel deploy อัตโนมัติเมื่อ push `main`)
- Repo: github.com/sangchaidaeng-sudo/ku-khab
- เจ้าของ: Daeng (IG @daen6_) นิสิตพืชสวน มก. กำแพงแสน — **คุยภาษาไทยเสมอ**

## กติกาที่ห้ามเปลี่ยน
- **ห้ามขอรหัสนนทรี** หรือรหัสผ่านใด ๆ ข้อมูลอยู่ใน `localStorage` ของผู้ใช้เท่านั้น ไม่มี backend
- นำเข้าตารางด้วย **คัดลอกข้อความจาก MyKU แล้ววาง** (หรือ JSON จาก AI) — ผู้ใช้ไม่เอาแบบอัปโหลดรูป/OCR
- ต้องมีข้อความ "คาบ ไม่ใช่ระบบของมหาวิทยาลัย ตรวจสอบตารางจริงกับ MyKU เสมอ" และเครดิต @daen6_ (https://www.instagram.com/daen6_/)
- **ห้ามลบ** `googlef1673b7fa6084081.html` (ยืนยัน Google Search Console) และ `65c1d760eba5b68174cc5df65a38d638.txt` (คีย์ IndexNow/Bing)
- ธีมเริ่มต้น = `thaiday` (สีประจำวัน), ฟอนต์ไทย = Kanit, ฟอนต์ตัวเลข/รหัส = Space Grotesk

## โครงสร้าง
```
src/app.html      ← ซอร์สจริง ไฟล์เดียว (HTML+CSS+JS) แก้ที่นี่เท่านั้น
tools/build.py    ← สร้าง index.html จาก src/app.html (ใส่ title/meta SEO, JSON-LD, og)
index.html        ← ไฟล์ที่ deploy (generated — อย่าแก้ตรง)
guide.html        ← หน้า SEO ข้อความล้วน: วิธีจัดตารางจาก MyKU (HowTo JSON-LD)
ku-get-reg.html   ← หน้า SEO: "KU Get Reg ปิดแล้วใช้อะไรแทน" (FAQ JSON-LD)
robots.txt, sitemap.xml, manifest.webmanifest, icon-*.png, apple-touch-icon.png, favicon-32.png, og.png
.vercelignore     ← ไม่ deploy src/ tools/ CLAUDE.md README.md
```

## Workflow
1. แก้ `src/app.html`
2. `python3 tools/build.py`
3. ทดสอบ (ดูด้านล่าง)
4. ถ้าเพิ่ม/แก้หน้า static ให้อัปเดต `lastmod` ใน `sitemap.xml`
5. commit + push:
```
git -c user.name="sangchaidaeng-sudo" -c user.email="sangchaidaeng-sudo@users.noreply.github.com" commit -m "<msg>"
git -c push.negotiate=true push origin main
```
มีสำเนาเป็น Claude artifact ด้วย (slug `40479678-7c5f-4866-b8ea-f7234709b071`, ประกาศ capability `downloads`) — ถ้าอยู่ใน session ที่มี artifact tools ให้ publish `src/app.html` เป็น `index.html` ทุกครั้งที่แก้

## โมเดลข้อมูล (ใน `src/app.html`)
- `localStorage['kutable.v2']` = `S = {term, courses, theme, colorBy, themeV, vw, me}`
- course: `{id, code, name, credits, sec, color, sessions:[{d, s, e, room, kind}], exams:[{kind,date,start,end}]}`
  - `d` 0=จันทร์ … 6=อาทิตย์, `s`/`e` เป็นนาทีนับจากเที่ยงคืน, `kind` = 'บรรยาย' | 'ปฏิบัติ' | ''
- `save()` มี guard: ตอนดูตารางเพื่อน (`VIEW`) จะไม่เขียนทับตารางตัวเอง (`MINE`)

## ส่วนสำคัญในโค้ด
- **Parser ข้อความ**: regex วัน/เวลา (`SESRX`), ข้าม label, หน่วยกิต "(3)", หมู่/หมู่ปฏิบัติ/Lab, kind ตามคีย์เวิร์ดล่าสุด, "ห้อง ติดต่อผู้สอน"
- **`fromJSON`**: นำเข้า JSON จาก prompt AI และไฟล์สำรอง (เก็บ exams ด้วย)
- **ตารางสัปดาห์** (`render()`): แนวนอน แบ่ง lane เมื่อเวลาซ้อน, เตือนชน (`clashes`), `.sh` = บล็อกสั้น ≤75 นาที
  - บล็อกแสดง **ชื่อวิชา + ห้อง** (ไม่แสดงเวลา — ผู้ใช้ขอ) เวลาดูได้จาก tooltip/แตะเปิด
- **มุมมองรายวัน** (`dayView()`): มือถือ ปัดเปลี่ยนวัน, แสดงเวลา
- **board()**: กำลังเรียน/คาบถัดไป
- **ธีม**: `THEMES` 11 แบบ, `cvFor(c,d)` สีตามวิชาหรือตามวัน
- **บันทึกรูป** (`drawSchedule(mode)`): canvas `land` (แนวนอน) / `port` (1080×1920) → `DLNS.save` ใน artifact, `<a download>` บนเว็บ
- **แชร์**: `?t=` + `z`(deflate-raw)/`j` + base64url ของ `pack()`, QR จาก cdnjs `qrcode-generator@1.4.4` (โหลดตอนใช้)

## ทดสอบ
- Playwright (Python) กับ `file://.../index.html` — ใน sandbox ฟอนต์และ cdnjs ถูกบล็อก ให้ route cdnjs ไป node_modules ในเครื่อง
- เช็กอย่างน้อย: วางตัวอย่างข้อความ MyKU → ตารางขึ้น, ไม่มี pageerror, 1440px / 820px (iPad) / 390px (มือถือ), export รูปทั้งสองแบบ, ลิงก์แชร์เปิดได้
- ตัวอย่างข้อความที่ parser ต้องรองรับ:
```
02036281-66 โรคพืชวิทยาเบื้องต้น(3)
บรรยาย หมู่ 700
MON 13:00 - 14:00 ห้อง LH4-102
ปฏิบัติ หมู่ 715
FRI 13:00 - 16:00 ห้อง ติดต่อผู้สอน
```

## SEO (สถานะ 27 พ.ย. 2569)
- Search Console ยืนยันแล้ว (HTML file), ส่ง sitemap แล้ว, หน้าแรกถูก index (`site:ku-khab.vercel.app`)
- ยังไม่ติดอันดับคำค้นทั่วไป: เว็บใหม่ + ยังไม่มี backlink + คำว่า "คาบ" กำกวม
- คู่แข่งในผลค้นหา "ตารางเรียน KU": ku-table, KU Retro Timetable, หน้าสำนักบริหารการศึกษา
- งานต่อ: ขอ index หน้าใหม่ใน Search Console, หา backlink (โพสต์กลุ่ม KU, Pantip, IG bio), Bing Webmaster

## งานที่เหลือ (ทำทีละ task ตามที่ผู้ใช้ขอ)
- **Task 3 — หาเวลาว่างตรงกับเพื่อน**: รวมตารางตัวเอง + ลิงก์แชร์ของเพื่อนหลายคน (ใช้ `?t=` token ที่มีอยู่, decode ด้วย `unpack`) แล้วแสดงช่วงที่ทุกคนว่างในวัน จ.–ศ. 8:00–20:00, เลือก/ไม่เลือกเพื่อนแต่ละคนได้, ห้ามบันทึกตารางเพื่อนทับของตัวเอง
- **Task 4 — ตารางสอบ + ส่งออก**: แสดงวันสอบกลางภาค/ปลายภาคจาก `exams` (มีจาก JSON แล้ว), เตือนสอบชน, ส่งออก `.ics` ให้ Google/Apple Calendar (ทั้งคาบเรียนแบบ weekly RRULE และวันสอบ) — การบันทึกรูปทำเสร็จแล้ว
- ข้อเสนอที่ค้างไว้: ข้อความโพสต์โปรโมต, Vercel Web Analytics, โดเมนของตัวเองภายหลัง (ไม่ฟรี ~$10/ปี)
