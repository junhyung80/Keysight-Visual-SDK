from jvisu.core.check import checkInteger, checkNodeClass , checkElementClass, checkPartClass , checkNatNum, checkPointClass
import VistaDb
import VToolKit
import VCmd
import VHostManager
import VScn
from VgPoint3 import VgPoint3
from scipy.spatial import cKDTree
import numpy as np

class node:

    def __init__(self, model=None):
        self.model = model
        self.get_bounding_box()


    def cnode_to_node(self, NID):

        node_obj = self.get_object(NID)

        nid = VistaDb.GetId(node_obj)

        var1=VCmd.Activate(0 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
        var5=VCmd.Activate( 0, r"VCPUtilities.VCPUtilInterface", r"ConvertNodes" )
        lst1_count,lst1 =  VScn.List( "  N {} ".format(nid)  )
        VCmd.SetObjectArrayValue( var1, r"GraphicSelection",  lst1_count , lst1 )
        VCmd.SetIntValue( var5, r"NumberSelected", 1 )
        lst1_count,lst1 =  VScn.List( "  N {} ".format(nid)  )
        VCmd.SetObjectArrayValue( var5, r"EntitiesSelected", lst1_count, lst1 )
        VCmd.SetIntValue( var5, r"ConvertOption", 1 )
        ret=VCmd.ExecuteCommand( var5, r"ConvertCnodetoNode" )
        VCmd.Quit( var5 )


    def node_to_cnode(self, NID):

        node_obj = self.get_object(NID)

        nid = VistaDb.GetId(node_obj)

        var1=VCmd.Activate(0 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
        var5=VCmd.Activate( 0, r"VCPUtilities.VCPUtilInterface", r"ConvertNodes" )
        lst1_count,lst1 =  VScn.List( "  N {} ".format(nid)  )
        VCmd.SetObjectArrayValue( var1, r"GraphicSelection",  lst1_count , lst1 )
        VCmd.SetIntValue( var5, r"NumberSelected", 1 )
        lst1_count,lst1 =  VScn.List( "  N {} ".format(nid)  )
        VCmd.SetObjectArrayValue( var5, r"EntitiesSelected", lst1_count, lst1 )
        VCmd.SetIntValue( var5, r"ConvertOption", 0 )
        ret=VCmd.ExecuteCommand( var5, r"ConvertNodetoCnode" )
        VCmd.Quit( var5 )


    def __get(self,NID):
        ''' Get object and coordinate from node id '''
        #NID TYPE CHECK
        try :

            if str(type(NID)) == "<class 'int'>" :
                input_value = NID
                node_obj = VistaDb.ModelGetNodeFromID(self.model, input_value)
            elif checkNodeClass(NID) == True: 
                input_value = VistaDb.GetId(NID)
                node_obj = VistaDb.ModelGetNodeFromID(self.model, input_value)
            elif checkPointClass(NID) == True: 
                node_obj = NID
            else :
                raise Exception('NID TYPE ERROR') 

        except Exception as e:
            print(e)
            return None, None


        try :
            if node_obj is not None:
                pnt = VistaDb.GetVgPoint3Value(node_obj,"Point")
                return node_obj, pnt
            else :
                raise Exception('NODE ID:{} is not exists.'.format(input_value)) 
        except Exception as e:
            print(e)
            return None, None

    def copy(self, obj):
        from visualenv.dbs.model.FindNewObjects import FindNewObjects
        import VHostManager
        entity_finder = FindNewObjects(self.model, "FeNodeClass")
        if isinstance(obj, list):
            VHostManager.CopyEntities(len(obj),obj)
            VHostManager.PasteEntities()
        else:
            objlist = list(obj)
            VHostManager.CopyEntities(len(objlist),objlist)
            VHostManager.PasteEntities()
        newLst = entity_finder.getNewObjects()
        return newLst

    def delete(self, obj):
        nid_list = self.list_check(obj)
        if isinstance(nid_list, list):
            VistaDb.ModelDestroyObjects(self.model,len(nid_list),nid_list)
        else:
            objlist = list(nid_list)
            VistaDb.ModelDestroyObjects(self.model,len(nid_list),nid_list)

    def list_check(self, mylist):

        if isinstance(mylist, list):
            nlist = [x for x in mylist if checkNodeClass(x)]
            if len(nlist) == 0:
                nlist = [ VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",x) for x in mylist ]

            return nlist

        elif isinstance(mylist, int):
            nlist = [ VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",mylist) ]
            return nlist

        elif checkNodeClass(mylist):
            nlist = [ mylist ]
            return nlist
        else:
            print("type error")
            return


    def locate(self,nid):
        ''' Show selected node id '''

        nlist = self.list_check(nid)

        if nlist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(nlist), nlist )
            ret=VCmd.ExecuteCommand( display_command, r"Locate" )


    def show(self,nid):

        nlist = self.list_check(nid)

        if nlist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(nlist), nlist )
            ret=VCmd.ExecuteCommand( display_command, r"ShowSelected" )


    def hide(self,nid):

        nlist = self.list_check(nid)

        if nlist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(nlist), nlist )
            ret=VCmd.ExecuteCommand( display_command, r"HideSelected" )

    def get_point_object(self,NID):

        node_object, point = self.__get(NID)
        if node_object:
            return point
        else:
            return None

    def get_object(self,NID):
        '''get_object(NID)  Get object from node id '''
        node_object, point = self.__get(NID)
        if node_object:
            return node_object
        else:
            return None

    def get_coordinate(self,NID):
        '''get_coordinate(NID)  Get coordinate from node id '''
        node_object, point = self.__get(NID)

        if node_object:
            return point.x, point.y, point.z
        else:
            return None


    def get_nodes_from_element(self, elist):
#        _, elems_node_list = VistaDb.ModelGetNodesfromElementList(len(elist) ,elist)
        node_set = set()
        if isinstance(elist, list):
            for elist_item in elist:

                if checkElementClass(elist_item):
                    elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elist_item)
                    for node_id in node_id_list:
                        node_obj = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",node_id)
                        node_set.add(node_obj)

                elif checkInteger(elist_item):
                    elem_obj = VistaDb.ModelGetObjectFromId(self.model, "FeElementClass", elist_item)
                    elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
                    for node_id in node_id_list:
                        node_obj = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",node_id)
                        node_set.add(node_obj)

        elif checkElementClass(elist):
            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elist)
            for node_id in node_id_list:
                node_obj = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",node_id)
                node_set.add(node_obj)

        elif isinstance(elist, int):
            elem_obj = VistaDb.ModelGetObjectFromId(self.model, "FeElementClass", elist)
            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
            for node_id in node_id_list:
                node_obj = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",node_id)
                node_set.add(node_obj)

        else:
            raise Exception("type error")

        return list(node_set)

    def get_nodes_from_part(self,plist):
        """ get_nodes_from_part(plist) pid, pid_list, part_object are all availible """
        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",i)
                        part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",plist)
                part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        part_list = list(part_set)
        num_parts = len(part_set)

        if part_list:
            pnt_num,pnt_list = VistaDb.ModelGetEntityNodes(self.model,num_parts,part_list)
            return pnt_list
        else:
            return None

    def create(self,cx,cy,cz,nid=None, show=False):
        """ create(cx, cy, cz, nid=None) """

        try :
            if nid :
                node = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",nid)

                if node:
                    raise Exception('Node number already exists')
                else :
                    NID = nid
                    create_node =  VistaDb.ModelCreateNode(self.model,NID,cx,cy,cz)
                    VToolKit.UpdateRanges( self.model,1,[create_node])
                    if show:
                        self.show(create_node)
                    return create_node

            else :
                NID = VistaDb.ModelGetUniqueId(self.model,"FeNodeClass",0)
                create_node =  VistaDb.ModelCreateNode(self.model,NID,cx,cy,cz)
                VToolKit.UpdateRanges( self.model,1,[create_node])
                if show:
                    self.show(create_node)
                return create_node

        except Exception as e:
            return print(e)
#

    def on_curve(self, curve_obj, num=2):
        from visualenv.dbs.model.FindNewObjects import FindNewObjects
        entity_finder = FindNewObjects(self.model, "FeNodeClass")

        NID = VistaDb.ModelGetUniqueId(self.model,"FeNodeClass",0)
        VhmCommand=VCmd.Activate(1 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
        node_on_curve=VCmd.Activate( 0, r"VMeshModeler.VmmICommandGui", r"NodesOnCurve" )
        VCmd.SetStringValue( VhmCommand, r"TargetName", r"Curve" )

        if isinstance(curve_obj, list) and len(curve_obj) > 1 :
            if len(curve_obj) > 1 :
                for  i in curve_obj:
                    curve_id = VistaDb.GetId(i)
                    VCmd.SetStringValue( VhmCommand, r"IdRange", str(curve_id) )
            else:
                curve_id = VistaDb.GetId(curve_obj[0])
                VCmd.SetStringValue( VhmCommand, r"IdRange", str(curve_id) )
        else:
            curve_id = VistaDb.GetId(curve_obj)
            VCmd.SetStringValue( VhmCommand, r"IdRange", str(curve_id) )
            
        VCmd.SetIntValue( node_on_curve, r"NumberOfNodes", num )
        VCmd.SetIntValue( node_on_curve, r"NodeStartID", NID )
        ret=VCmd.ExecuteCommand( node_on_curve, r"UpdateSelection" )
        VCmd.Accept( node_on_curve )
        VCmd.Cancel( node_on_curve )
        VCmd.Quit( node_on_curve )

        node_obj_list = entity_finder.getNewObjects()
        VToolKit.UpdateRanges( self.model,len(node_obj_list),node_obj_list)

        return node_obj_list

    def between_2nodes(self, N1, N2):

        n1x, n1y, n1z = self.get_coordinate(N1)
        n2x, n2y, n2z = self.get_coordinate(N2)

        new_x = (n2x+n1x)/2
        new_y = (n2y+n1y)/2
        new_z = (n2z+n1z)/2
        
        new_nid = self.create(new_x, new_y, new_z)
        node_obj = self.get_object(new_nid) 
        VToolKit.UpdateRanges( self.model,1,[node_obj])
        return node_obj

    def get_mid_2nodes(self, N1, N2):

        n1x, n1y, n1z = self.get_coordinate(N1)
        n2x, n2y, n2z = self.get_coordinate(N2)

        new_x = (n2x+n1x)/2
        new_y = (n2y+n1y)/2
        new_z = (n2z+n1z)/2
        
        return new_x, new_y, new_z

    def pair_list(self, nlist1, nlist2, tol=0.5):

        out_list =[]
        for i in nlist1:
            point = VistaDb.ModelGetNodeFromID(self.model, i)
            min_value_obj = VistaDb.GetNearestNodeFromPoint(len(nlist2), nlist2, point, tol)
            out_list.append([i,min_value_obj])
        return out_list
    
    def get_boundary_nodes(self, elem_obj):
        num_list = len(elem_obj)
        ret1, ret2, BoundaryNodeList= VistaDb.ElementGetBoundaryNodes(num_list,elem_obj)
        return BoundaryNodeList

    def drop_nodes_on_curve(self, node_obj, curve_obj):
        EntitySelector = VCmd.Activate( 0, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
        dropGui = VCmd.Activate( 0, r"VMeshModeler.VmmICommandGui", r"DropEntities" )
        VCmd.SetStringValue( dropGui, r"SelectionType", r"Node" )
        VCmd.SetStringValue( dropGui, r"CopyOrMoveOpt", "'Move" )
        VCmd.SetObjectArrayValue( EntitySelector, r"GraphicSelection",  len(node_obj), node_obj )
        ret=VCmd.ExecuteCommand( dropGui, r"UpdateSourceEntities" )
        VCmd.SetStringValue( dropGui, r"DirectionOfDropOpt", r"AlongTargetNormal" )
        VCmd.SetStringValue( dropGui, r"TargetEntityType", "Curve" )
        VCmd.SetObjectArrayValue( EntitySelector, r"GraphicSelection",  len(curve_obj), curve_obj )
        ret=VCmd.ExecuteCommand( dropGui, r"UpdateTargetEntities" )

        VCmd.Accept( dropGui )
        VCmd.Quit( dropGui )    

    def projection_on_plane_normal(self, node_list, plane_x, plane_y, plane_z, d_constant ):
        input_plane = VgPoint3(plane_x, plane_y, plane_z)
        ret,normalised_plane = VistaDb.MathNormaliseVector(input_plane)

        for i in node_list:
            node = i
            pnt = VistaDb.GetVgPoint3Value(node,"Point")
            ret, normal_distance = VistaDb.MathGetDistanceOfPointFromPlane(plane_x,plane_y,plane_z,d_constant,pnt)

            distance_x =  normalised_plane.x * normal_distance
            distance_y =  normalised_plane.y * normal_distance
            distance_z =  normalised_plane.z * normal_distance
            x = pnt.x - distance_x
            y = pnt.y - distance_y
            z = pnt.z - distance_z
            VistaDb.SetVgPoint3Value(node, "Point", VgPoint3(x,y,z))
        #part update
        part_num,part_obj = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
        VHostManager.UpdateDisplayOfGivenParts(self.model,part_num,part_obj)
        VHostManager.ModelDraw(self.model)

    def projection_on_plane_vector(self, node_list, plane_x, plane_y, plane_z, d_constant, vect_n1, vect_n2 ):

        user_n1= VistaDb.GetVgPoint3Value(vect_n1,"Point")
        user_n2= VistaDb.GetVgPoint3Value(vect_n2,"Point")
        ret,user_vector = VistaDb.MathComputeVector(user_n1,user_n2)
        ret,normalised_vector = VistaDb.MathNormaliseVector(user_vector)

        for i in node_list:
            node = i
            pnt = VistaDb.GetVgPoint3Value(node,"Point")

            #plane equation
            numerator = (d_constant + plane_x * pnt.x + plane_y * pnt.y + plane_z * pnt.z)  
            #line equation
            denominator = (plane_x * normalised_vector.x + plane_y * normalised_vector.y + plane_z * normalised_vector.z )
            #distance from point to plane
            dist_u = numerator/denominator

            distance_x =  normalised_vector.x * dist_u
            distance_y =  normalised_vector.y * dist_u
            distance_z =  normalised_vector.z * dist_u
            x = pnt.x - distance_x
            y = pnt.y - distance_y
            z = pnt.z - distance_z
            VistaDb.SetVgPoint3Value(node, "Point", VgPoint3(x,y,z))
        #part update
        part_num,part_obj = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
        VHostManager.UpdateDisplayOfGivenParts(self.model,part_num,part_obj)
        VHostManager.ModelDraw(self.model)

    def get_nearest_node(self, nodes, chkpoint):

        mindist = 1000000.0
        output = None

        if(nodes == None or len(nodes) < 1 or chkpoint == None):
            return None , None

        checkpoint  = VistaDb.GetVgPoint3Value(chkpoint,"Point")

        for i in nodes:
            pnt_obj  = VistaDb.GetVgPoint3Value(i,"Point")
            dist = VistaDb.MathGetDistanceBetweenTwo3DPoints(pnt_obj, checkpoint)
            if(dist < mindist):
                mindist = dist
                output = i

        return output

    def sort_nodes_by_distance(self, nlist, base):

        sort_list = []

        while nlist:

            min_obj =  self.get_nearest_node(nlist, base )
            sort_list.append(min_obj)
            nlist.pop(nlist.index(min_obj))

            base = min_obj

        return sort_list

    def delete_free_node(self):
        # delete free node
        var2=VCmd.Activate( 0, r"VModelValidate.VUnAttachedElementInterface", r"UnAttachedElements" )
        VCmd.ExecuteCommand( var2, r"CheckLooseEnt" )
        VCmd.ExecuteCommand( var2, r"UnAttachDelSelAll" )
        VCmd.ExecuteCommand( var2, r"UnAttachNodeDel" )
        VCmd.Quit( var2 )

    def coincident_nodes(self, node_obj_list, base_parts, move_parts):

        _, base_node_part = VistaDb.ModelGetEntityNodes(vista_model,len(base_parts),base_parts)
        _, move_node_part = VistaDb.ModelGetEntityNodes(vista_model,len(move_parts),move_parts)

        base_node_list = [ x for x in node_obj_list if x in base_node_part ]
        move_node_list = [ x for x in node_obj_list if x in move_node_part ]

        nid_list = [ VistaDb.GetId(x) for x in node_obj_list ]

        base_pnt_obj_list = [ VistaDb.GetVgPoint3Value(x,"Point") for x in base_node_list ]
        move_pnt_obj_list = [ VistaDb.GetVgPoint3Value(x,"Point") for x in move_node_list ]

        base_coordinate_pnt_list = [ [x.x, x.y, x.z] for x in base_pnt_obj_list ]
        move_coordinate_pnt_list = [ [x.x, x.y, x.z] for x in move_pnt_obj_list ]

        stator_coordinate_array = np.array(base_coordinate_pnt_list)
        motor_coordinate_array = np.array(move_coordinate_pnt_list)

        tree = cKDTree(move_coordinate_array)
        dist, idxs = tree.query(base_coordinate_array)

        for node_obj, idx in zip(base_node_list, idxs):
            target_motor_node = move_node_list[idx]
            pnt_obj = VistaDb.GetVgPoint3Value(node_obj,"Point")
            VistaDb.SetVgPoint3Value(target_motor_node, "Point", pnt_obj)

    def all_coordinate_list(self):
        node_num,node_obj_list = VistaDb.ModelGetObjectList(self.model,"FeNodeClass") 
        pnt_obj_list = [ VistaDb.GetVgPoint3Value(x,"Point") for x in node_obj_list ]
        coordinate_pnt_list = [ [x.x, x.y, x.z] for x in pnt_obj_list ]
        return coordinate_pnt_list
    
    def get_bounding_box(self):
        coordinate = self.all_coordinate_list()

        if not coordinate:   # 빈 리스트
            self.xmin = self.ymin = self.zmin = None
            self.xmax = self.ymax = self.zmax = None
            return False

        coordinate_array = np.array(coordinate)
        xmin, ymin, zmin = coordinate_array.min(axis=0)
        xmax, ymax, zmax = coordinate_array.max(axis=0)   
        self.xmin = xmin
        self.ymin = ymin
        self.zmin = zmin
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        return xmin, xmax, ymin, ymax, zmin, zmax


    def get_bbox_corner_nodes(self, tol=1e-6):
        node_num, node_obj_list = VistaDb.ModelGetObjectList( self.model, "FeNodeClass")

        # 좌표 추출
        pnt_obj_list = [VistaDb.GetVgPoint3Value(x, "Point") for x in node_obj_list]
        coords = np.array([[p.x, p.y, p.z] for p in pnt_obj_list])

        xmin, ymin, zmin = coords.min(axis=0)
        xmax, ymax, zmax = coords.max(axis=0)

        # convenience
        def find_closest(mask, target_y, target_z):
            idx = np.where(mask)[0]
            sub = coords[idx]
            dist = (sub[:,1] - target_y)**2 + (sub[:,2] - target_z)**2
            return idx[np.argmin(dist)]

        result_nodes = []

        # ---------- xmin 면 (4개) ----------
        mask_xmin = np.abs(coords[:,0] - xmin) < tol

        for (y, z) in [(ymin, zmin), (ymin, zmax),
                       (ymax, zmin), (ymax, zmax)]:
            i = find_closest(mask_xmin, y, z)
            result_nodes.append(node_obj_list[i])

        # ---------- xmax 면 (4개) ----------
        mask_xmax = np.abs(coords[:,0] - xmax) < tol

        for (y, z) in [(ymin, zmin), (ymin, zmax),
                       (ymax, zmin), (ymax, zmax)]:
            i = find_closest(mask_xmax, y, z)
            result_nodes.append(node_obj_list[i])

        return result_nodes


    def node_refresh(self):
        part_num,part_obj = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
        VHostManager.UpdateDisplayOfGivenParts(self.model,part_num,part_obj)
        VHostManager.ModelDraw(self.model)

    def node_coordinate_modify(self, node_id_list, final_point_list):

        for nid, pnt_obj in zip(node_id_list,final_point_list):
            node_obj = VistaDb.ModelGetNodeFromID(self.model, nid)
            if checkPointClass(pnt_obj):
                VistaDb.SetVgPoint3Value(node_obj, "Point", pnt_obj)
            else:
                x,y,z = pnt_obj
                VistaDb.SetVgPoint3Value(node_obj, "Point", VgPoint3(x, y, z))

        self.node_refresh()
    
    def get_nodes_by_user_box( self, cog, pid_list, vector, length, depth=5.0, shape="box"):
        """
        Select nodes inside a user-defined section volume.

        Parameters
        ----------
        cog : [x,y,z]
            Section center/start point.

        pid_list : list[int]
            Part ID list.

        vector : str
            Extrusion direction.

            Supported:
                x, y, z
                +x, +y, +z
                -x, -y, -z

        shape : str

            box
                Square section.

                width  = length
                height = length

                Depth direction = vector

            circle
                Cylindrical section.

                radius = length

                Depth direction = vector

        length : float

            box:
                square side length

            circle:
                cylinder radius

        depth : float

            Extrusion depth along vector.

        Examples
        --------

        Example 1
        ---------

        Parts:
            11,12

        Start plane:
            x = -1000

        Direction:
            +X

        shape="box"
        length=100
        depth=200

        Creates:

            100 x 100 square section

        extruded 200 units along +X.

        Example 2
        ---------

        Parts:
            11,12

        Start plane:
            x = -1000

        Direction:
            +X

        shape="circle"
        length=50
        depth=200

        Creates:

            radius = 50

        cylinder extruded 200 units along +X.

        Returns
        -------
        list[int]
            Selected node IDs.
        """

        import math

        def _to_xyz(p):
            try:
                return as_xyz(p)
            except Exception:
                pass

            if hasattr(p, "x"):
                return ( float(p.x), float(p.y), float(p.z))

            return ( float(p[0]), float(p[1]), float(p[2]))

        def _dot(a, b):
            return ( a[0] * b[0] +
                a[1] * b[1] +
                a[2] * b[2]
            )

        def _cross(a, b):
            return (
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0],
            )

        def _norm(v):
            return math.sqrt(_dot(v, v))

        def _normalize(v):

            n = _norm(v)

            if n <= 1.0e-12:
                raise ValueError("zero vector")

            return ( v[0] / n, v[1] / n, v[2] / n,)

        def _parse_vector(v):

            if not isinstance(v, str):
                return _normalize(_to_xyz(v))

            s = str(v).strip().lower()

            mapping = {
                "x":  ( 1, 0, 0),
                "+x": ( 1, 0, 0),
                "-x": (-1, 0, 0),

                "y":  ( 0, 1, 0),
                "+y": ( 0, 1, 0),
                "-y": ( 0,-1, 0),

                "z":  ( 0, 0, 1),
                "+z": ( 0, 0, 1),
                "-z": ( 0, 0,-1),
            }

            if s not in mapping:
                raise ValueError(
                    "vector must be x,y,z,+x,+y,+z,-x,-y,-z"
                )

            return mapping[s]

        cog = _to_xyz(cog)

        axis = _normalize(
            _parse_vector(vector)
        )

        length = float(length)
        depth = float(depth)

        shape = str(shape).lower()

        if length <= 0.0:
            raise ValueError("length must be > 0")

        if depth <= 0.0:
            raise ValueError("depth must be > 0")

        if shape not in ("box", "circle"):
            raise ValueError(
                "shape must be box or circle"
            )

        # box = side length
        half_size = length * 0.5

        # circle = radius
        radius = length

        if abs(axis[0]) < 0.9:
            ref = (1.0, 0.0, 0.0)
        else:
            ref = (0.0, 1.0, 0.0)

        v1 = _normalize(
            _cross(axis, ref)
        )

        v2 = _normalize(
            _cross(axis, v1)
        )
        node_obj_list = self.get_nodes_from_part(pid_list)
        nid_list = [VistaDb.GetId(x) for x in node_obj_list]
        coordinate_list = [ [pt.x, pt.y, pt.z] for pt in (VistaDb.GetVgPoint3Value(n, "Point") for n in nodes_list) ]
        coordinate_array = np.array(coordinate_list)

        selected_nid_list = []

        for nid, coord in zip( nid_list, coordinate_array):

            x, y, z = _to_xyz(coord)

            rel = ( x - cog[0], y - cog[1], z - cog[2],)

            axial = _dot(rel, axis)

            if axial < 0.0:
                continue

            if axial > depth:
                continue

            s1 = _dot(rel, v1)
            s2 = _dot(rel, v2)

            if shape == "box":

                if (
                    abs(s1) <= half_size and
                    abs(s2) <= half_size
                ):
                    selected_nid_list.append(int(nid))

            else:

                r2 = s1 * s1 + s2 * s2

                if r2 <= radius * radius:
                    selected_nid_list.append(int(nid))

        return selected_nid_list
