[![Coverage Status](https://coveralls.io/repos/mapaction/osm2mapaction/badge.svg)](https://coveralls.io/r/mapaction/osm2mapaction)

Running Tests
=============
Run all unittests (from the osm2ma directory:
```
python -m unittest discover
```
Or from a different directory:
```
python -m unittest discover -s <path_to_osm2ma>
```
We are using the unittest framework for all our testing. Strictly some of our
tests are not unittests but module-level integration tests. This is a pragmatic,
if imperfect, approach. Our aim is to get to 100% coverage.



Testing coverage
----------------
Run unittest code through coverage to update it's record
```
coverage erase
coverage run -a -m unittest discover
coverage run -a osm2mapaction.py -c testfiles\fixtures.xls -g gb, -su -o 
testfiles\output_shp testfiles\oxfordshire-latest.osm.pbf
```

Print (on cmdline) a report of coverage per module
```
coverage report --omit=test*,fixtures*  *.py
```

Update copies of source files, annotated with which lines the tests reach or not:
```
coverage annotate --omit=test*,fixtures* -d coverageoutput *.py
```