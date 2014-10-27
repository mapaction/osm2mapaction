#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      asmith
#
# Created:     17/09/2014
# Copyright:   (c) asmith 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import test_configengine
import test_ogrwrapper

def main():
    test_ogrwrapper.unittest.main()
    test_configengine.unittest.main()

if __name__ == '__main__':
    main()
