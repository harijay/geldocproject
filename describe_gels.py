#!/usr/bin/env python
import sys
import os
import PIL
import Image

from optparse import OptionParser
p = OptionParser()
p.add_option("-d" , "--dir",dest="tif_source_dir",metavar="tif source_directory",default="/home/W.hari/OutQueue")
global_options, spillover = None,None


if __name__=="__main__" :
    if len(sys.argv) == 1:
        p.print_help()
    global_options,spillover = p.parse_args()
    try:
        print "Walking through {dirtowalk}".format(dirtowalk = global_options.tif_source_dir)
        for path,dirs,files in os.walk(global_options.tif_source_dir):
            for afile in files:
                if "tif" in os.path.abspath(afile):
                    print "Processing {afile}".format(afile=afile)
                    im = Image.open(os.path.join( global_options.tif_source_dir,afile))
                    print im.mode
                    print im.size
                    im2 =  im.convert("I")
                    print im2.mode
                    out = im2.resize([int(0.5 *s) for s in im2.size],Image.ANTIALIAS)
                    out.save(os.path.splitext(afile)[0] + "_proc.png")                         
                    
    except Exception as e:
        print e
        p.print_help()



