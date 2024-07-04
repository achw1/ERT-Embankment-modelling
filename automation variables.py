# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 21:33:40 2022

@author: adwh
"""

import layered_ground_automation as ea

#To run this needs an electrode positions.csv in the root folder.
#Additionaly a copy of R3t.exe, a portocol.dat and R3t.in file is required in both the R3t_embankment/R3t_foundation folder (these are both in the root folder)..

#%%
#define variables for model space
crest_width_log=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5] #[1,1.1][1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
slope_angle=[1,1.25,1.5,1.75,2,2.25,2.5,2.75,3]
resistivity_contrasts_log=[-2,-5/3,-4/3,-1,-2/3,-1/3,0,1/3,2/3,1,4/3,5/3,2]#[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100]

crest_width=[round(10**i,2)for i in crest_width_log]
resistivity_contrasts=[round(10**rc,3) for rc in resistivity_contrasts_log]

height=[6]
foundation_height=[0]

#%%

#Create folder structure
ea.create_folder(fname='temp',file='mesh3d_geometry.txt')#resipy running folder
ea.create_folder(fname='1_fm_meshes')#forward_model_combine
ea.create_folder(fname='2_fm_results')#forward_model_combine
ea.create_folder(fname='3_combined_results', file='combined models.csv',text='index,cw,cot,bw,area,a,b,m,n,survey_length,n_value,doi')#forward_model_combine
ea.create_folder(fname='4_figures')#forward_model_combine

#create variables
variables=ea.create_variables(crest_width, slope_angle, height,foundation_height)

#import electrode file
electrodes=ea.electrodes(file_name='electrode positions.csv')


for index, model in variables.iterrows():
    try:
        #create mesh for a specific geometry and electrode spacing
        ea.mesh_creation(model=model,elec=electrodes)
        for rc in resistivity_contrasts:
            
            #layered model
            print('Running layered model \n\n')
            ea.create_resistivity(res_contrast=rc,model_type='l')
            r3t_path='C:/Users/adwh/OneDrive - NERC/Documents/Chapter 1 ERT modelling/Error modelling 12_04_23/R3t_layered_ground/R3t.exe'
            ea.forward_model(model=model, res_contrast=rc,r3t_path=r3t_path,model_type='l')#Run model for resistivity contrast
            
            #embankment model
            print('Running embankment model \n\n')

            ea.create_resistivity(res_contrast=rc,model_type='e')
            r3t_path=r'C:/Users/adwh/OneDrive - NERC/Documents/Chapter 1 ERT modelling/Error modelling 12_04_23/R3t_embankment/R3t.exe'
            ea.forward_model(model=model, res_contrast=rc,r3t_path=r3t_path,model_type='e')
            
            
            ea.combine_data(model=model,res_contrast=rc)
            
        #combine_forward_models()
    except:
        print('Model failed')
        
        with open('temp/failed_models_index.txt', 'a') as f:
            f.write(str(index) + '\n')
        

