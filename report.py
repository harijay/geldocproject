#!/usr/bin/env python
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm
from optparse import OptionParser
import sys



def report_image_as_pdf(imagename,left_start,hspread,lane_vert_pos,num_lanes,lanenames,flip):
    image_name = imagename
    lanenames = lanenames
    left_start = float(left_start)
    num_lanes = int(num_lanes)
    hspread = float(hspread)
    lane_vert_pos = float(lane_vert_pos)
    
    print lanenames
    c = canvas.Canvas("hello{image_name}.pdf".format(image_name=image_name),pagesize=pagesizes.landscape(letter))
#    for x in range(0,11,1):
#        for y in range(0,9,1): 
#            c.drawString(x*inch,y*inch,"%d,%d" % (x,y))
            
    lane_label_xspread = (7 -(hspread))/num_lanes
    
    if flip:
        c.translate(11*inch, 0)
        c.scale(-1.0, 1.0)
        
        c.drawImage("{image_name}.png".format(image_name=image_name),2*inch,2.5*inch,width=7*inch,height=5*inch)

        c.translate(11*inch, 0)
        c.scale(-1.0, 1.0)
    else:
        c.drawImage("{image_name}.png".format(image_name=image_name),2*inch,2.5*inch,width=7*inch,height=5*inch)
        
    for lane_number in range(1,num_lanes + 1, 1):
        c.drawString((left_start + lane_number * lane_label_xspread)*inch,lane_vert_pos*inch,u"%s" % (str(lane_number)))

    for i in range(num_lanes):
        left_pos_x = 2*inch
        laneinfo_spread = 2.0*inch/(num_lanes/2)
        print laneinfo_spread
        lane_index = i
        if i >=  num_lanes/2:
            left_pos_x = 5.0*inch
            i = i - num_lanes/2
            
        try:
            print "Lane infor for", i
            print "LEFT",left_pos_x ,"RIGHT", 2 - i*laneinfo_spread
            c.drawString(left_pos_x , (2*inch - i*laneinfo_spread),u"Lane %d : %s" % (lane_index+1 , lanenames[lane_index].strip()))
        except IndexError:
            print "ERREUEUEU"
            
    c.showPage()
    c.save()
    

if __name__=="__main__":

        
    p = OptionParser()
    p.add_option("--png" ,"-p", dest="pngimage", metavar = "*.png", help="png image to annotate")
    p.add_option("--hspread","-w", dest="hspread",help="distance between lane labels default 1.52 inches",default=1.52)
    p.add_option("--numlanes", "-n", dest="numlanes",metavar="Number of lanes",default=12)
    p.add_option("--lanenames","-s",dest="lanenames",help="lane names as csv",default=["Lane %s Label" % i for i in range(1,13,1)])
    p.add_option("--left_start" , "-b" , dest="left_start", help="gap before labels", default = 2.12)
    p.add_option("--flip","-f",action="store_true",dest ="flip")
    p.add_option("--top_pos" , "-t",dest="lane_vert_pos",metavar="Lane vert pos[6.7]",default=6.7)
    options,args = None,None
    if (len(sys.argv) == 1):
        p.print_help()
        exit()
    try:
        options,args = p.parse_args()
        print options
        report_image_as_pdf(options.pngimage ,options.left_start,options.hspread,options.lane_vert_pos,options.numlanes,options.lanenames.split(","),options.flip)
    except Exception as e:
        print e
        p.print_help()
