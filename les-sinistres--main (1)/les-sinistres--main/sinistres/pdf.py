from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from datetime import date, datetime
import matplotlib.pyplot as plt

width, height = A4
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER

def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y
def pdf(nom,villef,date1f,caf,pivotf,cff,x):
    ca = Paragraph('''<b>Chiffre d'Affaire journalier (en €)</b>''', styleBH)
    pivot = Paragraph('''<b>Pivôt (en mm)</b>''', styleBH)
    ville = Paragraph('''<b>Ville de souscription</b>''', styleBH)
    date1 = Paragraph('''<b>Date de début de contrat</b>''', styleBH)
    
    dc = Paragraph('''<b>Durée de contrat (en jours) </b>''', styleBH)
    cf = Paragraph('''<b>Coûts fixes journalier (en€) </b>''', styleBH)
    
    
    # Texts
    a = Paragraph(str(caf), styleN)
    b = Paragraph(str(pivotf), styleN)
    c = Paragraph(villef, styleN)
    d = Paragraph(date1f.strftime("%d/%m/%Y"), styleN)
    f = Paragraph('52.00', styleN)
    j = Paragraph(str(cff), styleN)
   

  
    f = Paragraph(str(365), styleN)
    data= [[ca, a],
    [cf, j],[pivot, b],[ville, c],[date1, d],[dc, f]]

    table = Table(data, colWidths=[6 * cm, 4 * cm])

    table.setStyle(TableStyle([
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    t=nom+".pdf"
    c = canvas.Canvas(t, pagesize=A4)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)
    c.drawImage('logo1.png', 30, 750, width=150 , height=90)
    c.drawString(30, 730, 'Les sinistres')
    c.drawString(30, 715, '930 Rte des Colles')
    c.drawString(30, 695, '06410 Biot')
    datec = datetime.now().strftime("%d/%m/%Y")
    c.drawString(500, 730, datec)
    c.line(480, 727, 560, 727)
    c.drawString(30, 655, 'Devis : Couverture contre les risques de pluies')
    c.drawString(30, 610, 'Client:')
    c.line(120, 607, 560, 607)
    c.drawString(120, 610, nom)
    table.wrapOn(c, width, height)
    table.drawOn(c, *coord(5, 13, cm))

    c.drawString(275, 380, 'Prime proposée:')
    c.drawString(500, 380, str(x)+" euro")
    c.line(378, 377, 580, 377)
    c.drawString(275, 350, 'Signature:')

    c.save()

