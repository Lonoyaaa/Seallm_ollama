# Seallm_ollama

Linebot สำหรับตอบคำถามโดยใช้ข้อมูลจากเซ็ตข้อมูลในการเลือกสร้างคำขอโดย Seallm-7b

## Installation
ติดตั้ง Ollama (https://ollama.com/download) จากลิงก์ดังกล่าว จากนั้นดาวน์โหลดโมเดลภาษา

```bash
ollama pull "nxphi47/seallm-7b-v2:q4_0"
```
จากนั้นติดตั้งแพ็กเกจที่จำเป็น
```bash
pip install -r requirements.txt
```
## Usage
Host ตัว webhook (app.py) เพื่อให้ได้ ้URL ที่เป็น HTTP ซึ่งเข้าถึงได้

*การเพิ่มข้อมูล : 

1. เพิ่มไฟล์ .docx หรือ .csv ในโฟลเดอร์ dataset
2. ส่ง POST request ไปที่ URL เดียวกับ webhook ที่ /update_v_db

*ข้อมูลที่อยู่ในไฟล์เวิร์ดต้องแบ่งเนื้อหาแต่ละส่วนด้วยการเคาะ new line 2 ครั้ง
***
การตั้งค่าไลน์บอท (กรณียังไม่มีบัญชีบอทให้สร้างขึ้นมาก่อน):

1. ไปที่ https://manager.line.biz/ เลือกตัว Linebot ที่ต้องการ > เลือกเมนูตั้งค่า (รูปเฟืองที่ด้านขวาบน)
2. ตั้งค่า Response setting เป็น webhook หรือ chat และ webhook
3. ตั้งค่า Chat response method เป็น Manual
4. ไปที่ https://developers.line.biz/console/ แล้วเลือกบอทที่ต้องการ ตั้งค่า Messaging API โดยนำ URL ของ web app ที่ได้ Host ไว้ + '/callback' มาใส่ในช่อง webhook แล้วกด verify
