from jvisu.core.check import checkMatClass 
import VistaDb
import VExpMngr
import VToolKit
from jvisu.config.type_dict import ATYPE, vps_mater_type, vista_mater_class_name


class material:

    def __init__(self, model=None):
        self.model = model

    def get_all_object(self):
        ret, material = VistaDb.ModelGetObjectList(self.model, "FeMatClass")
        return material

    def get_object(self,mid):
        '''
        Get object from material id 
        '''
        #PID TYPE CHECK
        try :

            if str(type(mid)) == "<class 'int'>" :
                input_value = mid
            elif checkMatClass(mid):
                return mid
            else :
                raise Exception('mid TYPE ERROR') 

        except Exception as e:
            print(e)
            return None

        mat_obj = VistaDb.ModelGetObjectFromId(self.model,"FeMatClass",input_value)

        if mat_obj :
            return mat_obj
        else :
            print('Material ID:{} is not exists.'.format(mid)) 
            return None

    def create_object(self,mtype=101, mid=None):
        mtype_id = vps_mater_type[mtype][0]
        mtype = vps_mater_type[mtype][1]
        matclass = vista_mater_class_name[mtype_id]

        mat_obj = VistaDb.ModelCreateObject(self.model, matclass)
        mat_id_unique = VistaDb.ModelGetUniqueId(self.model , matclass,0)

        if mid:
            mat_id_check = VistaDb.ModelGetObjectFromId(self.model,"FeMatClass",mid)
        else:
            mat_id_check = None

        if mid and mat_id_check == None:
            VistaDb.SetId(mat_obj,mid)
        else:
            VistaDb.SetId(mat_obj,mat_id_unique)

        VistaDb.SetIntegerValue(mat_obj,"Type",mtype)

        return mat_obj


    def get_sigma_option_number(self, mat_obj):

        mat_type_id = VistaDb.GetIntegerValue(mat_obj,"Type")

        mat_class_name = VistaDb.GetClassName(mat_obj)
        rev_class_name = {j:i for i,j in vista_mater_class_name.items()}
        rev_class_name_id = rev_class_name[mat_class_name]

        rev_type_id = {j:i for i,j in vps_mater_type.items()}
        mat_id = rev_type_id[( rev_class_name_id, mat_type_id)]

        if type(mat_id) == int :
            return mat_id
        else:
            print("Error: Get material ID")

    def set_sigma_option(self, mat_obj, type_name):

        solid_mtype_id = [1, 16, 26, 35, 52, 62, 71]
        shell_mtype_id = [103, 105, 106, 108, 109, 115, 116, 117, 118, 127, 128, 143, 162, 171]

        solid_list1 = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5, "ECURV":6, "LOOKU":7, "VOCEG":8 }
        solid_list2 = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5, "ECURV":6 }
        solid_list3 = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5 }
        solid_list4 = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5, "LOOKU":6, "ECURV":7 }
        solid_list5 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4 }

        solid_sigma_option_num = { 1:solid_list1, 16:solid_list2, 71:solid_list2, \
                                   26:solid_list3, 35:solid_list3, 52:solid_list4, 62:solid_list5 }

        shell_list1 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4, "ECURV":5 }
        shell_list2 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4 }
        shell_list3 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4, "KINEM":5, "YOSHD":6, "TCURV":7, "YOSSW":8 }
        shell_list4 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4, "KINEM":5, "YOSHD":6, "TCURV":7, "LOOKU":8, "YOSSW":9 }
        shell_list5 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4, "VOCEG":5 }
        shell_list6 = { "YIELD STRESS":1, "CURVE":2, "POWER":3, "KRUPK":4, "KINEM":5 }
        shell_list7 = { "BLANK":1, "ECURV":2 }

        shell_sigma_option_num = { 103:shell_list1, 105:shell_list1, 106:shell_list1, 171:shell_list1, \
                             108:shell_list2, 115:shell_list2, 116:shell_list2, 118:shell_list2, 162:shell_list2, \
                             109:shell_list3, \
                             117:shell_list4, \
                             127:shell_list5, \
                             128:shell_list6, \
                             143:shell_list7, }

        upper_name = type_name.upper()
        mat_type_num = self.get_sigma_option_number(mat_obj)

        if mat_type_num in solid_mtype_id :
            solid_type_dict = solid_sigma_option_num[mat_type_num]
            val = solid_type_dict[upper_name]
            VistaDb.SetIntegerValue(mat_obj, r"CurveKrupkFlag" , val)

        elif mat_type_num in shell_mtype_id :
            shell_type_dict = shell_sigma_option_num[mat_type_num]
            val = shell_type_dict[upper_name]
            VistaDb.SetIntegerValue(mat_obj, r"CurveKrupkFlag" , val)

        else:
            print("sigmOPTN type error")

        


    def get_name(self,mid):

        mat_obj = self.get_object(mid)


        if mat_obj :
            # hash_tbl = VistaDb.GetHashtable(mat_obj, "VExtendedObject")
            # _, name = VistaDb.HashtableGetString(hash_tbl, "NAME")
            output = VistaDb.GetStringValue(mat_obj,"Name")
            return output 
        else:
            return None  
#


    def set_name(self,mid,mat_name):

        mat_obj = self.get_object(mid)


        if mat_obj :
            output = VistaDb.DbsSetName(mat_obj,mat_name)
            VExpMngr.RefreshExplorer( r"Materials" )

#


    def create_mat1(self,name=None,mid=None,rho=7.8e-6,e_value=210,nu=0.3):

        mtype = 1
        mat_obj = self.create_object(mtype,mid=mid)
        mat_id = VistaDb.GetId(mat_obj)

        if name :
            mat_name = name
        else:
            mat_name = "Material_ID_{}".format(mat_id)

        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))

        RHO = float(rho)
        #Shear Modulus
        G = round(float(e_value/(2*(1+nu))),4)
        #Bulk Modulus
        K = round(float(e_value/(3*(1-2*nu))),4)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"ShearModulus",G)
        VistaDb.SetDoubleValue(mat_obj,"BulkModulus",K)
        VistaDb.SetDoubleValue(mat_obj,"YieldStress",float(1e30))

        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def create_mat16(self,Name=None,MID=None,rho=7.8e-6,e_value=210,nu=0.3):

        mtype = 16
        mat_obj = self.create_object(mtype,mid=MID)
        mat_id = VistaDb.GetId(mat_obj)

        if Name :
            mat_name = Name
        else:
            mat_name = "Material_ID_{}".format(mat_id)

        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))

        RHO = float(rho)
        #Shear Modulus
        G = round(float(e_value/(2*(1+nu))),4)
        #Bulk Modulus
        K = round(float(e_value/(3*(1-2*nu))),4)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"ShearModulus",G)
        VistaDb.SetDoubleValue(mat_obj,"BulkModulus",K)
        VistaDb.SetDoubleValue(mat_obj,"YieldStress",float(1e30))

        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def create_mat100(self,name=None,mid=None,rho=7.8e-6,e_value=210,nu=0.3):
        mtype= 100
        mat_obj = self.create_object(mtype,mid=mid)
        mat_id = VistaDb.GetId(mat_obj)

        if name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))


        RHO = float(rho)
        E = float(e_value)
        NU = float(nu)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"YoungsModulus",E)
        VistaDb.SetDoubleValue(mat_obj,"PoissonsRatio",NU)

        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def create_mat101(self,name=None,mid=None,rho=7.8e-6,e_value=210,nu=0.3):
        mtype= 101
        mat_obj = self.create_object(mtype,mid=mid)
        mat_id = VistaDb.GetId(mat_obj)

        if name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))


        RHO = float(rho)
        E = float(e_value)
        NU = float(nu)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"YoungsModulus",E)
        VistaDb.SetDoubleValue(mat_obj,"PoissonsRatio",NU)

        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj

    def create_mat117(self,Name=None,MID=None,rho=7.8e-6,e_value=210,nu=0.3):
        mtype= 117
        mat_obj = self.create_object(mtype,mid=MID)
        mat_id = VistaDb.GetId(mat_obj)

        if Name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = Name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))


#        RHO = float(rho)
#        E = float(e_value)
#        NU = float(nu)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"YoungsModulus",E)
        VistaDb.SetDoubleValue(mat_obj,"PoissonsRation",NU)

        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def create_mat200(self,Name=None, MID=None,rho=7.8e-6,e_value=210):
        mtype= 200
        mat_obj = self.create_object(mtype,mid=MID)
        mat_id = VistaDb.GetId(mat_obj)
        

        if Name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = Name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))

        RHO = float(rho)
        E = float(e_value)
        
        VistaDb.SetDoubleValue(mat_obj,"Density",RHO)
        VistaDb.SetDoubleValue(mat_obj,"YoungsModulus",E)


        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def create_mat301(self,Name=None,MID=None):
        mtype= 301
        mat_obj = self.create_object(mtype,mid=MID)
        mat_id = VistaDb.GetId(mat_obj)

        if Name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = Name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))


        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj

    def create_mat302(self,Name=None, MID=None):
        mtype= 302
        mat_obj = self.create_object(mtype,mid=MID)
        mat_id = VistaDb.GetId(mat_obj)

        if Name == None:
            mat_name = "Material_ID_{}".format(mat_id)
        else:
            mat_name = Name
        VistaDb.DbsSetName(mat_obj,"{}".format(mat_name))


        VToolKit.UpdateRanges( self.model,1,[mat_obj])
        VExpMngr.RefreshExplorer( r"Materials" )
        return mat_obj 

    def get_type(self, mid):

        mat_obj = self.get_object(mid)

        if mat_obj:
            mat_type_id = VistaDb.GetIntegerValue(mat_obj,"Type")
            return mat_type_id
        else:
            return None

    def mat103_to_mat1(self, matid):

        mat_obj = self.get_object(matid)
        matid = VistaDb.GetId(mat_obj) + 1
        mat_name = self.get_name(mat_obj) + "_SOLID"

        RHO = VistaDb.GetDoubleValue(mat_obj,"Density")
        E = VistaDb.GetDoubleValue(mat_obj,"YoungsModulus")
#        NU = VistaDb.GetDoubleValue(mat_obj,"PoissonsRatio")
        NU = VistaDb.GetDoubleValue(mat_obj,"PoissionsRatio")
        print(f"RHO: {RHO}")
        print(f"E: {E}")
        print(f"NU: {NU}")

        curve_list = []
        rate_list = []

        for i in range(8):
            curve = VistaDb.GetObjectValue(mat_obj, "LCStressStrain{}Pam".format(i+1))  
            rate = VistaDb.GetDoubleValue(mat_obj, "StrainRate{}".format(i+1))
            if curve:
                curve_list.append(curve)
                rate_list.append(rate)
        solid_mat_obj = self.create_mat1(name=mat_name,mid=matid,rho=RHO,e_value=E,nu=NU)


        solid_sigma_opt = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5, "ECURV":6, "LOOKU":7, "VOCEG":8 }
        shell_sigma_opt = { 1:"YIELD STRESS", 2:"CURVE", 3:"POWER", 4:"KRUPK", 5:"ECURV" }

        shell_sigma_opt_num = VistaDb.GetIntegerValue(mat_obj, r"CurveKrupkFlag")
        shell_sigma_name = shell_sigma_opt[shell_sigma_opt_num]

        solid_sigma_opt_num = solid_sigma_opt[shell_sigma_name]

        VistaDb.SetIntegerValue(solid_mat_obj, r"CurveKrupkFlag" , solid_sigma_opt_num)

        num = 1
        for i,j in zip(curve_list, rate_list):

            VistaDb.SetObjectValue(solid_mat_obj, "LCStressStrain{}Pam".format(num), i)  
            VistaDb.SetDoubleValue(solid_mat_obj, "StrainRate{}".format(num), j)
            num += 1
        return solid_mat_obj
            

    def mat103_to_mat16(self, matid):

        mat_obj = self.get_object(matid)
        matid = VistaDb.GetId(mat_obj) + 1
        mat_name = self.get_name(mat_obj) + "_SOLID"

        RHO = VistaDb.GetDoubleValue(mat_obj,"Density")
        E = VistaDb.GetDoubleValue(mat_obj,"YoungsModulus")
#        NU = VistaDb.GetDoubleValue(mat_obj,"PoissonsRatio")
        NU = VistaDb.GetDoubleValue(mat_obj,"PoissionsRatio")
        print(f"RHO: {RHO}")
        print(f"E: {E}")
        print(f"NU: {NU}")

        curve_list = []
        rate_list = []

        for i in range(8):
            curve = VistaDb.GetObjectValue(mat_obj, "LCStressStrain{}Pam".format(i+1))  
            rate = VistaDb.GetDoubleValue(mat_obj, "StrainRate{}".format(i+1))
            if curve:
                curve_list.append(curve)
                rate_list.append(rate)
        solid_mat_obj = self.create_mat16(Name=mat_name,MID=matid,rho=RHO,e_value=E,nu=NU)


        solid_sigma_opt = { "YIELD STRESS":1, "BLANK":2, "CURVE":3, "POWER":4, "KRUPK":5, "ECURV":6, "LOOKU":7, "VOCEG":8 }
        shell_sigma_opt = { 1:"YIELD STRESS", 2:"CURVE", 3:"POWER", 4:"KRUPK", 5:"ECURV" }

        shell_sigma_opt_num = VistaDb.GetIntegerValue(mat_obj, r"CurveKrupkFlag")
        shell_sigma_name = shell_sigma_opt[shell_sigma_opt_num]

        solid_sigma_opt_num = solid_sigma_opt[shell_sigma_name]

        VistaDb.SetIntegerValue(solid_mat_obj, r"CurveKrupkFlag" , solid_sigma_opt_num)

        num = 1
        for i,j in zip(curve_list, rate_list):

            VistaDb.SetObjectValue(solid_mat_obj, "LCStressStrain{}Pam".format(num), i)  
            VistaDb.SetDoubleValue(solid_mat_obj, "StrainRate{}".format(num), j)
            num += 1
        return solid_mat_obj

