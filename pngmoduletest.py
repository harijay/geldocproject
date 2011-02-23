#!/usr/bin/env python
import png

p = png.Reader("12_1_10_good_timecourse_6a_10a_6b_10b_proc.png")
w = png.Writer(width=800,height=600,bitdepth=8)
f = open("12_1_10_good_timecourse_6a_10a_6b_10b_pngmod_rgbA8.png","wb")
w.write(f,p.asRGB8()[2])
f.close()
