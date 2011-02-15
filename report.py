#!/usr/bin/env python
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm

c = canvas.Canvas("hello.pdf",pagesize=pagesizes.landscape(letter))
for x in range(0,11,1):
    for y in range(0,9,1): 
        c.drawString(x*inch,y*inch,"%d,%d" % (x,y))

c.showPage()
c.save()
