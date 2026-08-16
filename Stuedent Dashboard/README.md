# 🎓 Student Performance Dashboard (Streamlit + Plotly)

## Kaise chalaye (How to run)

1. Is folder ko kahin bhi extract/rakho — `app.py`, `requirements.txt`, aur `student_performance.csv` teeno **same folder** me hone chahiye.
2. Terminal me is folder me jaakar ye commands chalao:

```bash
pip install -r requirements.txt
streamlit run app.py
```

3. Browser automatically khul jayega `http://localhost:8501` pe — agar nahi khule to manually us link ko open kar lena.

## Dashboard me kya hai

- **Sidebar Filters**: Grade (multi-select), Weekly Study Hours, Attendance %, Class Participation, Total Score — sab range sliders ke saath.
- **KPI Cards**: Total students, avg score, avg study hours, avg attendance, avg participation — filters ke hisaab se live update hote hain.
- **Charts**:
  - Grade distribution (donut)
  - Total score distribution (histogram)
  - Study hours vs score (scatter, grade-wise color)
  - Attendance vs score (scatter, grade-wise color)
  - Avg score by study-hours group (bar)
  - Avg score by attendance group (bar)
  - Correlation heatmap
  - Score spread by grade (box plot)
- **Data table + CSV download** of filtered data at the bottom.
- **Speed mode** toggle in sidebar — dataset 10 lakh (1M) rows ka hai, isliye charts ke liye 50k sample use hota hai speed ke liye (KPIs hamesha full filtered data pe based hote hain). Chaho to isse off bhi kar sakte ho.

## Dark theme

Custom CSS diya gaya hai jo purple/cyan/pink gradient accents ke saath deep dark background deta hai — cards pe hover glow bhi hai.
