ATYPE = { "SOLID":5, "BSHELL":48, "TSHELL":49, "SHELL":3, "MEMBR":50 , "BEAM":0,
          "BAR":10,  "SPRING":1,  "SPRGBM":58, "MBSPR":44, "JOINT":45, "KJOIN":46,
          "MTOJNT":77, "MBKIN":47, "SPHEL":55, "GAP":9, "PLINK":54, "ELINK":52, 
          "LLINK":53, "SLINK":51, "TIED":57, "COS3D":79} 

KINTYPE = { "SET":1, "NODE":2, "RIGID":3, "RIGID_LOCAL":4, "BOUNC":5 , "VELBC":6,
          "DIS3D":7, "VEL3D":8, "ACC3D":9, "ACFLD":10, "DAMP":11, "RAN3D":13, 
          "RVE3D":14, "RAC3D":15} 

CNT_TYPE= { 33:105, 34:99, 36:100, 37:101, 43:178, 44:154, 46:102, 54:153, 154:186}

ELEMENT_TYPE = { "HEXA20":2006 , "PENTA15":2007, "TETRA10":2008, "TETRA4":2004, "SHELL4":1000, 
                 "HEXA":2000 , "PENTA":2002, "SHELL3":1002, "BEAM":100, "BAR":101 , "SPRING":517, 
                 "SPRGBM":518, "PLINK":6004, "ELINK":6002, "LLINK":6003, "SLINK":6001,} 

GROUP_TYPE = { "FeNodeClass":0, "FePartClass":1, "FeQuadClass":2,  "FeTriaClass":2,
        "FeSegmentClass":3, "FeTetraClass":4, "FePentaClass":4, "FeHexaClass":4,
        "FeQuadHigherClass":5, "FeTriaHigherClass":5, "FeBeamClass":6, "FeDiscreteClass":7, 
        "FeBoxClass":8, "FeJointClass":9, "FeRigidClass":11, "FeSetClass":24, "heterogeneous":12 }

dyna_mater_type = { \
   'CONSTRAINED_JOINT_STIFFNESS_GENERALIZED' :( 3134, 122, '  0'  ), \
   'MAT_ELASTIC'                             :( 3101,   0, '001'  ), \
   'MAT_PLASTIC_KINEMATIC'                   :( 3103,   4, '003'  ), \
   'MAT_VISCOELASTIC'                        :( 3105,   7, '006'  ), \
   'MAT_NULL'                                :( 3107,  10, '009'  ), \
   'MAT_STRAIN_RATE_DEPENDENT_PLASTICITY'    :( 3111,  20, '019'  ), \
   'MAT_RIGID'                               :( 3112,  21, '020'  ), \
   'MAT_PIECEWISE_LINEAR_PLASTICITY'         :( 3103,  25, '024'  ), \
   'MAT_MOONEY_RIVLIN_RUBBER'                :( 3106,  28, '027'  ), \
   'MAT_FABRIC'                              :( 3102,  36, '034'  ), \
   'MAT_KELVIN_MAXWELL_VISCOELASTIC'         :( 3105,  62, '061'  ), \
   'MAT_VISCOUS_FOAM'                        :( 3132,  63, '062'  ), \
   'MAT_CABLE_DISCRETE_BEAM'                 :( 3119,  72, '071'  ), \
   'MAT_ELASTIC_SPRING_DISCRETE_BEAM'        :( 3135, 244, '074'  ), \
   'MAT_GENERAL_VISCOELASTIC'                :( 3117,  74, '076'  ), \
   'MAT_OGDEN_RUBBER'                        :( 3106,  76, '077_O'), \
   'MAT_HYPERELASTIC_RUBBER'                 :( 3106,  75, '077_H'), \
   'MAT_SOFT_TISSUE_VISCO'                   :( 3117, 322, '092'  ), \
   'MAT_GENERAL_NONLINEAR_6DOF_DISCRETE_BEAM':( 3135, 256, '119'  ), \
   'MAT_GENERAL_NONLINEAR_1DOF_DISCRETE_BEAM':( 3135, 208, '121'  ), \
   'MAT_HEART_TISSUE'                        :(10332, 177, '128'  ), \
   'MAT_LUNG_TISSUE'                         :( 3117, 172, '129'  ), \
   'MAT_MUSCLE'                              :( 3151, 293, '156'  ), \
   'MAT_HILL_FOAM'                           :( 3117, 298, '177'  ), \
   'MAT_SIMPLIFIED_RUBBER/FOAM'              :( 3106, 207, '181'  ), \
   'MAT_SPRING_ELASTIC'                      :( 3120,  83, 'S01'  ), \
}
# VPS material type: ( Visual ClassId, Visual Material Type )
vps_mater_type = {  \
      1: (3109,  13), \
      2: (3104,   6), \
      5: (3105,   7), \
      6: (3105, 210), \
      7: (3108,  11), \
      8: (3105, 211), \
     12: (3105, 212), \
     15: (3105, 213), \
     16: (3109,  99), \
     20: (3117,  55), \
     22: (3132,  63), \
     24: (3117, 214), \
     26: (3109, 153), \
     28: (3109, 167), \
     30: (3121, 100), \
     35: (3109, 215), \
     36: (3109, 216), \
     37: (3105, 217), \
     38: (3105, 368), \
     41: (3140, 147), \
     42: (3140, 336), \
     45: (3109, 218), \
     51: (3105, 219), \
     52: (3109, 220), \
     61: (3105, 221), \
     62: (3103, 263), \
     71: (3109, 222), \
     99: (3107, 103), \
    100: (3107, 104), \
    101: (3101, 105), \
    103: (3103, 107), \
    105: (3103, 108), \
    106: (3103, 109), \
    108: (3124, 110), \
    109: (3124, 250), \
    110: (3101, 337), \
    115: (3103, 148), \
    116: (3103, 338), \
    117: (3124, 242), \
    118: (3103, 149), \
    121: (3105, 192), \
    126: (3101, 224), \
    127: (3124, 396), \
    128: (3124, 225), \
    131: (3125, 169), \
    143: (3103, 182), \
    150: (3126, 112), \
    151: (3126, 150), \
    152: (3126, 226), \
    161: (3101, 227), \
    162: (3103, 264), \
    171: (3103, 228), \
    200: (3107, 113), \
    201: (3101, 114), \
    202: (3103, 115), \
    204: (3128, 117), \
    205: (3128, 118), \
    212: (3103, 119), \
    213: (3129, 120), \
    214: (3129, 151), \
    220: (3130, 121), \
    221: (3134, 122), \
    222: (3134, 123), \
    223: (3130, 229), \
    224: (3130, 339), \
    225: (3130, 341), \
    230: (3134, 166), \
    301: (3136, 230), \
    302: (3136, 231), \
    303: (3136, 232), \
    304: (3136, 340), \
    305: (3136, 417), \
    371: (3136, 418) }

vista_mater_class_name = { \
    3101:'FeMatElasticClass'           , \
    3103:'FeMatPlasticityClass'        , \
    3104:'FeMatSoliFoamClass'          , \
    3105:'FeMatViscoelasticClass'      , \
    3107:'FeMatNullClass'              , \
    3108:'FeMatEPHydroClass'           , \
    3109:'FeMatEPIsotropicClass'       , \
    3117:'FeMatFoamClass'              , \
    3121:'FeMatBiphaseOrthoClass'      , \
    3124:'FeMatEPAnisotropicClass'     , \
    3125:'FeMatOrthotropicBiphaseClass', \
    3126:'FeMatLayredMembraneClass'    , \
    3128:'FeMatNBarDashpotClass'       , \
    3129:'FeMatEPBeamClass'            , \
    3130:'FeMatSpringDashpotClass'     , \
    3132:'FeMatViscoFoamClass'         , \
    3134:'FeMatJointClass'             , \
    3136:'FeMatSpotweldClass'          , \
    3140:'FeMatImprSideImpactClass'    }

# solver type
solver_lsdyna = 0
solver_nastran = 1
solver_vps = 2
solver_abaqus = 3

#
# input file format
e_inpvdb = 0
e_inpnas = 1
e_inpdyn = 2
e_inpigs = 4
e_inpvps = 5
e_inpsts = 25
e_inpaba = 34


#Full car assembly name 
assem_list = ["BARRIER ", "FR_LH_DUMMY", "FR_RH_DUMMY", "RR_LH_DUMMY", "RR_RH_DUMMY", "FEM", "FENDER_LH", "FENDER_RH", \
        "F_APRON_LH", "F_APRON_RH", "FR_SMBR_LH", "FR_SMBR_RH", "FR_BBEAM", "RR_BBEAM", "FR_CBOX_LH", "FR_CBOX_RH",\
        "RR_CBOX_LH", "RR_CBOX_RH", "COWL", "DASH", "ROOF", "CTR_FLR", "RR_FLR", "RR_SMBR_LH", "RR_SMBR_RH", "SIDE_LH",\
        "SIDE_RH", "QTR_LH", "QTR_RH", "B_PNL", "P_TRAY", "HOOD", "T_LID", "FR_DR_BIW_LH", "FR_DR_MODULE_LH", "FR_DR_TRIM_LH",\
        "FR_DR_GLASS_LH", "FR_DR_BIW_RH", "FR_DR_MODULE_RH", "FR_DR_TRIM_RH", "FR_DR_GLASS_RH", "RR_DR_BIW_LH", "RR_DR_MODULE_LH",\
        "RR_DR_TRIM_LH", "RR_DR_GLASS_LH", "RR_DR_BIW_RH", "RR_DR_MODULE_RH", "RR_DR_TRIM_RH", "RR_DR_GLASS_RH",\
        "FR_BUMPER_CVR", "FR_BUMPER_FOAM", "RR_BUMPER_CVR", "RR_BUMPER_FOAM", "COWL_X_MBR", "CONSOLE", "C_PAD",\
        "HVAC", "FR_SEAT_LH", "FR_SEAT_RH", "RR_SEAT_LH", "RR_SEAT_RH", "THIRD_SEAT", "B_PLR_TRIM_LH", "B_PLR_TRIM_RH",\
        "H_LAMP", "C_LAMP", "W_SHIELD", "RR_GLASS", "WIPER", "FR_SUBFRAME", "FR_SUSP", "FR_TIRE", "RR_X_MBR", "RR_SUSP",\
        "RR_TIRE", "STRG_COLUMN", "STRG_WHEEL", "MUFFLER", "P_SHAFT", "FUEL_TANK", "SPARE_TIRE", "ACCEL", "BRAKE", "CLUTCH",\
        "P_BRAKE", "TGS", "POWER_TRAIN", "RADIATOR", "BATTERY", "F_BOX", "A_CLEANER", "RESERVOIR", "INTERCOOLER", "ABS",\
        "ELEC_PARTS", "DAB", "DKAB", "PAB", "PKAB", "SAB", "CAB", "SEAT_BELT", "EV_HEV_BATT", "EV_HEV_CABLE", "TEST_DEVICE",\
        "ETC", "BIW" ]
