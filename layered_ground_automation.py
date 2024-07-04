# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 12:48:18 2022

@author: adwh
"""

from resipy import meshTools
from resipy import Project
import pandas as pd
from math import tan
from math import e
import numpy as np
import os
import os.path
import glob
import os,subprocess
import matplotlib.pyplot as plt
import matplotlib as mpl

def mesh_creation(model,elec):
    #create mesh for a specific geometry and electrode spacing
    ewd='C:/Users/adwh/Anaconda3/lib/site-packages/resipy/exe' #where gmsh lives

    #model variable for iteration
    cw=model['crest_width']
    cot=model['slope_angle']
    h=model['height'] #not currently used
    z=model['foundation_height']
    elec_x=elec[:,0].tolist()
    
    #find or create mesh
    geometry=f'cw{cw}_cot{cot}'
    mesh_path=f'1_fm_meshes/{geometry}'
    mesh_name=f'1_fm_meshes/{geometry}.geo'
    if os.path.exists(mesh_name)==False:
        create_geo(fname=mesh_path,electrodes=elec_x,h=h,z=z,cw=cw,slope_angle=cot)
        create_mesh(ewd=ewd, fname=mesh_path)
        create_advanced_mesh(fname=mesh_path,geometry=geometry,electrodes=elec)
        print(f'File {mesh_name} .geo .msh and advanced mesh created')
    
    #check mesh3d.dat file
    with open('temp/mesh3d_geometry.txt', 'r') as file:
        current_geometry = file.read()
    print(current_geometry)

    if current_geometry!=geometry:
        create_advanced_mesh(fname=mesh_path,geometry=geometry,electrodes=elec)
        print(f'File {mesh_name} .geo .msh and advanced mesh created')
        


def create_geo(fname,electrodes,h,z,cw,slope_angle):
    #%%
    # Lmax=max(electrodes)
    # Lmin=min(electrodes)
    # L=Lmax-Lmin
    # bw=cw+2*slope_angle*h #base width of the embankemnt
    
    # #electrode spacings
    # elec_spacing_min=(1)
    # elec_spacing_max=(16)
    
    # #ratios for placing inner and outer mesh coordinates in terms of survey lenght
    # ixr=1/4 #innerzone x e.g 0.25 is  0.25 of L
    # izr=1/2 #innerzone z
    # out_z=10 #outerzone
    
    # #inner mesh region coordinates
    # ixmin=Lmin-L*ixr/2 #inner mesh region minimum x
    # ixmax=Lmax+L*ixr #inner mesh region max x
    # iy=50*6 #inner mesh region minimum y 11 is the max bw for cw=5 cot=3
    # iz=-iy#innder mesh region depth
    
    # #high res region
    # hrmin=-10
    # hrmax=104
    
    # #outer mesh  coordinates
    # oxmin=Lmin-L*out_z #outerzone smallets x
    # oxmax=Lmax+L*out_z #outerxone largest x
    # oy=L*out_z # outerzone y either side of line a y=0
    # oz=-L*out_z #depth depth of outerzone
    
    
    
    # #cell lengths electrodes
    # cl_elec=10 #number of cells between adjacent electrodes
    # cl_elec_sp_min=round((elec_spacing_min/cl_elec),3)
    # cl_elec_sp_max=round((elec_spacing_max/(cl_elec)),3)
    
    # #cell length outer zone
    # clo=elec_spacing_max*40 #outerzone cell length
    
    # #cell length outer zone
    # cliu_xmin=12 #cell length top of inner zone x=min
    # cliu_xmax=24 #cell length top of inner zone  x=max
    # clil_xmin=36 #cell length bottom of inner zone  x=min
    # clil_xmax=72 #cell length bottom of inner zone x=max
    
    # #cell lengths embankment
    
    # cl_ec_xmin=(cl_elec_sp_min*3+cw/(cl_elec*2/3))#inner zone left crest
    # cl_ec_xmax=(cl_elec_sp_max*2+cw/(cl_elec*2/3)) #inner zone right crest
    
    # cl_ec_hr=cl_elec_sp_min+cw/(cl_elec*2) #high res zone
    # cl_eb_hr=0.9 #0.15*e**(0.5*elec_spacing_min)*6 #high res zone
    
    # cl_eb_xmin=2 #0.1*e**(0.5*elec_spacing_min)*6 #inner zone left crest
    # # cl_eb_xmax=5 #0.15*e**(0.5*elec_spacing_max)*6 #inner zone right crest
    
    
    #%%
    #survey length
    Lmax=max(electrodes)
    Lmin=min(electrodes)
    L=Lmax-Lmin
    bw=cw+2*slope_angle*h #base width of the embankemnt
    
    #electrode spacings
    elec_spacing_min=(1)
    elec_spacing_max=(16)
    
    #ratios for placing inner and outer mesh coordinates in terms of survey lenght
    ixr=1/4 #innerzone x e.g 0.25 is  0.25 of L
    izr=1/2 #innerzone z
    out_z=10 #outerzone
    
    #inner mesh region coordinates
    ixmin=Lmin-L*ixr/2 #inner mesh region minimum x
    ixmax=Lmax+L*ixr #inner mesh region max x
    iy=50*6 #inner mesh region minimum y 11 is the max bw for cw=5 cot=3
    iz=-iy#innder mesh region depth
    
    #high res region
    hrmin=-10
    hrmax=104
    
    #outer mesh  coordinates
    oxmin=Lmin-L*out_z #outerzone smallets x
    oxmax=Lmax+L*out_z #outerxone largest x
    oy=L*out_z # outerzone y either side of line a y=0
    oz=-L*out_z #depth depth of outerzone
    
    
    
    #cell lengths electrodes
    cl_elec=7 #number of cells between adjacent electrodes
    cl_elec_sp_min=round((elec_spacing_min/cl_elec),3)
    cl_elec_sp_max=round((elec_spacing_max/(cl_elec)),3)
    
    #cell length outer zone
    clo=elec_spacing_max*60 #outerzone cell length
    
    #cell length outer zone
    cliu_xmin=15 #cell length top of inner zone x=min
    cliu_xmax=30 #cell length top of inner zone  x=max
    clil_xmin=40 #cell length bottom of inner zone  x=min
    clil_xmax=100 #cell length bottom of inner zone x=max
    
    #cell lengths embankment
    
    cl_ec_xmin=(cl_elec_sp_min*3+cw/(cl_elec*2/3))#inner zone left crest
    cl_ec_xmax=(cl_elec_sp_max*2+cw/(cl_elec*2/3)) #inner zone right crest
    
    cl_ec_hr=cl_elec_sp_min+cw/(cl_elec*2) #high res zone
    cl_eb_hr=1.2 #0.15*e**(0.5*elec_spacing_min)*6 #high res zone
    
    cl_eb_xmin=3 #0.1*e**(0.5*elec_spacing_min)*6 #inner zone left crest
    cl_eb_xmax=10 #0.15*e**(0.5*elec_spacing_max)*6 #inner zone right crest
    
   


    
    print('Creating .geo file')
    with open(fname+'.geo', 'w') as f:
        f.write(
            '\n//Embankment outzone left\n'
            f'Point(1)={{{oxmin}, {-bw/2}, {z}, {clo}}};\n'
            f'Point(2)={{{oxmin}, {-cw/2}, {h}, {clo}}};\n'
            f'Point(3)={{{oxmin}, {cw/2}, {h}, {clo}}};\n'
            f'Point(4)={{{oxmin}, {bw/2}, {z}, {clo}}};\n'
            'Line(1) = {1, 2};\n'
            'Line(2) = {2, 3};\n'
            'Line(3) = {3, 4};\n'
            'Line(4) = {4, 1};\n\n'
            
            '//Embankment inner zone left\n'
            f'Point(5)={{{ixmin}, {-bw/2}, {z}, {cl_eb_xmin}}};\n'
            f'Point(6)={{{ixmin}, {-cw/2}, {h}, {cl_ec_xmin}}};\n'
            f'Point(7)={{{ixmin}, {cw/2}, {h}, {cl_ec_xmin}}};\n'
            f'Point(8)={{{ixmin}, {bw/2}, {z}, {cl_eb_xmin}}};\n'
            'Line(5) = {5, 6};\n'
            'Line(6) = {6, 7};\n'
            'Line(7) = {7, 8};\n'
            'Line(8) = {8, 5};\n\n'
            
            '//Embankment high res zone left\n'
            f'Point(50)={{{hrmin}, {-bw/2}, {z}, {cl_eb_hr}}};\n'
            f'Point(51)={{{hrmin}, {-cw/2}, {h}, {cl_ec_hr}}};\n'
            f'Point(52)={{{hrmin}, {cw/2}, {h}, {cl_ec_hr}}};\n'
            f'Point(53)={{{hrmin}, {bw/2}, {z}, {cl_eb_hr}}};\n\n'
                        
            '//Embankment high res zone right\n'
            f'Point(54)={{{hrmax}, {-bw/2}, {z}, {cl_eb_hr}}};\n'
            f'Point(55)={{{hrmax}, {-cw/2}, {h}, {cl_ec_hr}}};\n'
            f'Point(56)={{{hrmax}, {cw/2}, {h}, {cl_ec_hr}}};\n'
            f'Point(57)={{{hrmax}, {bw/2}, {z}, {cl_eb_hr}}};\n\n'
            
            '//Embankment inner zone right\n'
            f'Point(9)={{{ixmax}, {-bw/2}, {z}, {cl_eb_xmax}}};\n'
            f'Point(10)={{{ixmax}, {-cw/2}, {h}, {cl_ec_xmax}}};\n'
            f'Point(11)={{{ixmax}, {cw/2}, {h}, {cl_ec_xmax}}};\n'
            f'Point(12)={{{ixmax}, {bw/2}, {z}, {cl_eb_xmax}}};\n'
            'Line(9) = {9, 10};\n'
            'Line(10) = {10, 11};\n'
            'Line(11) = {11, 12};\n'
            'Line(12) = {12, 9};\n\n'
            
            
            '//Embankment outer right\n'
            f'Point(13)={{{oxmax}, {-bw/2}, {z}, {clo}}};\n'
            f'Point(14)={{{oxmax}, {-cw/2}, {h}, {clo}}};\n'
            f'Point(15)={{{oxmax}, {cw/2}, {h}, {clo}}};\n'
            f'Point(16)={{{oxmax}, {bw/2}, {z}, {clo}}};\n'
            'Line(13) = {13, 14};\n'
            'Line(14) = {14, 15};\n'
            'Line(15) = {15, 16};\n'
            'Line(16) = {16, 13};\n\n'
            
            '//create left embankment lines\n'
            'Line(17) = {1, 5};\n'
            'Line(18) = {2, 6};\n'
            'Line(19) = {3, 7};\n'
            'Line(20) = {4, 8};\n\n'
            
            '// create central embankment\n'
            'Line(21) = {8, 53};\n'
            'Line(60) = {53, 57};\n'
            'Line(61) = {57, 12};\n'
            'Line(22) = {7, 52};\n'
            'Line(62) = {52, 56};\n'
            'Line(63) = {56, 11};\n'
            'Line(23) = {6, 51};\n'
            'Line(64) = {51, 55};\n'
            'Line(65) = {55, 10};\n'
            'Line(24) = {5, 50};\n'
            'Line(66) = {50, 54};\n'
            'Line(67) = {54, 9};\n\n'
            
            '//create right embankment\n'
            'Line(25) = {12, 16};\n'
            'Line(26) = {11, 15};\n'
            'Line(27) = {10, 14};\n'
            'Line(28) = {9, 13};\n\n'
            
            '// electrodes on embankment\n'
            )
        
        for i,elec in enumerate(electrodes):
           
            dif=round((1/cl_elec),3)
            
            i+=100
            f.write(f'Point({i})={{{elec}, 0, {h}, {dif}}};\n')
            
        f.write(
            '\n//Inner zone points and lines\n'
            f'Point(17)={{{ixmin}, {iy}, {z}, {cliu_xmin}}};\n'
            f'Point(18)={{{ixmax}, {iy}, {z}, {cliu_xmax}}};\n'
            f'Point(19)={{{ixmax}, {-iy}, {z}, {cliu_xmax}}};\n'
            f'Point(20)={{{ixmin}, {-iy}, {z}, {cliu_xmin}}};\n'
            f'Point(21)={{{ixmin}, {iy}, {iz}, {clil_xmin}}};\n'
            f'Point(22)={{{ixmax}, {iy}, {iz}, {clil_xmax}}};\n'
            f'Point(23)={{{ixmax}, {-iy}, {iz}, {clil_xmax}}};\n'
            f'Point(24)={{{ixmin}, {-iy}, {iz}, {clil_xmin}}};\n'
            f'Point(37)={{{ixmin}, {iy}, {h}, {cliu_xmin}}};\n'
            f'Point(38)={{{ixmax}, {iy}, {h}, {cliu_xmax}}};\n'
            f'Point(39)={{{ixmax}, {-iy}, {h}, {cliu_xmax}}};\n'
            f'Point(40)={{{ixmin}, {-iy}, {h}, {cliu_xmin}}};\n'
            'Line(29) = {19, 9};\n'
            'Line(30) = {12, 18};\n'
            'Line(31) = {18, 22};\n'
            'Line(32) = {22, 23};\n'
            'Line(33) = {23, 19};\n'
            'Line(34) = {19, 20};\n'
            'Line(35) = {20, 24};\n'
            'Line(36) = {24, 21};\n'
            'Line(37) = {21, 17};\n'
            'Line(38) = {17, 8};\n'
            'Line(39) = {5, 20};\n'
            'Line(40) = {24, 23};\n'
            'Line(41) = {22, 21};\n'
            'Line(42) = {17, 18};\n\n'
            
            
            '//Create embankment surfaces and volumes\n'
            'Curve Loop(1) = {11, 25, -15, -26};\n'
            'Plane Surface(1) = {1};\n'
            'Curve Loop(2) = {14, -26, -10, 27};\n'
            'Plane Surface(2) = {2};\n'
            'Curve Loop(3) = {9, 27, -13, -28};\n'
            'Plane Surface(3) = {3};\n'
            'Curve Loop(4) = {14, 15, 16, 13};\n'
            'Plane Surface(4) = {4};\n'
            'Curve Loop(5) = {10, 11, 12, 9};\n'
            'Plane Surface(5) = {5};\n'
            'Curve Loop(6) = {12, 28, -16, -25};\n'
            'Plane Surface(6) = {6};\n'
            'Curve Loop(7) = {21, 60, 61, 12, -24, -66, -67, -8};\n'
            'Plane Surface(7) = {7};\n'
            'Curve Loop(8) = {22, 62, 63, 11, -21, -60, -61, -7};\n'
            'Plane Surface(8) = {8};\n'
            'Curve Loop(9) = {23, 64, 65, 10, -22, -62, -63, -6};\n'
            'Plane Surface(9) = {9};\n'
            'Curve Loop(10) = {24, 66, 67, 9, -23, -64, -65, -5};\n'
            'Plane Surface(10) = {10};\n'
            'Curve Loop(11) = {8, 5, 6, 7};\n'
            'Plane Surface(11) = {11};\n'
            'Curve Loop(12) = {20, 8, -17, -4};\n'
            'Plane Surface(12) = {12};\n'
            'Curve Loop(13) = {17, 5, -18, -1};\n'
            'Plane Surface(13) = {13};\n'
            'Curve Loop(14) = {6, -19, -2, 18};\n'
            'Plane Surface(14) = {14};\n'
            'Curve Loop(15) = {19, 7, -20, -3};\n'
            'Plane Surface(15) = {15};\n'
            'Curve Loop(16) = {4, 1, 2, 3};\n'
            'Plane Surface(16) = {16};\n'
            'Surface Loop(1) = {13, 12, 15, 14, 16, 11};\n'
            'Volume(1) = {1};\n'
            'Surface Loop(2) = {10, 7, 8, 9, 11, 5};\n'
            'Volume(2) = {2};\n'
            'Surface Loop(3) = {5, 6, 3, 2, 4, 1};\n'
            'Volume(3) = {3};\n\n'
            )
        f.write(
            '\n//define points on embankment\n'
            'Point{\n')
        for i in range(len(electrodes)):
            if i==len(electrodes)-1:
                f.write(str(i+100))
            else:
                f.write(str(i+100)+', ')
        f.write('\n} In Surface{9};\n\n')
            
        f.write('//Create inner surface and volume\n'
            'Curve Loop(17) = {39, -34, 29, -24, -66, -67};\n'
            'Plane Surface(17) = {17};\n'
            'Curve Loop(18) = {38, 21, 60, 61, 30, -42};\n'
            'Plane Surface(18) = {18};\n'
            'Curve Loop(19) = {41, 37, 42, 31};\n'
            'Plane Surface(19) = {19};\n'
            'Curve Loop(20) = {38, 8, 39, 35, 36, 37};\n'
            'Plane Surface(20) = {20};\n'
            'Curve Loop(21) = {35, 40, 33, 34};\n'
            'Plane Surface(21) = {21};\n'
            'Curve Loop(22) = {29, -12, 30, 31, 32, 33};\n'
            'Plane Surface(22) = {22};\n'
            'Curve Loop(23) = {32, -40, 36, -41};\n'
            'Plane Surface(23) = {23};\n'
            'Surface Loop(4) = {21, 20, 18, 22, 17, 19, 23, 7};\n'
            'Volume(4) = {4};\n\n'
            
           '//outerzone points and lines\n'
           f'Point(25)={{{oxmin}, {oy}, {z}, {clo}}};\n'
           f'Point(26)={{{oxmax}, {oy}, {z}, {clo}}};\n'
           f'Point(27)={{{oxmax}, {-oy}, {z}, {clo}}};\n'
           f'Point(28)={{{oxmin}, {-oy}, {z}, {clo}}};\n'
           f'Point(29)={{{oxmin}, {oy}, {oz}, {clo}}};\n'
           f'Point(30)={{{oxmax}, {oy}, {oz}, {clo}}};\n'
           f'Point(31)={{{oxmax}, {-oy}, {oz}, {clo}}};\n'
           f'Point(32)={{{oxmin}, {-oy}, {oz}, {clo}}};\n'
           
           f'Point(33)={{{oxmin}, {oy}, {h}, {clo}}};\n'
           f'Point(34)={{{oxmax}, {oy}, {h}, {clo}}};\n'
           f'Point(35)={{{oxmax}, {-oy}, {h}, {clo}}};\n'
           f'Point(36)={{{oxmin}, {-oy}, {h}, {clo}}};\n'
           'Line(43) = {26, 16};\n'
           'Line(44) = {13, 27};\n'
           'Line(45) = {27, 31};\n'
           'Line(46) = {26, 30};\n'
           'Line(47) = {30, 31};\n'
           'Line(48) = {28, 32};\n'
           'Line(49) = {32, 29};\n'
           'Line(50) = {29, 25};\n'
           'Line(51) = {25, 4};\n'
           'Line(52) = {1, 28};\n'
           'Line(53) = {28, 27};\n'
           'Line(54) = {31, 32};\n'
           'Line(55) = {29, 30};\n'
           'Line(56) = {26, 25};\n\n'
            'Curve Loop(24) = {50, -56, 46, -55};\n'
            'Plane Surface(24) = {24};\n'
            'Curve Loop(25) = {55, 47, 54, 49};\n'
            'Plane Surface(25) = {25};\n'
            'Curve Loop(26) = {49, 50, 51, 4, 52, 48};\n'
            'Plane Surface(26) = {26};\n'
            'Curve Loop(27) = {48, -54, -45, -53};\n'
            'Plane Surface(27) = {27};\n'
            'Curve Loop(28) = {45, -47, -46, 43, 16, 44};\n'
            'Plane Surface(28) = {28};\n'
            'Curve Loop(29) = {25, -43, 56, 51, 20, -38, 42, -30};\n'
            'Plane Surface(29) = {29};\n'
            'Curve Loop(30) = {52, 53, -44, -28, -29, 34, -39, -17};\n'
            'Plane Surface(30) = {30};\n'
            'Surface Loop(5) = {27, 26, 25, 24, 29, 28, 30, 6, 19, 23, 22, 21, 20, 12};\n'
            'Volume(5) = {5};\n\n'
            
            
            '//Inner surface layer\n'
            'Line(68) = {20, 40};\n'
            'Line(69) = {40, 6};\n'
            'Line(70) = {40, 39};\n'
            'Line(71) = {39, 19};\n'
            'Line(72) = {39, 10};\n'
            'Line(73) = {38, 37};\n'
            'Line(75) = {37, 17};\n'
            'Line(77) = {38, 11};\n'
            'Line(78) = {38, 18};\n\n'
            
            '//Outer surface layer\n'
            'Line(79) = {35, 27};\n'
            'Line(80) = {36, 28};\n'
            'Line(81) = {2, 36};\n'
            'Line(82) = {36, 35};\n'
            'Line(83) = {35, 14};\n'
            'Line(84) = {15, 34};\n'
            'Line(85) = {26, 34};\n'
            'Line(86) = {34, 33};\n'
            'Line(87) = {33, 25};\n'
            'Line(88) = {33, 3};\n\n'
            '//\n'
            'Curve Loop(31) = {1, 81, 80, -52};\n'
            'Plane Surface(31) = {31};\n'
            'Curve Loop(32) = {82, 79, -53, -80};\n'
            'Plane Surface(32) = {32};\n'
            'Curve Loop(33) = {79, -44, 13, -83};\n'
            'Plane Surface(33) = {33};\n'
            'Curve Loop(34) = {18, -69, 70, 72, 27, -83, -82, -81};\n'
            'Plane Surface(34) = {34};\n'
            'Curve Loop(35) = {5, -69, -68, -39};\n'
            'Plane Surface(35) = {35};\n'
            'Curve Loop(36) = {70, 71, 34, 68};\n'
            'Plane Surface(36) = {36};\n'
            'Curve Loop(37) = {71, 29, 9, -72};\n'
            'Plane Surface(37) = {37};\n'
            'Curve Loop(38) = {72, -65, -64, -23, -69, 70};\n'
            'Plane Surface(38) = {38};\n'
            'Line(89) = {37, 7};\n'
            'Curve Loop(39) = {7, -38, -75, 89};\n'
            'Plane Surface(39) = {39};\n'
            'Curve Loop(40) = {75, 42, -78, 73};\n'
            'Plane Surface(40) = {40};\n'
            'Curve Loop(41) = {77, 11, 30, -78};\n'
            'Plane Surface(41) = {41};\n'
            'Curve Loop(42) = {89, 22, 62, 63, -77, 73};\n'
            'Plane Surface(42) = {42};\n'
            'Curve Loop(43) = {89, -19, -88, -86, -84, -26, -77, 73};\n'
            'Plane Surface(43) = {43};\n'
            'Curve Loop(44) = {88, 3, -51, -87};\n'
            'Plane Surface(44) = {44};\n'
            'Curve Loop(45) = {87, -56, 85, 86};\n'
            'Plane Surface(45) = {45};\n'
            'Curve Loop(46) = {84, -85, 43, -15};\n'
            'Plane Surface(46) = {46};\n'
            'Surface Loop(6) = {43, 44, 45, 46, 29, 1, 40, 39, 41, 15};\n'
            'Volume(6) = {6};\n'
            'Surface Loop(7) = {42, 18, 40, 39, 41, 8};\n'
            'Volume(7) = {7};\n'
            'Surface Loop(8) = {38, 17, 36, 37, 35, 10};\n'
            'Volume(8) = {8};\n'
            'Surface Loop(9) = {34, 33, 32, 31, 30, 35, 36, 37, 13, 3};\n'
            'Volume(9) = {9};\n'
            )
        

def create_mesh(ewd,fname):
    print('Creating .msh file')
    meshTools.runGmsh(ewd, fname, show_output=False, threed=True, handle=None)
       
def create_advanced_mesh(fname,geometry,electrodes):
    print(f'Creating advanced mesh_{geometry}')
    mesh = meshTools.readMesh(fname+'.msh')   
    electrodes=range(100,100+len(electrodes))
    mesh.setElecNode(electrodes)
    #print(mesh.showAvailAttr(flag=True))

    mesh.datAdv(file_path='R3t_layered_ground/mesh3D.dat')
    region = mesh.df['region'].values # zones in the mesh saved as region parameter in mesh dataframe 
    np.save('model_regions', region)
    
    
    mesh=mesh.threshold(attr='region', vmin=None, vmax=5)
    print(mesh.df['region'].values)
    mesh.datAdv(file_path='R3t_embankment/mesh3D.dat')
    
   
    
    ## create resistivity mesh
    #region = mesh.df['region'].values # zones in the mesh saved as region parameter in mesh dataframe 
    #np.save('model_regions_layer', region)
    path='temp/mesh3d_geometry.txt'
    
    with open(path, 'w') as f:
        f.write(f'{geometry}')
    
    return region
       
def create_folder(fname,file=None,text=''):
    try:
        os.mkdir(fname)
        print(f'Folder {fname} created')
    except:
        print(f'Folder {fname} already exists')
    if file!=None:
        if os.path.exists(f'{fname}/{file}')==False:
            with open(f'{fname}/{file}', 'w') as f:
                f.write(text)

def create_resistivity(res_contrast,model_type):
    print(f'creating resistivity file {res_contrast}')
    res_list=np.load('model_regions.npy') # list of regions for each cell.
    
    #res_contrast=round(10**res_contrast,3)
    #model type = embankment or layers
    if res_contrast<=1: 
        embankment_res=1
        foundation_res=1/res_contrast
    else:
        embankment_res=res_contrast
        foundation_res=1
    
    #Import resistiivty values for mesh
    resistivity= pd.DataFrame(index=res_list,columns=['x','y','z','res'])
    resistivity[['x','y','z']]=0
    resistivity['res']=res_list
    # volumes 1-3 embankment,4-7 volume either side of the embankment, 8-9 embankment foundation layer
    resistivity.loc[resistivity['res'].isin([1,2,3]),'res']='embankment'
    resistivity.loc[resistivity['res'].isin([4,5]),'res']='foundation'
    if model_type=='e':
        resistivity.loc[resistivity['res'].isin([6,7,8,9]),'res']='air' #low and high are inclusive
        #emplace resistivity values based on labels
        
        resistivity.loc[resistivity['res']=='embankment','res']=round(embankment_res,3)
        resistivity.loc[resistivity['res']=='foundation','res']=round(foundation_res,3)
        resistivity=resistivity[resistivity['res']!='air']#remove air values
        resistivity.to_csv('R3t_embankment/resistivity.dat',index=False,header=False)
        
    else:
        resistivity.loc[resistivity['res'].isin([6,7,8,9]),'res']='embankment' #low and high are inclusive

        #emplace resistivity values based on labels
        resistivity.loc[resistivity['res']=='embankment','res']=round(embankment_res,3)
        resistivity.loc[resistivity['res']=='foundation','res']=round(foundation_res,3)
        resistivity.to_csv('R3t_layered_ground/resistivity.dat',index=False,header=False)

def forward_model(model,res_contrast,r3t_path,model_type):
    
    cw=model['crest_width']
    cot=model['slope_angle']
    output_path=f'2_fm_results/cw{cw}_cot{cot}_res{res_contrast}_{model_type}'
    
    #folder location
    #list of electrodes x only,
    #embankment height
    #resistivity contrast between embankment and foundation
    cwd=r3t_path[:-8]    #os.system('"' + r3t_path + '"')
    process = subprocess.Popen(r3t_path, stderr=subprocess.PIPE,cwd=cwd)
    process.wait()
    if model_type=='e':
        os.rename('R3t_embankment/R3t_forward.dat', f'{output_path}.dat')
    if model_type=='l':
        os.rename('R3t_layered_ground/R3t_forward.dat', f'{output_path}.dat')
   
    
def electrodes(file_name):
    electrodes=pd.read_csv(file_name)
    elec_x_list=electrodes['x'].tolist()
    elec_x=np.array(elec_x_list)
    elec_y=np.zeros(len(elec_x))
    elec_z=np.zeros(len(elec_x))+1 #1 is embankment height
    elec=np.transpose(np.array([elec_x,elec_y,elec_z]))
    return elec

def create_variables(crest_width, slope_angle,  height,foundation_height):
    variables=pd.DataFrame(columns=['crest_width', 'slope_angle', 'height','foundation_height'])
    for cw in crest_width:
        for cot in slope_angle:
            for h in height:
                for fh in foundation_height:
                    temp=pd.DataFrame(data=[[cw,cot,h,fh]],columns=['crest_width', 'slope_angle', 'height','foundation_height'])
                    variables=pd.concat([variables,temp],ignore_index=True)
    variables.to_csv('temp/ERT_input_variables.csv')
    return variables
       
def combine_data(model,res_contrast):
    print('Combining data')
    cw=model['crest_width']
    cot=model['slope_angle']
    res=res_contrast
   
    #import files
    #embankment model
    names=['measurement','a_line','a','b_line','b','m_line','m','n_line','n','resistance','apparent_resistivity']
    e_mod=pd.read_csv(f'2_fm_results/cw{cw}_cot{cot}_res{res}_e.dat',skiprows=1,sep='\s+',names=names)
    #layered model
    l_mod=pd.read_csv(f'2_fm_results/cw{cw}_cot{cot}_res{res}_l.dat',skiprows=1,sep='\s+',names=names)
    #survey parameters
    sp=pd.read_csv('survey_parameters.csv')
    #combined models
    combined_models=pd.read_csv('3_combined_results/combined models.csv')
    #normalise numbers to 1m heigh embankment
    
    cw=cw/6 
    height=1
    bw=2*cot*height+cw
    area=height*(cw+height*cot)
    res=float(res)
    cw=round(cw,2)
    if res.is_integer():
        res=int(res)
    index=(f'cw{cw}_cot{cot}')
    
    temp=pd.DataFrame(data=e_mod['resistance'], columns=['R3D'])
    temp['R3D']=e_mod['resistance']
    temp['R2D']=l_mod['resistance']
    temp['E']=(temp['R3D']-temp['R2D'])/temp['R3D']*100
    temp['doi']=sp['doi']
    temp['array']=sp['array']
    
    if index not in combined_models['index'].unique(): # if the embankment geometry not used before creates space in dataframe for it.     
        template=sp[['a','b','m','n','survey_length','n_value','doi','array']]
        template[['index','cw','cot','bw','area']]=index,cw,cot,bw,area
        combined_models=pd.concat([combined_models,template],ignore_index=True)
    
    combined_models.loc[combined_models['index']==index,f'2D_{res}']=temp['R2D'].tolist()
    combined_models.loc[combined_models['index']==index,f'3D_{res}']=temp['R3D'].tolist()
    combined_models.loc[combined_models['index']==index,f'E_{res}']=temp['E'].tolist()
    #combined_models['doi']=combined_models['doi'].round(5)
    combined_models.to_csv('3_combined_results/combined models.csv',index=False)
    combined_models
    model_parameters={'cw':cw,'cot':cot,'res':res}
    
    visulise_error(data=temp,mp=model_parameters)

def visulise_error(data,mp):
    print('Plotting graph')
    print(data)
    #plot data
    dd=data[data['array']=='dd']
    w=data[data['array']=='w']
    sh=data[data['array']=='sh']
    mg=data[data['array']=='mg']
    ax=plt.scatter(x=dd['E'],y=dd['doi'],label='DD',c='k', s=1.5)
    plt.scatter(x=w['E'],y=w['doi'],label='W',c='r', s=1.5)
    plt.scatter(x=sh['E'],y=sh['doi'],label='SH',c='b', s=1.5)
    plt.scatter(x=mg['E'],y=mg['doi'],label='MG',c='g', s=1.5)
    
    #ax=plt.scatter(x=data['E'],y=data['doi'],s=1.5,c=data['n_value'],cmap='jet')#c='k')
    plt.yscale('log')
    #plt.xscale('log')
    ax = plt.gca()
    ax.invert_yaxis()
    plt.grid(which='major')
    plt.grid(which='minor',lw=0.2)
    plt.ylabel("Median depth of investigation [m]")
    plt.xlabel("E [%]")
    plt.title(f'cw{mp["cw"]}_cot{mp["cot"]}_rc{mp["res"]}')
    plt.legend(title='RC')
    #save figure
    plt.savefig(f'4_figures/cw{mp["cw"]}_cot{mp["cot"]}_rc{mp["res"]}.png',format='png')
    print('Figure saved \n\n')
    plt.show()


            
def forward_modelling(crest_width, slope_angle, resistivity_contrasts, height=[1],foundation_height=[0]):
    #create table of variables
    variables=create_variables(crest_width, slope_angle, height,foundation_height)
    ewd='C:/Users/adwh/Anaconda3/lib/site-packages/resipy/exe' #where gmsh lives
    
    #Create folder structure
    create_folder(fname='temp')#resipy running folder
    create_folder(fname='1_fm_meshes')#forward_model_combine
    create_folder(fname='2_fm_results')#forward_model_combine
    create_folder(fname='3_combined_results')#forward_model_combine
    
    #create electrodes
    electrodes=pd.read_csv('electrode positions.csv')
    elec_x_list=electrodes['x'].tolist()
    elec_x=np.array(elec_x_list)
    elec_y=np.zeros(len(elec_x))
    elec_z=np.zeros(len(elec_x))+1 #1 is embankment height
    elec=np.transpose(np.array([elec_x,elec_y,elec_z]))
    
    error_list=[]
    
    for index, model in variables.iterrows():
        try:
            #create mesh for a specific geometry and electrode spacing
            ewd='C:/Users/adwh/Anaconda3/lib/site-packages/resipy/exe' #where gmsh lives
    
            #model variable for iteration
            cw=model['crest_width']
            cot=model['slope_angle']
            h=model['height'] #not currently used
            #h=1
            z=model['foundation_height']
    
            #find or create mesh
            geometry=f'cw{cw}_cot{cot}'
            mesh_path=f'1_fm_meshes/{geometry}'
            mesh_name=f'1_fm_meshes/{geometry}.geo'
            if os.path.exists(mesh_name)==True:
                if os.path.exists(f'1_fm_meshes/{geometry}.msh')==True:
                    print('Creating advanced mesh')
                    resistivity=create_advanced_mesh(fname=mesh_path,electrodes=elec)
                else:
                    print('Creating .msh file')
                    create_mesh(ewd=ewd, fname=mesh_path)
                    print('Creating advanced mesh')
                    resistivity=create_advanced_mesh(fname=mesh_path,electrodes=elec)
                    print(f'File {mesh_name} .geo .msh and advanced mesh created')
            else:
                print('Creating .geo file')
                create_geo(fname=mesh_path,electrodes=elec_x_list,h=h,z=z,cw=cw,slope_angle=cot)
                print('Creating .msh file')
                create_mesh(ewd=ewd, fname=mesh_path)
                print('Creating advanced mesh')
                resistivity=create_advanced_mesh(fname=mesh_path,electrodes=elec)
                print(f'File {mesh_name} .geo .msh and advanced mesh created')
            print(resistivity)
            for rc in resistivity_contrasts:
                
                #model_type: 'layeres' or 'embankment'
                create_resistivity(res_list=resistivity,res_contrast=rc,model_type='embankment')
               
                #Run model for resistivity contrast
                
                fm_path=f'2_fm_results/cw{cw}_cot{cot}_res{rc}'
                forward_model(output_path=fm_path)
            
            #combine_forward_models()
        except:
            print(f'Model {geometry} failed')
            error_list.append(geometry)

       
    