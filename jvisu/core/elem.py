from jvisu.core.check import checkNodeClass , checkElementClass, checkPartClass 
import VistaDb
import VCmd
import numpy as np
from jvisu.core.part import part as visual_part
from jvisu.config.type_dict import ELEMENT_TYPE
import VExpMngr
import VMeshMdlr

class element:

    def __init__(self, model=None):
        self.model = model
        self._part = visual_part(self.model)
    
    def __get(self,EID):
        '''
        Get object and node list from element id 
        '''
        #EID TYPE CHECK
        try :

            if str(type(EID)) == "<class 'int'>" :
                input_value = EID
            elif checkElementClass(EID) == True: 
#                input_value = VistaDb.GetId(EID)
                return EID
            else :
                raise Exception('EID TYPE ERROR') 

        except Exception as e:
            print(e)
            return None

        elem_obj = VistaDb.ModelGetObjectFromId(self.model, "FeElementClass", input_value)
        return elem_obj

#        if elem_obj != None:
##            ret ,num, elem_nodes = VistaDb.ElementGetNodeList(elem_obj)
#            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
#            return elem_obj, elem_id , part_id , num_nodes, node_id_list
#        else :
#            print('ELEMENT ID:{} is not exists.'.format(input_value)) 
#            return None, None,None,None,None

    def get_object(self, EID):
        '''get_object(EID)  Get object from element id '''
        elem_obj = self.__get(EID)
        return elem_obj

    def get_partid(self, EID):
        '''get_partid(EID)  Get partid from element id '''
        elem_obj = self.__get(EID)

        if elem_obj != None:
#            ret ,num, elem_nodes = VistaDb.ElementGetNodeList(elem_obj)
            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
            return part_id 
    
    def get_normal(self, EID):
        elem_obj = self.__get(EID)
        ret, normal = VistaDb.ElementComputeNormal(elem_obj)
        pnt_obj = normal[0]
        output = np.array([ pnt_obj.x , pnt_obj.y, pnt_obj.z ])
        return output
    
    def get_nodelist(self, EID):
        elem_obj = self.__get(EID)

        if elem_obj != None:
#            ret ,num, elem_nodes = VistaDb.ElementGetNodeList(elem_obj)
            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
        return node_id_list

    def get_tria_area(self, n1, n2, n3 ):
        a = [n1.x, n1.y, n1.z]
        b = [n2.x, n2.y, n2.z]
        c = [n3.x, n3.y, n3.z]
        ab = np.array(b) - np.array(a)
        ac = np.array(c) - np.array(a)
        cross_product = np.cross(ab, ac)
        return 0.5 * np.linalg.norm(cross_product)

    def get_area(self, elem_obj):

        n1 = VistaDb.GetObjectValue(elem_obj, "N1")
        n2 = VistaDb.GetObjectValue(elem_obj, "N2")
        n3 = VistaDb.GetObjectValue(elem_obj, "N3")
        n4 = VistaDb.GetObjectValue(elem_obj, "N4")  # 사각형 쉘 요소일 수 있음

        if n4:  # 사각형 쉘인 경우 두 개의 삼각형으로 분리
            pnt1 = VistaDb.GetVgPoint3Value(n1, "Point")
            pnt2 = VistaDb.GetVgPoint3Value(n2, "Point")
            pnt3 = VistaDb.GetVgPoint3Value(n3, "Point")
            pnt4 = VistaDb.GetVgPoint3Value(n4, "Point")
            area1 = self.get_tria_area(pnt1,pnt2,pnt3)
            area2 = self.get_tria_area(pnt1,pnt3,pnt4)
            return area1+area2

        else:  # 삼각형 쉘인 경우
            pnt1 = VistaDb.GetVgPoint3Value(n1, "Point")
            pnt2 = VistaDb.GetVgPoint3Value(n2, "Point")
            pnt3 = VistaDb.GetVgPoint3Value(n3, "Point")
            return self.get_tria_area(pnt1,pnt2,pnt3)


    def get_tria_projected_area(self, n1, n2, n3, axis):

        a = np.array([n1.x, n1.y, n1.z])
        b = np.array([n2.x, n2.y, n2.z])
        c = np.array([n3.x, n3.y, n3.z])

        ab = b - a
        ac = c - a

        cross_product = np.cross(ab, ac)

        axis = np.asarray(axis, dtype=float)
        axis /= np.linalg.norm(axis)

        return 0.5 * abs(np.dot(cross_product, axis))

    def get_projected_area(self, elem_obj, axis):
        # z축 투영
        #area = self.get_projected_area(elem, [0, 0, 1])

        # x축 투영
        #area = self.get_projected_area(elem, [1, 0, 0])

        # y축 투영
        #area = self.get_projected_area(elem, [0, 1, 0])

        # 임의 방향
        #area = self.get_projected_area(elem, [1, 1, 1])

        n1 = VistaDb.GetObjectValue(elem_obj, "N1")
        n2 = VistaDb.GetObjectValue(elem_obj, "N2")
        n3 = VistaDb.GetObjectValue(elem_obj, "N3")
        n4 = VistaDb.GetObjectValue(elem_obj, "N4")

        pnt1 = VistaDb.GetVgPoint3Value(n1, "Point")
        pnt2 = VistaDb.GetVgPoint3Value(n2, "Point")
        pnt3 = VistaDb.GetVgPoint3Value(n3, "Point")

        if n4:
            pnt4 = VistaDb.GetVgPoint3Value(n4, "Point")

            area1 = self.get_tria_projected_area(
                pnt1, pnt2, pnt3, axis
            )
            area2 = self.get_tria_projected_area(
                pnt1, pnt3, pnt4, axis
            )

            return area1 + area2

        else:
            return self.get_tria_projected_area(
                pnt1, pnt2, pnt3, axis
            )


    def get_lengths_list(self, obj_list):
        # 노드 좌표 DB 구성
        _, node_obj_list = VistaDb.ModelGetObjectList(self.model, "FeNodeClass")
        nid_list = [VistaDb.GetId(x) for x in node_obj_list]
        pnt_obj_list = [VistaDb.GetVgPoint3Value(node, "Point") for node in node_obj_list]

        # nid -> (x, y, z) 매핑
        coords = {nid: (pnt.x, pnt.y, pnt.z) for nid, pnt in zip(nid_list, pnt_obj_list)}

        lengths = []

        for elem in obj_list:
            # 요소 연결 정보 가져오기
            _, _, n, nids = VistaDb.ElementGetData(elem)

            # 요소를 구성하는 좌표 배열
            pts = [np.array(coords[nid]) for nid in nids]

            # 변 길이 계산
            if n == 2:
                # 2-노드 선요소
                L = np.linalg.norm(pts[1] - pts[0])
                lengths.append(L)

            elif n == 3:
                # 삼각형 요소: 세 변 길이 중 최대
                d1 = np.linalg.norm(pts[1] - pts[0])
                d2 = np.linalg.norm(pts[2] - pts[1])
                d3 = np.linalg.norm(pts[0] - pts[2])
                lengths.append(max(d1, d2, d3))

            elif n == 4:
                # 사각형 요소: 네 변 길이 중 최대
                d1 = np.linalg.norm(pts[1] - pts[0])
                d2 = np.linalg.norm(pts[2] - pts[1])
                d3 = np.linalg.norm(pts[3] - pts[2])
                d4 = np.linalg.norm(pts[0] - pts[3])
                lengths.append(max(d1, d2, d3, d4))

            else:
                # 그 외 요소 (예: 고차원 요소) → 모든 노드쌍 거리 중 최대
                max_len = 0.0
                for i in range(n):
                    for j in range(i + 1, n):
                        d = np.linalg.norm(pts[j] - pts[i])
                        if d > max_len:
                            max_len = d
                lengths.append(max_len)

        return np.array(lengths)


    def get_areas_list(self, obj_list):
        # --- 노드 좌표 배열 ---
        _, node_obj_list = VistaDb.ModelGetObjectList(self.model, "FeNodeClass")
        nid_list = [VistaDb.GetId(x) for x in node_obj_list]
        pnt_obj_list = [VistaDb.GetVgPoint3Value(node, "Point") for node in node_obj_list]

        # nid → index 매핑
        nid_to_idx = {nid: i for i, nid in enumerate(nid_list)}
        coords = np.zeros((len(nid_list), 3))
        for i, p in enumerate(pnt_obj_list):
            coords[i] = (p.x, p.y, p.z)

        areas = []

        # --- 입력 obj_list 순서대로 처리 ---
        for elem in obj_list:
            _, _, n, nids = VistaDb.ElementGetData(elem)
            pts = coords[[nid_to_idx[nid] for nid in nids]]

            if n == 3:  # 삼각형
                A, B, C = pts
                area = 0.5 * np.linalg.norm(np.cross(B - A, C - A))
                areas.append(area)

            elif n == 4:  # 사각형 (두 삼각형 합)
                P1, P2, P3, P4 = pts
                area1 = 0.5 * np.linalg.norm(np.cross(P2 - P1, P3 - P1))
                area2 = 0.5 * np.linalg.norm(np.cross(P3 - P1, P4 - P1))
                areas.append(area1 + area2)

            else:
                raise ValueError(f"지원하지 않는 요소: {n} 노드")

        return np.array(areas)


    def reverse_split(self, elem_obj1, elem_obj2):

        e1_n1 = VistaDb.GetObjectValue(elem_obj1, "N1")
        e1_n2 = VistaDb.GetObjectValue(elem_obj1, "N2")
        e1_n3 = VistaDb.GetObjectValue(elem_obj1, "N3")
        e1_n4 = VistaDb.GetObjectValue(elem_obj1, "N4") 

        e1_list = [e1_n1, e1_n2, e1_n3, e1_n4 ]
        e1_set = set(e1_list)

        e2_n1 = VistaDb.GetObjectValue(elem_obj2, "N1")
        e2_n2 = VistaDb.GetObjectValue(elem_obj2, "N2")
        e2_n3 = VistaDb.GetObjectValue(elem_obj2, "N3")
        e2_n4 = VistaDb.GetObjectValue(elem_obj2, "N4") 

        e2_list = [e2_n1, e2_n2, e2_n3, e2_n4 ]
        e2_set = set(e2_list)

        shared_vertices = list(set(triangle1) & set(triangle2))

        # 2점 공유 여부 확인
        if len(shared_vertices) == 2 and len(e1_set) == 3 and len(e2_set) == 3:
            t1_unique = [p for p in e1_list if p not in shared_vertices][0]
            t2_unique = [p for p in e2_list if p not in shared_vertices][0]
            VistaDb.SetObjectValue(elem_obj1, "N1", shared_vertices[0])
            VistaDb.SetObjectValue(elem_obj1, "N2", t2_unique)
            VistaDb.SetObjectValue(elem_obj1, "N3", shared_vertices[1])
            VistaDb.SetObjectValue(elem_obj1, "N4", shared_vertices[1])
            VistaDb.SetObjectValue(elem_obj2, "N1", shared_vertices[1])
            VistaDb.SetObjectValue(elem_obj2, "N2", t1_unique)
            VistaDb.SetObjectValue(elem_obj2, "N3", shared_vertices[0])
            VistaDb.SetObjectValue(elem_obj2, "N4", shared_vertices[0])
        else:
            print(f"Number of shared vertices: {len(shared_vertices)} (or not a triangle)")


    def get_longest_length(self, elem_obj):
        minLength, minEle,maxLength,maxele = VistaDb.ElementsGetMinMaxLength(1,[elem_obj])
        return maxLength

    def get_shortest_length(self, elem_obj):
        minLength, minEle,maxLength,maxele = VistaDb.ElementsGetMinMaxLength(1,[elem_obj])
        return minLength


    def get_nodelist_of_elements(self, EID):

        elem_set = set()
        node_set = set()
        try :
            if isinstance(EID, list):
                for i in EID:
                    if checkElementClass(i):
                        elem_set.add(i)
                    if isinstance(i, int):
                        elem = self.get_object(i)
                        elem_set.add(elem)

            elif checkElementClass(EID):
                elem_set.add(EID)

            elif isinstance(EID, int):
                elem = self.get_object(EID)
                elem_set.add(elem)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        elem_list = list(elem_set)

        if elem_list:
            for elem_obj in elem_list:
                elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
                for i in node_id_list:
                    node_set.add(i)

        return list(node_set)

    def get_volume(self, EID):
        elem_obj = self.__get(EID)
        vol = VistaDb.ElementComputeVolume(elem_obj )
        return vol

    def get_volume_list(self, EID):
        elem_obj_list = [ self.__get(x) for x in EID]
        vol = [ VistaDb.ElementComputeVolume(elem_obj ) for elem_obj in elem_obj_list]
        return vol

    def get_elements_cog(self, EID):
        elem_obj_list = [ self.__get(x) for x in EID]

        nodes_set = set()
        for elem_obj in elem_obj_list:
            elem_id , part_id , num_nodes, node_id_list = VistaDb.ElementGetData(elem_obj)
            node_obj_list = [ VistaDb.ModelGetObjectFromId(vistamodel,"FeNodeClass",nid) for nid in node_id_list ]
            nodes_set.update(node_obj_list)

        node_list = list(nodes_set)
        num_node = len(node_list)

        cog_coord = VistaDb.NodesGetCg(num_node,node_list)
        return cog_coord


    def copy(self, obj):
        from visualenv.dbs.model.FindNewObjects import FindNewObjects
        import VHostManager
        entity_finder_quad = FindNewObjects(self.model, "FeQuadClass")
        entity_finder_tria = FindNewObjects(self.model, "FeTriaClass")
        if isinstance(obj, list):
            VHostManager.CopyEntities(len(obj),obj)
            VHostManager.PasteEntities()
        else:
            objlist = list(obj)
            VHostManager.CopyEntities(len(objlist),objlist)
            VHostManager.PasteEntities()
        new_quad = entity_finder_quad.getNewObjects()
        new_tria = entity_finder_tria.getNewObjects()
        new_list = new_quad + new_tria
        pid = VistaDb.ModelGetUniqueId(self.model, "FePartClass", 0)
        VistaDb.ModelMoveElementsToPart(self.model, len(new_list), new_list, pid)
        VExpMngr.RefreshExplorer( r"Parts" )
        return new_list

    def delete(self, obj):
        if isinstance(obj, list):
            VistaDb.ModelDestroyObjects(self.model,len(obj),obj)
        else:
            objlist = list(obj)
            VistaDb.ModelDestroyObjects(self.model,len(objlist),objlist)

    def change_pid(self, EID, PID):

        elem_set = set()
        try :
            if isinstance(EID, list):
                for i in EID:
                    if checkElementClass(i):
                        elem_set.add(i)
                    if isinstance(i, int):
                        elem = self.get_object(i)
                        elem_set.add(elem)

            elif checkElementClass(EID):
                elem_set.add(EID)

            elif isinstance(EID, int):
                elem = self.get_object(EID)
                elem_set.add(elem)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        part_obj = self._part.get_object(PID)

        elem_num = len(elem_set)
        elem_list = list(elem_set)

        if part_obj:
            VistaDb.ModelMoveElementsToPart(self.model, elem_num, elem_list, PID)
            VExpMngr.RefreshExplorer( r"Parts" )

    def get_element_from_part(self,plist):
        ''' get element_from_part(plist) Parts, parts list, and part objects are all availible '''

        part_set = set()
        try :
            if isinstance(plist, list):
                for i in plist:
                    if checkPartClass(i):
                        part_set.add(i)
                    if isinstance(i, int):
                        part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",i)
                        if part != None:
                            part_set.add(part)

            elif checkPartClass(plist):
                part_set.add(plist)

            elif isinstance(plist, int):
                part = VistaDb.ModelGetObjectFromId(self.model,"FePartClass",plist)
                if part != None:
                    part_set.add(part)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        part_list = list(part_set)
        num_parts = len(part_set)

        if part_list :
            ele_num, ele_list = VistaDb.ModelGetElementsFromObjects(self.model,num_parts,part_list)
            return ele_list
        else:
            print('PART ID:{} is not exists.'.format(plist)) 
            return None

    def cog(self,EID):
        '''cog(EID)'''
        elem_obj = self.get_object(EID)

        if elem_obj != None:
            cog_coordinate = VistaDb.ElementGetCenterOfGravity(elem_obj)
            output = [ cog_coordinate.x,  cog_coordinate.y,  cog_coordinate.z ]
            return output
#
    def get_element_by_node(self,nlist):
        ''' get element_by_node(nlist) nid, nid list, node objects are all availible '''

        node_set = set()
        try :
            if isinstance(nlist, list):
                for i in nlist:
                    if checkNodeClass(i):
                        node_set.add(i)
                    if isinstance(i, int):
                        node = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",i)
                        if node != None:
                            node_set.add(node)

            elif checkNodeClass(nlist):
                node_set.add(nlist)

            elif isinstance(nlist, int):
                node = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",nlist)
                if node != None:
                    node_set.add(node)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        node_list = list(node_set)
        num_nodes = len(node_set)

        outlist = set()

        if node_list :
            VistaDb.FeModelBuildNodeToElementRelation(self.model,0,[])

            for i in node_list:
                num, numEle, eleList = VistaDb.GetElementsForNode(i)
                if eleList:
                    for j in eleList:
                        outlist.add(j)
            VistaDb.FeModelFreeNodeToElementRelation(self.model)

        if outlist:
            elist = [ VistaDb.GetId(x) for x in outlist ]
            return elist    
        else:
            print('NODE ID: {} has no attached elements.'.format(nlist)) 
            return None

    def list_check(self, mylist):

        if isinstance(mylist, list):
            elist = [x for x in mylist if checkElementClass(x)]
            if len(elist) == 0:
                elist = [ VistaDb.ModelGetObjectFromId(self.model,"FeElementClass",x) for x in mylist ]

            return elist

        elif isinstance(mylist, int):
            elist = [ VistaDb.ModelGetObjectFromId(self.model,"FeElementClass",mylist) ]
            return elist

        elif checkElementClass(mylist):
            elist = [ mylist ]
            return elist
        else:
            print("type error")
            return


    def locate(self,eid):

        elist = self.list_check(eid)

        if elist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(elist), elist )
            ret=VCmd.ExecuteCommand( display_command, r"Locate" )

    def show(self,eid):

        elist = self.list_check(eid)

        if elist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(elist), elist )
            ret=VCmd.ExecuteCommand( display_command, r"ShowSelected" )


    def hide(self,eid):

        elist = self.list_check(eid)

        if elist:
            display_command=VCmd.Activate( 1, r"VHostManagerPlugin.VhmInterface", r"VhmCommand" )
            VCmd.SetObjectArrayValue( display_command, r"ExplorerSelection", len(elist), elist )
            ret=VCmd.ExecuteCommand( display_command, r"HideSelected" )

    def smooth(self, elem_obj, fix_node = None):
        import VHostManager
        smooth_obj=VistaDb.CreateObject( r"QualEnhClass" )
        VistaDb.SetIntegerValue( smooth_obj, r"Num_Iterations", 10 )
        VistaDb.AppendObjectList( smooth_obj, r"Elements", len(elem_obj), elem_obj )

        if fix_node:
            VistaDb.AppendObjectList( smooth_obj, r"Fixed_Nodes", len(fix_node), fix_node )

        VistaDb.SetIntegerValue( smooth_obj, r"FeatureLineFlag", 0 )
        VistaDb.SetIntegerValue( smooth_obj, r"BoundaryFlag", 0 )
        VistaDb.SetDoubleValue( smooth_obj, r"FeatureLineAngle", 15  )
        VistaDb.SetIntegerValue( smooth_obj, r"Input_Type", 0 )
        VistaDb.SetIntegerValue( smooth_obj, r"OverallQualityEnh", 0 )
        VistaDb.SetIntegerValue( smooth_obj, r"DropNodesOnSurface", 0 )
        VistaDb.SetDoubleValue( smooth_obj, r"SnapTolToDropNodesOnSurf", 2.5  )
        VistaDb.SetObjectValue( smooth_obj, r"Model", self.model )
        ret=VistaDb.SmoothMeshQuality( smooth_obj )
        VistaDb.DestroyObject( smooth_obj )
        part_num,part_obj = VistaDb.ModelGetObjectList(self.model,"FePartClass") 
        VHostManager.UpdateDisplayOfGivenParts(self.model,part_num,part_obj)
        VHostManager.ModelDraw(self.model)

    def get_boundary_nodes(self, elem_obj):
        num_list = len(elem_obj)
        ret1, ret2 ,BoundaryNodeList= VistaDb.ElementGetBoundaryNodes(num_list,elem_obj)
        return BoundaryNodeList 

    def sort_quad_nodes(self, node_obj_list):
        """
        3D 공간상의 4개 점을 반시계 방향(CCW)으로 정렬.
        points: [(x1,y1,z1), (x2,y2,z2), (x3,y3,z3), (x4,y4,z4)]
        return: 정렬된 [(x,y,z), ...]
        """
        pnt_list = [ VistaDb.GetVgPoint3Value(x,"Point") for x in node_obj_list ]
        points = [ [pnt.x, pnt.y, pnt.z] for pnt in pnt_list ]

        pts = np.array(points)
        if pts.shape != (4, 3):
            raise ValueError("입력은 반드시 4개의 3D 좌표여야 합니다.")
        
        # 중심점
        center = np.mean(pts, axis=0)

        # 평면 법선 벡터 추정 (두 벡터의 외적)
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        
        # 국소 좌표계 생성 (u, v)
        # u: 첫 번째 점에서 두 번째 점 방향
        u = v1 / np.linalg.norm(v1)
        # v: normal과 u의 외적 → 평면 내에서 직교하는 방향
        v = np.cross(normal, u)
        v /= np.linalg.norm(v)
        
        # 각 점을 (u, v) 평면으로 투영
        local_coords = np.array([
            [np.dot(p - center, u), np.dot(p - center, v)] for p in pts
        ])
        
        # 중심 기준 각도 계산
        angles = np.arctan2(local_coords[:,1], local_coords[:,0])
        
        # 각도 기준 정렬
        sorted_indices = np.argsort(angles)
        sorted_pts = pts[sorted_indices]
        
        return [node_obj_list[idx] for idx in sorted_indices]


    def create_tetra(self, node_obj_list, pid, show=False):
        eid = VistaDb.ModelGetUniqueId(self.model,'FeElementClass',0)
        node_list = self.node_obj_list_check(node_obj_list)
        NewElement = VMeshMdlr.CreateTetra(self.model,pid,eid,len(node_list),node_list)
        if show:
            self.show(NewElement)
        return NewElement

    def create_hexa(self, node_obj_list, pid, show=False):
        eid = VistaDb.ModelGetUniqueId(self.model,'FeElementClass',0)
        node_list = self.node_obj_list_check(node_obj_list)
        NewElement = VMeshMdlr.CreateHexa(self.model,pid,eid,len(node_list),node_list)
        if show:
            self.show(NewElement)
#        import VCmdFramework
#        var1=VCmd.Activate(0 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
#        var32=VCmdFramework.Activate( r"MeshModeler", r"ByNodes", r"UI Shown" )
#        VCmd.SetStringValue( var1, r"TargetName", r"Part" )
#        VCmdFramework.SetIntValue( var32, r"PartID", pid )
#        VCmdFramework.SetIntValue( var32, r"AutoOrder", 1 )
#        lst1_count = len(node_list)
#        lst1 = node_list
#        VCmdFramework.SetObjectArrayValue( var32, r"NodeInput.GraphicSelection",  lst1_count , lst1 )
#        VCmdFramework.Quit( var32 )
        return NewElement

    def node_obj_list_check(self, node_list):
        node_set = set()
        for i in node_list:
            if checkNodeClass(i):
                node_set.add(i)
            if isinstance(i, int):
                node = VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",i)
                if node != None:
                    node_set.add(node)
        node_obj_list = list(node_set)
        return node_obj_list

    def create_penta(self, node_obj_list, pid, show=False):
        eid = VistaDb.ModelGetUniqueId(self.model,'FeElementClass',0)
        node_list = self.node_obj_list_check(node_obj_list)
        NewElement = VMeshMdlr.CreatePenta(self.model,pid,eid,len(node_list),node_list)
        if show:
            self.show(NewElement)
        return NewElement

    def create_quad(self, node_obj_list, pid, show=False):
        etype_num = ELEMENT_TYPE["SHELL4"]
        eid = VistaDb.ModelGetUniqueId(self.model,'FeElementClass',0)
        node_list = self.node_obj_list_check(node_obj_list)
        node_list = self.sort_quad_nodes( node_list)
#        NewElement = VMeshMdlr.CreatePenta(self.model,pid,eid,len(node_list),node_list)
        ret = VistaDb.ModelCreateShellElement( self.model, len(node_list), node_list, eid, etype_num, pid )
        NewElement = VistaDb.ModelGetObjectFromId(self.model, "FeElementClass", eid)

        if show:
            self.show(NewElement)

        return NewElement

    def create_tria(self, node_obj_list, pid, show=False):
        etype_num = ELEMENT_TYPE["SHELL3"]
        eid = VistaDb.ModelGetUniqueId(self.model,'FeElementClass',0)
        node_list = self.node_obj_list_check(node_obj_list)
        ret = VistaDb.ModelCreateShellElement( self.model, len(node_list), node_list, eid, etype_num, pid )
        NewElement = VistaDb.ModelGetObjectFromId(self.model, "FeElementClass", eid)
        if show:
            self.show(NewElement)
        return NewElement

    def create_bar(self, node_obj1, node_obj2, pid):
        import VHostManager
        etype_num = ELEMENT_TYPE["BAR"]
        bar_obj = VistaDb.CreateObject("FeBeamClass")
        eid  = VistaDb.ModelGetUniqueId(vista_model,"FeBeamClass",0)
        VistaDb.SetId(bar_obj,eid)
        VistaDb.SetIntegerValue(bar_obj,"Type",etype_num)

        VistaDb.SetObjectValue(bar_obj,"N1",node_obj1)
        VistaDb.SetObjectValue(bar_obj,"N2",node_obj2)
        VistaDb.SetObjectValue(bar_obj,"Part",pid)
        VistaDb.ModelAddElements(vista_model,1,[bar_obj])
        VHostManager.UpdateDisplayOfModifiedParts(self.model)
        return bar_obj


    def get_cog_array(self, elist, decimals=5):

        elem_set = set()
        try :
            if isinstance(elist, list):
                for i in elist:
                    if checkElementClass(i):
                        elem_set.add(i)
                    if isinstance(i, int):
                        elem = self.get_object(i)
                        elem_set.add(elem)

            elif checkElementClass(elist):
                elem_set.add(elist)

            elif isinstance(elist, int):
                elem = self.get_object(elist)
                elem_set.add(elem)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        elem_list = list(elem_set)

        if elem_list:
            coordinate_list = []
            eid_list = []

            for elem_obj in elem_list:
                cog_coordinate = VistaDb.ElementGetCenterOfGravity(elem_obj)
                eid_list.append(VistaDb.GetId(elem_obj))
                coordinate_list.append([cog_coordinate.x,cog_coordinate.y,cog_coordinate.z])

            coordinate_array = np.around(coordinate_list, decimals=decimals)
            return eid_list, elem_list, coordinate_array


    def get_coordinate_array(self, elist, decimals=5):

        elem_set = set()
        try :
            if isinstance(elist, list):
                for i in elist:
                    if checkElementClass(i):
                        elem_set.add(i)
                    if isinstance(i, int):
                        elem = self.get_object(i)
                        elem_set.add(elem)

            elif checkElementClass(elist):
                elem_set.add(elist)

            elif isinstance(elist, int):
                elem = self.get_object(elist)
                elem_set.add(elem)

            else:
                raise Exception("type error")

        except Exception as e:
            return print(e)

        elem_list = list(elem_set)
        eid_list = []

        if elem_list:
            coordinate_list = []
            nid_list = []

            for elem_obj in elem_list:
                eid_list.append(VistaDb.GetId(elem_obj))

                nlist = self.get_nodelist(elem_obj)
                node_obj_list = [ VistaDb.ModelGetObjectFromId(self.model,"FeNodeClass",x) for x in nlist ]
                for i in node_obj_list:
                    nid_list.append(VistaDb.GetId(i))
                    coordinate = VistaDb.GetVgPoint3Value(i,"Point")
                    coordinate_list.append([coordinate.x, coordinate.y, coordinate.z])

            coordinate_array = np.around(coordinate_list, decimals=decimals)  
            return nid_list, coordinate_array

    def get_group(self, elist):
        from group_elements.element_group_wrap import call_element_group_list
        eid_dict = { VistaDb.GetId(x):x for x in elist}
        vista_obj_eid_dict = {v: k for k, v in eid_dict.items()}

        connectivity_dict = { eid_dict[i]:j for i, _, _, j in (VistaDb.ElementGetData(x) for x in elist)}
        elements = [ (vista_obj_eid_dict[elem_obj], connectivity_dict[elem_obj] ) for elem_obj in elist ]

        connected_group_id_list = call_element_group_list(elements)

        output = [ [ eid_dict[y] for y in x] for x in connected_group_id_list ]
        return output


    def get_group_old(self, elist):
        from collections import defaultdict, deque

        eid_dict = { VistaDb.GetId(x):x for x in elist}
        connectivity_dict = { eid_dict[i]:j for i, _, _, j in (VistaDb.ElementGetData(x) for x in elist)}
        elements = [ (elem_obj, connectivity_dict[elem_obj] ) for elem_obj in elist ]

#        elements = [
#        (10, [1, 2, 3, 4]),
#        (20, [4, 5, 6, 7]),
#        (eid_obj3, [8, 9, 10, 11]),
#        (eid_obj4, [10, 12, 13, 14]) ]

        # 1. 노드 -> 요소 매핑
        node_to_eids = defaultdict(set)
        for eid, nids in elements:
            for nid in nids:
                node_to_eids[nid].add(eid)

        # 2. BFS를 이용한 연결 요소 그룹화
        visited = set()
        groups = []

        for eid, _ in elements:
            if eid not in visited:
                group = set()
                queue = deque([eid])
                visited.add(eid)

                while queue:
                    current = queue.popleft()
                    group.add(current)
                    # current 요소의 모든 노드 가져오기
                    current_nodes = next(nids for eid2, nids in elements if eid2 == current)
                    # 이 노드를 공유하는 요소 탐색
                    for nid in current_nodes:
                        for neighbor_eid in node_to_eids[nid]:
                            if neighbor_eid not in visited:
                                visited.add(neighbor_eid)
                                queue.append(neighbor_eid)
                groups.append(list(group))
#       output = [[obj1, obj2], [obj3,obj4]]
        return groups

    def get_quad_internal_angle(self, elem_obj):
        if VistaDb.GetClassName(elem_obj) == 'FeQuadClass':
            num, angle_list = VistaDb.QuadComputeInternalAngles(elem_obj)
            return angle_list
        else:
            print(f"[WARN] get_quad_internal_angle: element type is not FeQuadClass "
                  f"(actual: {VistaDb.GetClassName(elem_obj)})")
            

    def get_tria_internal_angle(self, elem_obj):

        if VistaDb.GetClassName(elem_obj) == 'FeTriaClass':
            num, angle_list = VistaDb.TriaComputeInternalAngles(elem_obj)
            return angle_list
        else:
            print(f"[WARN] get_tria_internal_angle: element type is not FeTriaClass "
                  f"(actual: {VistaDb.GetClassName(elem_obj)})")

    def get_displayed_entities_list(self):
        var1 = VCmd.Activate(1 ,r"VHostManagerPlugin.VhmInterface" ,r"VhmCommand"  )
        VCmd.SetStringValue( var1, r"TargetName", r"Element" )
        VCmd.ExecuteCommand( var1, r"SelectAllVisible" )
        _,elem_obj_list = VCmd.GetObjectValues(var1,"SelectedEntities")
        VCmd.ExecuteCommand( var1, r"DeselectAll" )

        if elem_obj_list:
            return elem_obj_list
        else:
            return False

    def get_displayed_nodes_list(self):
        elem_obj_list = self.get_displayed_entities_list()
        _,node_obj_list = VistaDb.ModelGetObjectList(self.model, "FeNodeClass")
        node_db = { VistaDb.GetId(x):x for x in node_obj_list }

        if elem_obj_list:

            nid_set = set()

            for elem_obj in elem_obj_list:
                _, _, n, nids = VistaDb.ElementGetData(elem_obj)
                nid_set.update(nids)
            nid_list = list(nid_set)
            output_list = [ node_db[nid] for nid in nid_list ]
            return output_list
        else:
            return False


    def get_displayed_entities_bounding_box(self):
        elem_obj_list = self.get_displayed_entities_list()
        _,node_obj_list = VistaDb.ModelGetObjectList(self.model, "FeNodeClass")
        point_db = { VistaDb.GetId(x):VistaDb.GetVgPoint3Value(x, "Point") for x in node_obj_list }

        if elem_obj_list:

            nid_set = set()

            for elem_obj in elem_obj_list:
                _, _, n, nids = VistaDb.ElementGetData(elem_obj)
                nid_set.update(nids)
            nid_list = list(nid_set)
            point_list = [ point_db[nid] for nid in nid_list ]
            coordinate_array = np.array([[pnt.x, pnt.y, pnt.z] for pnt in point_list], dtype= np.float64)

            xmin, ymin, zmin = coordinate_array.min(axis=0)
            xmax, ymax, zmax = coordinate_array.max(axis=0)

            bbox_points = np.array([ [x, y, z] for x in (xmin, xmax) for y in (ymin, ymax) for z in (zmin, zmax) ])
            return [xmin, xmax, ymin, ymax, zmin, zmax]
        else:
            return False
