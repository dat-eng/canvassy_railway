# 🗳️ FieldIntel – Canvassing Map MVP

A simple mobile-friendly map app to visualize voter data (Red/Blue/Undecided) and help prioritize door knocking.

---

## 🚀 What This App Does

- Plots addresses from an Excel file on a map  
- Colors:
  - 🔵 Democrat (D)
  - 🔴 Republican (R)
  - ⚪ Undecided (U)
- Works on laptop **and phone (same WiFi)**
- Helps identify high-priority areas for canvassing

---

## 🧾 Input Data Format (Excel)

Create a file called `data.xlsx` with the following columns:

| Address       | City   | State | Party |
|--------------|--------|-------|-------|
| 123 Main St  | Nashua | NH    | D     |
| 45 Elm St    | Nashua | NH    | R     |
| 78 Oak Ave   | Nashua | NH    | U     |

---

## 💻 Setup Instructions (Mac)

### 1. Create Project Folder

```bash
mkdir canvassing-app
cd canvassing-app
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install streamlit folium pandas geopy streamlit-folium openpyxl
```

### 4. Add Files

Place these in the folder:
	•	app.py → main application code
	•	data.xlsx → your voter data

## ▶️ Run the App

```bash
streamlit run app.py
```

You will see:

Local URL: http://localhost:8501  
Network URL: http://192.168.x.x:8501

## 📱 Access on Phone
	•	Make sure laptop and phone are on the same WiFi
	•	Open browser on phone
	•	Enter:
http://192.168.x.x:8501

🧠 Features (MVP)
	•	Interactive map
	•	Party-based filtering
	•	Clickable address markers
	•	Mobile-friendly UI

