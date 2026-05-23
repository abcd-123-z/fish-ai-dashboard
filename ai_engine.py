import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json
import sys
import re

# ===== รับคำถาม =====

question = sys.argv[1]

# ===== อ่าน CSV =====

url = "https://docs.google.com/spreadsheets/d/1dRyT0iPaTrrxnfon_TEqO6rcdZSSHGwUGZG-H0KjZYQ/gviz/tq?tqx=out:csv"

df = pd.read_csv(url)

# ===== แปลงข้อมูล =====

temps = pd.to_numeric(
    df.iloc[:, 2],
    errors='coerce'
).dropna().values

phs = pd.to_numeric(
    df.iloc[:, 3],
    errors='coerce'
).dropna().values

# ===== ตรวจข้อมูล =====

if len(temps) < 2 or len(phs) < 2:

    print(json.dumps({
        "result": "ข้อมูลยังไม่เพียงพอ"
    }))

    sys.exit()

# ===== สร้างแกนเวลา =====

X = np.arange(len(temps)).reshape(-1, 1)

# ===== Train Temp =====

model = LinearRegression()
model.fit(X, temps)

# ===== Train PH =====

ph_model = LinearRegression()
ph_model.fit(X, phs)

# ===== ค่าปัจจุบัน =====

current_temp = round(temps[-1], 2)
current_ph = round(phs[-1], 2)

# ===== AI Logic =====

answer = "ผมยังวิเคราะห์ไม่ได้"

# ===== ตรวจจับตัวเลข =====

match = re.search(r'(\d+)', question)

if match:

    hours = int(match.group(1))

    future_index = len(temps) + hours

    # ===== Predict Temp =====

    prediction = model.predict([[future_index]])
    future_temp = round(prediction[0], 2)

    # ===== Predict PH =====

    ph_prediction = ph_model.predict([[future_index]])
    future_ph = round(ph_prediction[0], 2)

    # ===== ตอบ =====

    if "อุณหภูมิ" in question:

        answer = f"คาดว่าอีก {hours} ชั่วโมง อุณหภูมิจะอยู่ประมาณ {future_temp} °C"

    elif "ph" in question.lower():

        answer = f"คาดว่าอีก {hours} ชั่วโมง ค่า pH จะอยู่ประมาณ {future_ph}"

    else:

        answer = f"อีก {hours} ชั่วโมง อุณหภูมิประมาณ {future_temp} °C และค่า pH ประมาณ {future_ph}"

# ===== อุณหภูมิปัจจุบัน =====

elif "อุณหภูมิ" in question:

    answer = f"อุณหภูมิปัจจุบันคือ {current_temp} °C"

# ===== PH ปัจจุบัน =====

elif "ph" in question.lower():

    answer = f"ค่า pH ปัจจุบันคือ {current_ph}"

# ===== แนวโน้ม =====

elif "แนวโน้ม" in question:

    if temps[-1] > temps[0]:

        answer = "อุณหภูมิมีแนวโน้มสูงขึ้น"

    else:

        answer = "อุณหภูมิมีแนวโน้มลดลง"

# ===== ส่งกลับ =====

print(json.dumps({
    "result": answer
}))