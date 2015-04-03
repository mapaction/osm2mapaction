
import sys
import test_raw_conf_loader
# import test_configengine
# import test_ogrwrapper


def main():
    print "print sys.path:"
    print sys.path
    print ""
    print "importing gdal"
    from osgeo import gdal
    print "print gdal.__file__"
    print gdal.__file__

    test_raw_conf_loader.runtests()
    # test_configengine.unittest.main()
    # test_ogrwrapper.unittest.main()

if __name__ == '__main__':
    main()
