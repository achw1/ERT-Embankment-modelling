# ERT-Embankment-modelling

Code for the ERT  modeling presented in 'Assessing the effect of offline topography on electrical resistivity measurements: insights from flood embankments.' 

Authors: Adrian White (a, c), James Boyd (a, b), Paul Wilkinson (a), Holly E. Unwin (a), James Wookey (c), John Michael Kendall (d), Andrew Binley (b), Jonathan Chambers (a). 

a.	British Geological Survey, Nottingham, United Kingdom*
b.	Lancaster University, Lancaster, United Kingdom
c.	University of Bristol, Bristol, United Kingdom
d.	University of Oxford, Oxford, United Kingdom

## File details:
  - Automation variables.py - Script to run the forward modelling functions to calculate topographic effects for a range of embankment topographies
  - layered_ground_auntomation.py - A module containing fuctions run by Automation variables.py
  - R3t_embankment.in - R3t.in file for the embankment model (must be renamed as R3t.in to run)
  - R3t_layered_ground.in - R3t.in file for the layered-ground (flat) model (must be renamed as R3t.in to run)
  - protocol.dat - protocol file describing each 4 electrode measurement in terms of electrode number.
  - survey-parameters.csv - key details for each measurement.
  - effective_depth.py - function to calculate effective depth from a 4 point measurement assuming homogenous ground
  - Figures with different E.ipynb Jupyter notebook visulising the outputs of the ERT forward models. It reads in the file from the folder that is created called '3_combined_results'

## Folder structure:
THis foulder structure is required to run the forward modelling.

> Working Directory
- Automation variables.py
- layered_ground_auntomation.py
- survey-parameters.csv

  > R3t_embankment
    - protocol.dat
    - R3t_embankment.in (rename R3t.in)
    - R3t.exe (R3t executable)
 
  > R3t_layered_ground
    - protocol.dat
    - R3t_layered_ground.in (rename R3t.in)
    - R3t.exe (R3t executable)

  
