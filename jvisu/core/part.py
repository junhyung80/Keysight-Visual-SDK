from jvisu.core.check import checkNodeClass , checkElementClass, checkPartClass , checkNatNum
import VistaDb
import VExpMngr
import VCmd
import VScn
from jvisu.config.type_dict import ATYPE
import numpy as np
import VToolKit


class part:

    def __init__(self, model=None):
        self.model = model
        self.part_list = self._get_part_list_dict()
        self.name_list = self._get_name_list()
        self.id_list = self._get_id_list()


    def get_object(self,PID):
        '''
        Get object from part id 
        '''
        #PID TYPE CHECK
        try :

            if str(type(PID)) == "<class 'int'>" :
                input_value = PID
                part_obj = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",input_value)
            elif checkPartClass(PID) == True: 
                # input_value = VistaDb.GetId(PID)
                part_obj = PID
            else :
                raise Exception('PID TYPE ERROR') 

        except Exception as e:
            print(e)


        if part_obj :
            return part_obj
        else :
            print(f'PART ID:{PID} is not exists.') 

    def cog(self,plist):
#        pnt_num, pnt_list = node.get_nodes_from_part(self.model,PID)

        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = self.get_object(i)
                        part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = self.get_object(plist)
                part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            print(e)

        part_list = list(part_set)
        num_parts = len(part_set)

        if part_list:
            pnt_num,pnt_list = VistaDb.ModelGetEntityNodes(self.model,num_parts,part_list)

        if pnt_list:
            cog_coordinate = VistaDb.NodesGetCg(pnt_num,pnt_list)
            output = [ cog_coordinate.x,  cog_coordinate.y,  cog_coordinate.z ]
            return output

    def get_name(self,PID):

        part = self.get_object(PID)

        try :
            if part :
                partname = VistaDb.GetStringValue(part, "Name")
                return partname
            else:
                raise Exception('Part ID {}  is not exist.'.format(PID)) 
        except Exception as e:
            print(e)

#        part_name = VistaDb.PartGetName(part)
#        partid = int(part_name.split("/")[0])
#        partname = '/'.join(part_name.split("/")[1:])

    def set_name(self,PID,NAME):

        part = self.get_object(PID)

        try :
            if part:
                VistaDb.DbsSetName(part,NAME)
                VExpMngr.RefreshExplorer( r"Parts" )
            else:
                raise Exception('Part ID {}  is not exist.'.format(PID)) 
        except Exception as e:
            print(e)

#


    def thickness_list(self):
        ret,objectList = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
        part_list = {}     
        for i in objectList:
            part = VistaDb.PartGetExactName(i) 
#            partid = int(part.split("/")[0])
#            partname = '/'.join(part.split("/")[1:])
            partid = VistaDb.GetId(i)
            partname = VistaDb.GetStringValue(i, "Name")
            part_t = VistaDb.PartGetThickness(i)
            part_list[partid] = [partname,part_t]

        return part_list


    def get_part_object_list(self, partlist=None):

        try:
            if partlist == None :
                part_num,part_obj = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
                return part_num , part_obj

            elif isinstance(partlist, list):
                part_num = len(partlist)
                part_obj = [VistaDb.ModelGetObjectFromId(self.model,"FePartClass",x) for x in partlist ]
                return part_num , part_obj

            else:
                raise Exception('Partlist type is not list.') 

        except Exception as e:
            print(e)



    def _get_part_list_dict(self):

        ret,objectList = VistaDb.ModelGetObjectList(self.model,"FePartClass") 

        part_list = {}     
        for part in objectList:
#            part = VistaDb.PartGetExactName(i) 
#            partid = int(part.split("/")[0])
#            partname = '/'.join(part.split("/")[1:])
            part_name = VistaDb.GetStringValue(part, "Name")
            partid = VistaDb.GetId(part)
            part_list[partid] = part_name

        return part_list

    def _get_id_list(self):
        partlist = self._get_part_list_dict()
        outlist = [x for x in partlist.keys()]
        return outlist

    def _get_name_list(self):
        partlist = self._get_part_list_dict()
        outlist = [x for x in partlist.values()]
        return outlist

    def create_null_part(self,pid=None,pname=None):

        if pid :
            part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",pid)
        else :
            part = None

        try:
            if pid  and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",pid)

            elif pid == None and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",0)

            else:
                raise Exception('Part number already exists')


        except Exception as e:
            return print(e)


        part_obj = VistaDb.ModelCreateObject(self.model, "FePartClass")
        self.set_color(part_obj)
        VistaDb.SetId(part_obj,new_pid)

        if pname :
            VistaDb.DbsSetName(part_obj,f"{pname}")
        else:
            VistaDb.DbsSetName(part_obj,f"PID_{new_pid}")

        VExpMngr.RefreshExplorer( r"Parts" )
        return new_pid


    def create_shell_part(self,pid=None,thickness=None, mid=None, pname=None, NINT=None, HCONT=None):
        ATYPE_NUM = ATYPE["SHELL"]

        if pid :
            part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",pid)
        else :
            part = None

        try:
            if pid  and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",pid)

            elif pid == None and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",0)

            else:
                raise Exception('Part number already exists')

        except Exception as e:
            return print(e)

        part_obj = VistaDb.ModelCreateObject(self.model, "FePartClass")
        self.set_color(part_obj)
        VistaDb.SetId(part_obj,new_pid)

        if pname :
            VistaDb.DbsSetName(part_obj,"{}".format(pname))
        else:
            VistaDb.DbsSetName(part_obj,"PID_{}".format(new_pid))

        part_shell = VistaDb.CreateObject("FeSectionClass")
        VistaDb.SetObjectValue(part_obj,"Property",part_shell)
        #0 = BEAM, 5 = SOLID, 3 = SHELL
        VistaDb.SetIntegerValue(part_shell,"Type",ATYPE_NUM)
        VistaDb.SetDoubleValue(part_shell,"IntegrationPoints",5)

        if thickness :
            VistaDb.SetDoubleValue(part_shell,"ShellThickness1",thickness)

        if NINT :
            VistaDb.SetDoubleValue(part_shell,"IntegrationPoints",NINT)

        if mid :
            self.set_material(new_pid,mid)

        if HCONT:
            self.set_hcont(part_obj, HCONT)

        VExpMngr.RefreshExplorer( r"Parts" )
        return new_pid




    def create_tied_part(self,pid=None,rdist=None, mid=None, pname=None):
        ATYPE_NUM = ATYPE["TIED"]

        if pid :
            part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",pid)
        else :
            part = None

        try:
            if pid  and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",pid)

            elif pid == None and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",0)

            else:
                raise Exception('Part number already exists')

        except Exception as e:
            return print(e)

        part_obj = VistaDb.ModelCreateObject(self.model, "FePartClass")
        self.set_color(part_obj)
        VistaDb.SetId(part_obj,new_pid)


        if pname :
            VistaDb.DbsSetName(part_obj,str(pname))
        else:
            VistaDb.DbsSetName(part_obj,f"PID_{new_pid}")


        part_tied = VistaDb.CreateObject("FeSectionClass")
        VistaDb.SetIntegerValue(part_tied,"Type",ATYPE_NUM)
        VistaDb.SetObjectValue(part_obj,"Property",part_tied)

        if rdist:
            VistaDb.HashtableSetExtendedDoubleAttribute(part_tied,"RDIST",rdist)

        if mid:
            self.set_material(new_pid,mid)

        VExpMngr.RefreshExplorer( r"Parts" )
        return new_pid

    def create_solid_part(self, pid=None, mid=None, pname=None, HCONT=None):
        ATYPE_NUM = ATYPE["SOLID"]

        if pid :
            part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",pid)
        else :
            part = None

        try:
            if pid and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",pid)

            elif pid == None and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",0)

            else:
                raise Exception('Part number already exists')

        except Exception as e:
            print(e)

        part_obj = VistaDb.ModelCreateObject(self.model, "FePartClass")
        self.set_color(part_obj)
        VistaDb.SetId(part_obj,new_pid)

        if pname :
            VistaDb.DbsSetName(part_obj,str(pname))
        else:
            VistaDb.DbsSetName(part_obj,f"PID_{new_pid}")

        part_solid = VistaDb.CreateObject("FeSectionClass")
        VistaDb.SetObjectValue(part_obj,"Property",part_solid)
        #0 = BEAM, 5 = SOLID, 3 = SHELL
        VistaDb.SetIntegerValue(part_solid,"Type",ATYPE_NUM)

        if mid :
            self.set_material(new_pid,mid)

        if HCONT:
            self.set_hcont(part_obj, HCONT)

        VExpMngr.RefreshExplorer( r"Parts" )
        return new_pid


    def create_plink_part(self, pid=None, mid=None, pname=None, RSEAR=None, NLAYR=None, NGESP=None, SPOTRA=None ):
        ATYPE_NUM = ATYPE["PLINK"]

        if pid :
            part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",pid)
        else :
            part = None

        try:
            if pid and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",pid)

            elif pid == None and part == None:
                new_pid = VistaDb.ModelGetUniqueId(self.model , "FePartClass",0)

            else:
                raise Exception('Part number already exists')

        except Exception as e:
            print(e)

        part_obj = VistaDb.ModelCreateObject(self.model, "FePartClass")
        self.set_color(part_obj)
        VistaDb.SetId(part_obj,new_pid)

        if pname :
            VistaDb.DbsSetName(part_obj, str(pname))
        else:
            VistaDb.DbsSetName(part_obj,f"PID_{new_pid}")

        part_plink = VistaDb.CreateObject("FeSectionClass")
        VistaDb.SetObjectValue(part_obj,"Property",part_plink)
        #
        VistaDb.SetIntegerValue(part_plink,"Type",ATYPE_NUM)

        if mid :
            self.set_material(new_pid,mid)

        if RSEAR:
            VistaDb.HashtableSetExtendedDoubleAttribute(part_plink,"RSEAR",RSEAR)

        if NLAYR:
            VistaDb.HashtableSetExtendedIntAttribute(part_plink,"NLAYR",NLAYR)

        if NGESP:
            VistaDb.HashtableSetExtendedIntAttribute(part_plink,"NGESP",NGESP)
            
        if SPOTRA:
            VistaDb.HashtableSetExtendedDoubleAttribute(part_plink,"SPOTRA",SPOTRA)

        VExpMngr.RefreshExplorer( r"Parts" )
        return new_pid

    def modify(self, pid, mid=None, thickness=None, NINT=None, HCONT=None ):

        if mid:
            self.set_material(pid, mid)

        if thickness:
            self.set_thickness(pid, thickness)

        if HCONT:
            self.set_hcont(pid, HCONT)

        if NINT :
            part_obj = self.get_object(pid)
            part_shell = VistaDb.GetObjectValue(part_obj,"Property")
            if part_shell:
                VistaDb.SetDoubleValue(part_shell,"IntegrationPoints",NINT)

    def get_material(self, pid):

        part_obj = self.get_object(pid)
        mat_obj = VistaDb.GetObjectValue(part_obj,"Material")
        mat_id = VistaDb.GetId(mat_obj)
        return mat_id

    def set_material(self, pid, mid):

        part_obj = self.get_object(pid)
        mat_obj = VistaDb.ModelGetObjectFromId(self.model,"FeMatClass",mid)
        if mat_obj:
            VistaDb.SetObjectValue(part_obj,"Material",mat_obj)
        else: 
            print("MAT_ID {} is not exists".format(MID))

    def get_thickness(self,pid):

        part_obj = self.get_object(pid)
        if part_obj:
            section = VistaDb.GetObjectValue(part_obj,"Property")
            return VistaDb.GetDoubleValue(section,"ShellThickness1")

    def set_thickness(self, pid, thickness):

        part_obj = self.get_object(pid)
        if part_obj:
            section = VistaDb.GetObjectValue(part_obj,"Property")
            VistaDb.SetDoubleValue(section,"ShellThickness1",thickness)

    def get_type(self,pid):

        part_obj = self.get_object(pid)
        section = VistaDb.GetObjectValue(part_obj,"Property")
        type_id = VistaDb.GetIntegerValue(section,"Type")
        return type_id


    def get_hcont(self, pid):

        part_obj = self.get_object(pid)

        if part_obj:
#            section = VistaDb.GetObjectValue(part_obj,"Property")
            output = VistaDb.GetDoubleValue(part_obj,"OptionalThickness")
            return output

    def set_hcont(self, pid, opt_thickness):

        part_obj = self.get_object(pid)

        if part_obj:
            VistaDb.SetDoubleValue(part_obj,"OptionalThickness",float(opt_thickness))

    def list_check(self, mylist):

        if isinstance(mylist, list):
            plist = [x for x in mylist if checkPartClass(x)]
            if len(plist) == 0:
                plist = [ VistaDb.ModelGetObjectFromId(self.model,"FePartClass",x) for x in mylist ]

            return plist

        elif isinstance(mylist, int):
            plist = [ VistaDb.ModelGetObjectFromId(self.model,"FePartClass",mylist) ]
            return plist

        elif checkPartClass(mylist):
            plist = [ mylist ]
            return plist
        else:
            print("type error")
            return    

    def locate(self,pid):

        plist = self.list_check(pid)

        if plist:

            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(plist), plist )
            ret=VCmd.ExecuteCommand( display_command, r"Locate" )


    def hide(self,pid):

        plist = self.list_check(pid)

        if plist:

            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(plist), plist )
            ret=VCmd.ExecuteCommand( display_command, r"HideSelected" )


    def show(self,pid):

        plist = self.list_check(pid)

        if plist:

            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(plist), plist )
            ret=VCmd.ExecuteCommand( display_command, r"ShowSelected" )


    def set_color(self,PID,cvalue=None):

        part_obj = self.get_object(PID)

        if cvalue:
            color = cvalue 
        else:
            r = np.random.randint(0, 255)
            g = np.random.randint(0, 255)
            b = np.random.randint(0, 255)
            color = f"{r} {g} {b}"

#        VistaDb.SetColor(part_obj,color)
#        VistaDb.PartUpdateDisplay(part_obj)
#        var1=VCmd.Activate(0 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
#        VCmd.SetObjectArrayValue( var1, r"ExplorerSelection", 1, [part_obj] )
#        VCmd.SetStringValue( var1, r"PartColor", color )
#        ret=VCmd.ExecuteCommand( var1, r"ChangePartAttributes" )

#        VExpMngr.RefreshExplorer( r"Parts" )
        value = color.split()
        r = int(value[0])
        g = int(value[1])
        b = int(value[2])
        part_list = [part_obj]
        VToolKit.VtkUpdatePartColorStatus(self.model,len(part_list),part_list,2,r,g,b)

    def get_color(self,PID):
        part_obj = self.get_object(PID)

        color = VistaDb.GetColor(part_obj)
        return color

    def get_bounding_box_cg(self, plist):
        nid_list, coordinate_array = self.get_coordinate_array(plist, decimals=5)

        if nid_list:
            xmin, ymin, zmin = coordinate_array.min(axis=0)
            xmax, ymax, zmax = coordinate_array.max(axis=0)

            center = [ (xmin + xmax) * 0.5, (ymin + ymax) * 0.5, (zmin + zmax) * 0.5 ]
            return [ float(x) for x in center ]
        else:
            return False

    def get_bounding_box_coordinate(self, plist):

        nid_list, coordinate_array = self.get_coordinate_array(plist, decimals=5)

        if nid_list:

            xmin, ymin, zmin = coordinate_array.min(axis=0)
            xmax, ymax, zmax = coordinate_array.max(axis=0)

            bbox_points = np.array([ [x, y, z] for x in (xmin, xmax) for y in (ymin, ymax) for z in (zmin, zmax) ])
            return [xmin, xmax, ymin, ymax, zmin, zmax]
        else:
            return False


    def get_cog_array(self, plist, decimals=5):

        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = self.get_object(i)
                        part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = self.get_object(plist)
                part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        part_list = list(part_set)

        if part_list:
            ele_num, ele_list = VistaDb.ModelGetElementsFromObjects(self.model,len(part_list),part_list)

            eid_list = [VistaDb.GetId(x) for x in ele_list]
            coordinate_list = [ [pt.x, pt.y, pt.z] for pt in (VistaDb.ElementGetCenterOfGravity(e) for e in ele_list) ]
            coordinate_array = np.around(coordinate_list, decimals=decimals)            

            return eid_list, ele_list, coordinate_array

    def get_node_object_list(self, plist):

        part_obj_list = self.list_check(plist)
        node_num, nodes_list = VistaDb.ModelGetEntityNodes(self.model,len(part_obj_list), part_obj_list)
        return nodes_list


    def get_coordinate_array(self, plist, decimals=5):

        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = self.get_object(i)
                        part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = self.get_object(plist)
                part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            print(e)
            return False, False

        part_list = list(part_set)

        if part_list:
            node_num, nodes_list = VistaDb.ModelGetEntityNodes(self.model,len(part_list),part_list)

            nid_list = [ VistaDb.GetId(x) for x in nodes_list]
            coordinate_list = [ [pt.x, pt.y, pt.z] for pt in (VistaDb.GetVgPoint3Value(n, "Point") for n in nodes_list) ]
            coordinate_array = np.around(coordinate_list, decimals=decimals)           

            return nid_list, coordinate_array

    def delete(self, plist, solver_type=2):
        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = self.get_object(i)
                        part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = self.get_object(plist)
                part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        part_list = list(part_set)

        if part_list:
            VistaDb.ModelDeleteParts(self.model, len(part_list),part_list,0,solver_type)
#            VE.DeleteEntities(len(part_list),part_list)
        else:
            print("no part_obj")


    def get_displayed_part_id_list(self):
        ret, object_list = VistaDb.ModelGetObjectList( self.model, "FePartClass")

        pid_list = [ VistaDb.GetId(part) for part in object_list if VistaDb.PartGetDisplayStatus(self.model, part, 1) ]

        return pid_list if pid_list else False
