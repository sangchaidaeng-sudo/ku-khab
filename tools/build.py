"""Build the deployed index.html from src/app.html (adds SEO meta, JSON-LD). Run: python3 tools/build.py"""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(os.path.join(ROOT,'src','app.html'),encoding='utf-8').read()
extra='''<meta name="description" content="คาบ — ตารางเรียน KU ฉบับนิสิต วางรายวิชาจาก MyKU แล้วดูคาบถัดไป ตารางทั้งสัปดาห์ และบันทึกเป็นรูปได้ ไม่ต้องใช้รหัสนนทรี">
<meta property="og:title" content="คาบ · ตารางเรียน KU ฉบับนิสิต">
<meta property="og:description" content="วางรายวิชาจาก MyKU แล้วรู้ทันทีว่าคาบถัดไปคืออะไร ไม่ต้องใช้รหัสนนทรี">
<meta property="og:image" content="og.png">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="คาบ">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
'''
extra=extra.replace('<meta property="og:image" content="og.png">','<meta property="og:image" content="https://ku-khab.vercel.app/og.png">\n<meta property="og:url" content="https://ku-khab.vercel.app/">\n<link rel="canonical" href="https://ku-khab.vercel.app/">')
s=s.replace('<meta name="theme-color" content="#faf9f6">','<meta name="theme-color" content="#faf9f6">\n'+extra,1)

import json as _j
s=s.replace('<title>คาบ · ตารางเรียน KU</title>','<title>ตารางเรียน KU ฉบับนิสิต · คาบ | จัดตารางเรียน ม.เกษตรศาสตร์ จาก MyKU ฟรี</title>',1)
s=s.replace('<meta name="description" content="คาบ — ตารางเรียน KU ฉบับนิสิต วางรายวิชาจาก MyKU แล้วดูคาบถัดไป ตารางทั้งสัปดาห์ และบันทึกเป็นรูปได้ ไม่ต้องใช้รหัสนนทรี">',
 '<meta name="description" content="คาบ เว็บจัดตารางเรียนฟรีสำหรับนิสิตเกษตรศาสตร์ (KU) วางรายวิชาจาก MyKU แล้วได้ตารางเรียนทันที รู้คาบถัดไป เตือนเวลาชน บันทึกเป็นรูปวอลเปเปอร์ได้ ไม่ต้องใช้รหัสนนทรี">',1)
ld={"@context":"https://schema.org","@graph":[
 {"@type":"WebApplication","name":"คาบ","alternateName":["Khab","ku-khab","ตารางเรียน KU"],"url":"https://ku-khab.vercel.app/","applicationCategory":"EducationalApplication","operatingSystem":"Any","inLanguage":"th","description":"เว็บจัดตารางเรียนฟรีสำหรับนิสิตมหาวิทยาลัยเกษตรศาสตร์ วางรายวิชาจาก MyKU แล้วได้ตารางเรียนรายสัปดาห์","offers":{"@type":"Offer","price":"0","priceCurrency":"THB"},"author":{"@type":"Person","name":"Daeng","url":"https://www.instagram.com/daen6_/"},"image":"https://ku-khab.vercel.app/og.png"},
 {"@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"ต้องใช้รหัสนนทรีไหม","acceptedAnswer":{"@type":"Answer","text":"ไม่ต้อง คาบไม่ขอรหัสผ่านใด ๆ ข้อมูลตารางเก็บอยู่ในเบราว์เซอร์ของคุณเท่านั้น"}},
  {"@type":"Question","name":"ใช้บนมือถือได้ไหม","acceptedAnswer":{"@type":"Answer","text":"ได้ เปิดใน Safari หรือ Chrome แล้วเลือกเพิ่มไปยังหน้าจอโฮม"}},
  {"@type":"Question","name":"ใช้แทน KU Get Reg ได้ไหม","acceptedAnswer":{"@type":"Answer","text":"ใช้ดูและจัดตารางเรียนได้โดยไม่ต้องล็อกอิน คาบเป็นโปรเจกต์อิสระ ไม่เกี่ยวข้องกับ KU Get Reg หรือมหาวิทยาลัย"}}]}]}
s=s.replace('</head>','<script type="application/ld+json">'+_j.dumps(ld,ensure_ascii=False).replace('<','\\u003c')+'</script>\n</head>',1)
s=s.replace('<meta property="og:title" content="คาบ · ตารางเรียน KU ฉบับนิสิต">','<meta property="og:title" content="คาบ · ตารางเรียน KU ฉบับนิสิต">\n<meta property="og:site_name" content="คาบ">\n<meta property="og:locale" content="th_TH">',1)
open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(s)
print(s.count('ku-khab.vercel.app'))
