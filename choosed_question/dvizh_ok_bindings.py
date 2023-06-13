import ctypes

dvizh_ok = ctypes.cdll.LoadLibrary("../dvizh_ok/dvizh_ok.so")
dvizh_ok.add_circle.argtypes = [ctypes.c_double] * 6
dvizh_ok.add_section.argtypes = [ctypes.c_double] * 4
dvizh_ok.set_borders.argtypes = [ctypes.c_double] * 4
dvizh_ok.set_collision_c_c.argtypes = [ctypes.c_int] * 3
dvizh_ok.set_collision_c_s.argtypes = [ctypes.c_int] * 3
dvizh_ok.step.argtypes = [ctypes.c_double]

dvizh_ok.add_section.restype = ctypes.c_int

class Circle(ctypes.Structure):
    _fields_ = [
        ('id', ctypes.c_uint),
        ('r', ctypes.c_double),
        ('m', ctypes.c_double),
        ('x', ctypes.c_double),
        ('y', ctypes.c_double),
        ('vx', ctypes.c_double),
        ('vy', ctypes.c_double),
    ]

class Section(ctypes.Structure):
    _fields_ = [
        ('id', ctypes.c_uint),
        ('x1', ctypes.c_double),
        ('y1', ctypes.c_double),
        ('x2', ctypes.c_double),
        ('y2', ctypes.c_double),
    ]

sections = ctypes.POINTER(ctypes.POINTER(Section)).in_dll(dvizh_ok, "sections")
circles = ctypes.POINTER(ctypes.POINTER(Circle)).in_dll(dvizh_ok, "circles")

def get_circle(n):
    return ctypes.POINTER(Circle)(circles[n].contents).contents

def get_section(n):
    return ctypes.POINTER(Section)(sections[n].contents).contents
