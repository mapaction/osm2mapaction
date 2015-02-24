
import sys
# import test_configengine
# import test_ogrwrapper


def main():
    print "print sys.path:"
    print sys.path
    # test_ogrwrapper.unittest.main()
    # test_configengine.unittest.main()
    print ""
    print "importing gdal"
    from osgeo import gdal
    print "print gdal.__file__"
    print gdal.__file__

if __name__ == '__main__':
    main()
