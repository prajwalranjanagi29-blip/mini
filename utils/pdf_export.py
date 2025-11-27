from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

def export_moods_to_pdf(csv_file, pdf_file):
    df = pd.read_csv(csv_file)
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Mood Tracker Report")

    c.setFont("Helvetica", 12)
    y = height - 80
    for idx, row in df.iterrows():
        text = f"{row['timestamp']} → {row['mood']}"
        c.drawString(50, y, text)
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50

    c.save()
    return pdf_file
