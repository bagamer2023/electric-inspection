app.post('/submit-inspection', upload.fields([
  { name: 'inspection_photos', maxCount: 10 },
  { name: 'speedtest_photo', maxCount: 1 }
]), (req, res) => {
  const body = req.body || {};
  const files = req.files || {};

  // คำนวณสัปดาห์จากวันที่
  let week = 0;
  const dateNum = parseInt(body.date);
  if (dateNum >= 1 && dateNum <= 7) week = 1;
  else if (dateNum >= 8 && dateNum <= 15) week = 2;
  else if (dateNum >= 16 && dateNum <= 22) week = 3;
  else if (dateNum >= 23 && dateNum <= 31) week = 4;

  // อัปเดต inspection_plan.json
  if (body.location && body.month && week) {
    const planPath = path.join(PUBLIC_DIR, 'inspection_plan.json');
    try {
      const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
      plan.forEach(item => {
        if (item.location === body.location || item.location.includes(body.location)) {
          item.inspections.forEach(i => {
            if (i.month === body.month && i.week === week) {
              i.status = 'ตรวจแล้ว';
            }
          });
        }
      });
      fs.writeFileSync(planPath, JSON.stringify(plan, null, 2));
    } catch (e) {
      console.error("ไม่สามารถอัปเดต inspection_plan.json:", e);
    }
  }

  // บันทึก submission ตามปกติ...
});
const express = require('express');
 const fs = require('fs');
 const path = require('path');
 const app = express();
 const PUBLIC_DIR = path.join(__dirname, 'public');

 app.use(express.static(PUBLIC_DIR));
 app.use(express.json());

 app.get('/get-inspection-plan', (req, res) => {
   const planPath = path.join(PUBLIC_DIR, 'inspection_plan.json');
   try {
     const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
     res.json(plan);
   } catch (e) {
     res.status(500).json({ error: 'ไม่สามารถอ่านไฟล์ inspection_plan.json' });
   }
 });