#!/usr/bin/env python
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm,cm
from optparse import OptionParser
import sys
import os
import subprocess
import math

def report_image_as_pdf(imagename,left_start,hspread,lane_vert_pos,num_lanes,lanenames,flip,show_grid,bench_mark_x,fudge,shift_marker,scale_marker):
    image_name = imagename
    lanenames = lanenames
    left_start = float(left_start)
    num_lanes = int(num_lanes)
    hspread = float(hspread)
    lane_vert_pos = float(lane_vert_pos)
    image_name = os.path.splitext(imagename)[0]
    bench_mark_x = float(bench_mark_x)
    fudge = list(fudge)
    shift_marker = float(shift_marker)
    scale_marker = float(scale_marker)
    c = canvas.Canvas("{image_name}_report.pdf".format(image_name=image_name),pagesize=pagesizes.landscape(letter))
    c.setTitle("{image_name}_report.pdf".format(image_name=image_name))     

    if show_grid:
        for lx in range(11):
            for ly in range(9):
                c.drawString(lx*inch,ly*inch, "%d,%d" % (lx,ly))
                
    if flip:
        c.translate(11*inch, 0)
        c.scale(-1.0, 1.0)
        
        c.drawImage("{image_name}.png".format(image_name=image_name),2*inch,2.5*inch,width=7*inch,height=5*inch)

        c.translate(11*inch, 0)
        c.scale(-1.0, 1.0)
    else:
        c.drawImage("{image_name}.png".format(image_name=image_name),2*inch,2.5*inch,width=7*inch,height=5*inch)
        
    for lane_number in range(1,num_lanes + 1, 1):
        c.drawString((left_start + lane_number * hspread)*inch,lane_vert_pos*inch,u"%s" % (str(lane_number)))

    # Putting the legend on the canvas
    for i in range(num_lanes):
        left_pos_x = 2*inch
        laneinfo_spread = 2.0*inch/(num_lanes/2)
        lane_index = i
        if i >=  num_lanes/2:
            left_pos_x = 5.0*inch
            i = i - num_lanes/2
        try:
            c.drawString(left_pos_x , (2*inch - i*laneinfo_spread),u"Lane %d : %s" % (lane_index+1 , lanenames[lane_index].strip()))
        except IndexError:
            print "Too many lanes in lane names array"
            

    bench_mark_y_positions =[6.6,6.45,6.23,6.00,5.50,5.0,4.2,3.9]
    bench_mark_values=[200,150,100,75,50,37,25,20]
    c.setFont('Helvetica', 6)
    for i,j in enumerate(bench_mark_values):
        xpos = bench_mark_x
        #ypos = (math.log10(j*1e3) - 3.333)/0.11
        ypos = bench_mark_y_positions[i]
        print "YPOS %d" % j , ypos
        c.drawString(bench_mark_x*inch,(shift_marker+ypos)*scale_marker*inch,"%s" % j)
        
    c.showPage()
    c.save()
    subprocess.call(["evince" , "{image_name}_report.pdf".format(image_name=image_name)])
    

if __name__=="__main__":

        
    p = OptionParser()
    p.add_option("--png" ,"-p", dest="pngimage", metavar = "*.png", help="png image to annotate")
    p.add_option("--gap","-g", dest="hspread",help="The gap between gel lanes",metavar="0.46",default=0.46)
    p.add_option("--numlanes", "-n", dest="numlanes",metavar="12",default=12)
    p.add_option("--legend","-l",dest="lanenames",help="lane names as csv",default=",".join([("Lane %s Label") % i for i in range(1,12,1)]))
    p.add_option("--margin" , "-m" , dest="left_start", help="left hand margin",metavar="2.12", default = 2.12)
    p.add_option("--flip","-f",action="store_true",dest ="flip")
    p.add_option("--top_pos" , "-t",dest="lane_vert_pos",help="lanelabel pos",metavar="6.7",default=6.7)
    p.add_option("--show_grid" ,"-r", dest="show_grid",help="overlay grid for planning layout" , action="store_true")
    p.add_option("--bench_mark_x" , "-b" , dest="bench_mark_x")
    p.add_option("--fudge","-u",dest="fudge", metavar="[6.6,6.45,6.23,6.00,5.50,5.0,4.2,3.9]",default="[6.6,6.45,6.23,6.00,5.50,5.0,4.2,3.9]",help="fudge factor for mwt labels")
    p.add_option("--shift_marker",dest="shift_marker", default=0, metavar="0")
    p.add_option("--scale_marker", dest="scale_marker", default=1 , metavar="0")
    options,args = None,None
    if (len(sys.argv) == 1):
        p.print_help()
        exit()
    try:
        options,args = p.parse_args()
        print options
        report_image_as_pdf(options.pngimage ,options.left_start,options.hspread,options.lane_vert_pos,options.numlanes,options.lanenames.split(","),options.flip,options.show_grid,options.bench_mark_x,options.fudge,options.shift_marker, options.scale_marker)
    except Exception as e:
        print e
        p.print_help()
