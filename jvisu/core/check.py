import VistaDb

# Junhyung's define function 
def checkNodeClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeNodeClass':
        return True
    else:
        return False

def checkElementClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.IsClassSuperClass(cname, "FeElementClass"):
        return True
#    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeTriaClass':
#        return True
#    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeQuadClass':
#        return True
#    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeHexaClass':
#        return True
#    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeTetraClass':
#        return True
#    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FePentaClass':
#        return True
    else:
        return False

def checkPartClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FePartClass':
        return True
    else:
        return False

def checkFuncClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeLoadCurveClass':
        return True
    else:
        return False


def checkPyFuncClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FePythonFunctClass':
        return True
    else:
        return False

def checkMatClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.IsClassSuperClass(cname, "FeMatClass" ):
        return True
    else:
        return False

def checkCurveClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'GmCurveClass':
        return True
    elif str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'VskPolylineClass':
        return True
    else:
        return False

def checkSurfaceClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'MeshFaceClass':
        return True
    else:
        return False

def checkKinematicsClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeKinematicsClass':
        return True
    else:
        return False

def checkGroupClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeSetClass':
        return True
    else:
        return False

def checkFrameClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeCoordSysClass':
        return True
    else:
        return False

def checkContactClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeContactClass':
        return True
    else:
        return False


def checkTiedClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeCrConTiebkNodeClass':
        return True
    else:
        return False

def checkPlinkClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FePlinkClass':
        return True
    else:
        return False

def checkJointClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeJointClass':
        return True
    else:
        return False

def checkRbodyClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeNodalRgdBdyClass':
        return True
    else:
        return False

def checkMtocoClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeMtocoClass':
        return True
    else:
        return False

def checkTHNodeClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'THNodeClass':
        return True
    else:
        return False

def checkTHLocClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'checkFeAccelerometerClass':
        return True
    else:
        return False

def checkTHElementClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'THElementClass':
        return True
    else:
        return False

def checkFeCrCrossSectionClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeCrCrossSectionClass':
        return True
    else:
        return False

def checkFeAccelerometerClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>" and VistaDb.GetClassName(cname) == 'FeAccelerometerClass':
        return True
    else:
        return False


def checkVistaObjectClass(cname):

    if str(type(cname)) == "<class 'VistaObject'>":
        return True
    else:
        return False

def checkPointClass(cname):

    if str(type(cname)) == "<class 'VgPoint3'>":
        return True
    else:
        return False


def checkNatNum(n):
    if str(n).isdigit() and float(n) == int(n) and int(n) > 0:
        return True
    else:
        return False

def checkInteger(cname):
    if str(type(cname))  == "<class 'int'>" :
        return True
    else:
        return False

def checkString(cname):
    if str(type(cname))  == "<class 'str'>" :
        return True
    else:
        return False

def checkFloat(cname):
    if str(type(cname))  == "<class 'float'>" :
        return True
    else:
        return False

def checkNumpy(cname):
    if str(type(cname))  == "<class 'numpy.ndarray'>" :
        return True
    else:
        return False
