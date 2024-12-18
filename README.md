# FORGE
Repository containing the input files for geos models of [Utah FORGE](https://utahforge.com/).

## Description
This repository provides the input deck for numerical models associated with two Utah FORGE research projects: `Closing the Loop Between In situ Stress Complexity and EGS Fracture Compexity` (Project Number: 2-2446) and `Coupled Investigation of Fracture Permeability Impact on Reservoir Stress and Seismic Slip Behavior` (Project Number: 5-2428). 

Three kinds of simulation decks are included: (i) hydraulic fracturing simulation (`HydroFrac` folder), (ii) phase-field simulation (`PhaseField` folder), and (iii) thermo-hydro-mechanical simulation (`ThermoHydroMech` folder). 

These are the input decks related to the following GDR submissions:

- **GDR Submission XXX**
  - Folders: **[Folder Name 1]**

- **GDR Submission XXX**
  - Folders: **[Folder Name 2]**

The detailed structure of the repository is provided below. 

## Repository Structure
```
FORGE                                                                     # Main repository 
│
├── HydroFrac/                                                            # Files for the hydraulic fracturing simulation
│   ├── ApparentKIcAnisotropy_test                                        # Files for the validation example
│   │   ├── injectionTable/                                               # Injection rate table
│   │   ├── stressProfile/                                                # Stress roughness profile 
│   │   └── xmls/                                                         # Input files for validation examples
│   │
│   └── Stage3                                                            # Files for Stage 3 simulation cases
│       ├── injectionTable3/                                              # Injection rate table for Stage 3
│       ├── scripts/                                                      # Python script to plot fracture growth
│       ├── stressProfile/                                                # Field stress profile based on sonic log
│       └── xmls/                                                         # Input files
│           ├── forgeStimulation_hydroFrac_3d_base.xml                    # Base input file
│           ├── forgeStimulation_hydroFrac_3d_heteroStressProfile.xml     # Main input file for the case with the field stress profile
│           └── forgeStimulation_hydroFrac_3d_apparentKIcAnisotropy.xml   # Main input file for calibrating apparent KIc anisotropy
│
├── PhaseField/                                                           # Files for the phase-field simulation
│   ├── meshes/                                                           # Wellbore mesh files
│   └── xmls/                                                             # Input files for different wellbore deviaiton cases
│
├── ThermoHydroMech/                                                      # Files for the Stage 3 THM simulation
│   ├── injectionTable3/                                                  # Injection rate table
│   ├── permTable/                                                        # DFN permeability table
│   ├── pressureTable/                                                    # Initial pressure table
│   ├── tempTable/                                                        # Initial temperature table
│   ├── scripts/                                                          # Python script to plot pressure
│   └── xmls/                                                             # Input files
│
└── README.md                        
```


## How to run 
### For input files in `HydroFrac` and `ThermoHydroMech`
One should swith to the FORGE modeling branch:
```
git checkout origin/frankfei/forge-HF
```

### For input files in `PhaseField`
One should swith to the phase-field modeling branch:
```
git checkout origin/feature/frank/phasefield_nucleation_poromech
```

**Note:** Refer to the [GEOS documentation](https://geosx-geosx.readthedocs-hosted.com/en/latest/index.html) for instruction on how to install and run GEOS.  
