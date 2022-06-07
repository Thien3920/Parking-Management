from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

# package = Extension('bbox', ['bbox.pyx'], include_dirs=[numpy.get_include()])

package = [
    Extension("bbox", ["bbox.pyx"],
              include_dirs=[numpy.get_include()]),
    Extension("anchors", ["anchors.pyx"],
              include_dirs=[numpy.get_include()]),
    Extension("cpu_nms", ["cpu_nms.pyx"],
              include_dirs=[numpy.get_include()]),
]
setup(ext_modules=cythonize(package))