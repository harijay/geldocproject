#!/usr/bin/env python
import sys
import os
import Image
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch,mm
import png

from optparse import OptionParser
p = OptionParser()
p.add_option("-d" , "--dir",dest="tif_source_dir",metavar="tif source_directory")
global_options, spillover = None,None
p.add_option("-i","--image",dest="pngimage",metavar="file.png", help="image for 16 bit png to 8 bit png")
p.add_option("-s","--single",dest="singletif",metavar="single tif image")

def make_rgb8from_16bit_tif(filename):
    try:
        print "Processing {afile}".format(afile=filename)
        im = Image.open(filename)
        dpi = im.info["dpi"]
        print "Input mode:" , im.mode
        print "Input size:", im.size
        print "Input  dpi:" ,dpi
        im2 =  im.convert("I")
        print "Output mode1:",im2.mode
      # out = im2.resize([int(0.5 *s) for s in im2.size],Image.ANTIALIAS)
        out = im2.resize([800,600],Image.ANTIALIAS)
        out.save(os.path.splitext(filename)[0] + "_proc.png")
        png_object = png.Reader(os.path.splitext(filename)[0] + "_proc.png")
        png_object_writer = png.Writer(width=800,height=600,bitdepth=8)
        outfile_fin = open((os.path.splitext(filename)[0] + "rgb8.png"),"wb")
        png_object_writer.write(outfile_fin,png_object.asRGB8()[2])
        outfile_fin.close()
    except Exception as e:
        print "Error during rgba8 from tif",e
        
    
if __name__=="__main__" :
    if len(sys.argv) == 1:
        p.print_help()
    global_options,spillover = p.parse_args()
    
    if global_options.tif_source_dir is not None:
        try:
            print "Walking through {dirtowalk}".format(dirtowalk = global_options.tif_source_dir)
            for path,dirs,files in os.walk(global_options.tif_source_dir):
                for afile in files:
                    if "tif" in os.path.abspath(afile):
                        print "Processing {afile}".format(afile=afile)
                        im = Image.open(os.path.join( global_options.tif_source_dir,afile))
                        dpi = im.info["dpi"]
                        print im.mode
                        print im.size
                        print dpi
                        im2 =  im.convert("I")
                        print im2.mode
                        out = im2.resize([int(0.5 *s) for s in im2.size],Image.ANTIALIAS)
                        out.save(os.path.splitext(afile)[0] + "_proc.png")
                        png_object = png.Reader(os.path.splitext(afile)[0] + "_proc.png")
                        png_object_writer = png.Writer(width=800,height=600,bitdepth=8)
                        outfile_fin = open((os.path.splitext(afile)[0] + "rgb8.png"),"wb")
                        png_object_writer.write(outfile_fin,png_object.asRGB8()[2])
                        outfile_fin.close()
#                    c = canvas.Canvas(os.path.splitext(afile)[0] + "_pdf.pdf")

        except Exception as e:
            print e
            p.print_help()

    if global_options.pngimage is not None:
        
        try:
            png_reader = png.Reader(global_options.pngimage)
            png_object_writer = png.Writer(width=800,height=600,bitdepth=8)
            outfile_fin = open((os.path.splitext(global_options.pngimage)[0] + "rgb8.png"),"wb")
            png_object_writer.write(outfile_fin,png_reader.asRGB8()[2])
            outfile_fin.close()
        except Exception as e:
            e

    if global_options.singletif is not None:
        make_rgb8from_16bit_tif(global_options.singletif)
        

