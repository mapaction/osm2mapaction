import os
import sys
import subprocess
import xlrd
import collections
import sqlite3
import re
import datetime

class RowsFromSheet:
    def __init__(self, area2d):
        self.mysheet, self.rowxlo, self.rowxhi, self.colxlo, self.colxhi = area2d
        self.row_current = self.rowxlo

    def __iter__(self):
        return self


    def next(self): # Python 3: def __next__(self)
        def parse_cell_values(val):
            if ((type(val) == int) and (val == 42)):
                return (None)
            elif (type(val) == unicode):
                return val.strip()
            else:
                return val

        if self.row_current >= self.rowxhi:
            raise StopIteration
        else:
            self.row_current += 1
            u_rtn_list = self.mysheet.row_values(self.row_current - 1, self.colxlo, self.colxhi)
            utf8_rtn_list = map(parse_cell_values, u_rtn_list)
            # print utf8_rtn_list
            return utf8_rtn_list


def load_excel(excelfilename, excelnamedrange, path):
    # define some constants
    _excelfilename = excelfilename
    _excelnamedrange = excelnamedrange

    # calculate some constants
    if path is None:
        _scriptdir = os.path.dirname(os.path.realpath(sys.argv[0]))
    else:
        _scriptdir = path

    _excelpath = os.path.join(_scriptdir, _excelfilename)

    # print "g_scriptdir = " + g_scriptdir
    # print "_excelpath = " + _excelpath

    workbook = xlrd.open_workbook(_excelpath)
    namedrange = workbook.name_map.get(_excelnamedrange)[0]
    return namedrange.area2d(clipped=True)

def get_column_indicies(area2d, col_names):
    def_col_names = ("Key", "Value", "Comment", "Data Category", "description",
    "Cat_value", "Date Theme", "description", "Theme_value", "OSM_Element",
    "Data type", "pt", "ln", "py")

    mysheet, rowxlo, rowxhi, colxlo, colxhi = area2d
    col_headers = mysheet.row_values(rowxlo, colxlo, colxhi)
    # print col_headers


def init_db_tables(cur):
    cur.executescript('''
        create table config (
            osm_key_name text,
            osm_key_value text,
            element_icon text,
            comment text,
            data_category text,
            cat_value text,
            data_theme text,
            theme_value text,
            osm_element text,
            geom_str text,
            pt text,
            ln text,
            py text,
            rel text
        );

        create table scratch (
            osm_key_name text,
            osm_key_value text,
            cat_value text,
            theme_value text,
            osm_element,
            geom_type text
        );

        create table shpf_list (
            shpfile_name text,
            cat_value text,
            geom_type text,
            attrib_str text,
            condition_str text,
            cmdline_str text
        );

        ''')


def populate_config_table(cur, area2d):

    mysheet, rowxlo, rowxhi, colxlo, colxhi = area2d

##    for r in RowsFromSheet(area2d):
##        print "row = " + str(r)

    cur.executemany('''
        INSERT INTO config
            (osm_key_name,
            osm_key_value,
            element_icon,
            comment,
            data_category,
            cat_value,
            data_Theme,
            theme_value,
            osm_element,
            geom_str,
            pt,
            ln,
            py,
            rel)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', RowsFromSheet(area2d))


##    for r in cur.execute("select osm_key_name,osm_key_value from config where osm_key_name='power'"):
##        print r

def populate_scratch_table(cur):
    for geom in ("pt", "ln", "py", "rel"):
        u_sql= '''
            INSERT INTO scratch (
                osm_key_name,
                osm_key_value,
                cat_value,
                theme_value,
                osm_element,
                geom_type
            )
            select
                osm_key_name,
                osm_key_value,
                cat_value,
                theme_value,
                osm_element,
                '{s_geom}'
            from config where
                instr(config.geom_str,'{s_geom}')
            '''.format(s_geom=geom)

        cur.execute(u_sql)

##    for r in cur.execute("select * from scratch order by osm_key_name, osm_key_value, cat_value, theme_value"):
##        print r

def populate_shpfile_table(cur, geo_extd, scale):
    u_sql = u'''
        INSERT INTO shpf_list (
            shpfile_name,
            cat_value,
            geom_type,
            attrib_str,
            condition_str,
            cmdline_str
        )
        select
            shpf_name('{s_geo_extd}', scratch.cat_value, scratch.theme_value, scratch.geom_type, '{s_scale}'),
            scratch.cat_value,
            scratch.geom_type,
            attriblist(scratch.osm_key_name),
            condition_clause(scratch.osm_key_name, scratch.osm_key_value),
            'something'
        from scratch
        group by
            shpf_name('{s_geo_extd}', scratch.cat_value, scratch.theme_value, scratch.geom_type, '{s_scale}'),
            scratch.cat_value,
            scratch.geom_type,
            'something'
        '''.format(s_geo_extd=geo_extd, s_scale=scale)

    cur.execute(u_sql)

#            shpf_name(:s_geo_extd, scratch.cat_value, scratch.theme_value, scratch.geom_type, :s_scale),
#            shpf_name('wrl', scratch.cat_value, scratch.theme_value, scratch.geom_type, 'su')
        #, {"s_geo_extd"=geo_extd, "s_scale"=scale})

##    for r in cur.execute("select * from shpf_list"):
##        print r

##    print cur.execute("select count(*) from shpf_list").fetchone()


def init_db_funcs(con):
    def create_shpf_name(geo_extd, data_cat, data_thm, geom_type, scale):
        # geoextent_datacategory_datatheme_datatype[_scale]_source[_permission][_FreeText]
        output_filename = \
            u'{s_geo_extd}_{s_cat}_{s_thm}_{s_geom_type}_{s_scale}_osm_pp.shp'.format(
            s_geo_extd=geo_extd,
            s_cat=data_cat,
            s_thm=data_thm,
            s_geom_type=geom_type,
            s_scale=scale
            )
        return output_filename

    class AttribList:
        def __init__(self):
            self.set_attribs = set()

        def step(self, value):
            self.set_attribs.add(value)

        def finalize(self):
            # def concat_list(a,b): return a + ", " + b
            return reduce(lambda a,b: a + ", " + b, sorted(self.set_attribs))

    class SelectClause:
        def __init__(self):
            self.l_dict = dict()
            self.exclude_keys = set()

        def step(self, osm_key, osm_value):
##            print "stepping ", osm_key, osm_value
            if ((type(osm_value) == unicode) and (osm_value.lower() in {u'*', u'user defined'})):
                self.exclude_keys.add(osm_key)
##                print "excluding " + osm_key
            else:
                for val in osm_value.split(u'/'):
                    l_key = u"'{s_key}'='{s_val}'".format(s_key=osm_key, s_val=val.strip())
                    self.l_dict[l_key] = osm_key
##                print "including " + l_key

        def finalize(self):
##            print "starting finalize"
            cleaned_pairs = set()
##            print "setup cleaned_pairs"
            for l_key, l_val in self.l_dict.iteritems():
##                print "started for loop"
                if l_val in self.exclude_keys:
##                    print "entered if statement"
                    # cleaned_pairs.add(u"('{s_val}' is not null and '{s_val}' != '')".format(s_val=l_val))
                    cleaned_pairs.add(u"'{s_val}' is not null".format(s_val=l_val))
##                    print "finalize " + l_key, l_val
                else:
##                    print "entered if statement"
                    cleaned_pairs.add(l_key)
##                    print "finalize " + l_key, l_val

            if len(cleaned_pairs) > 0:
                return reduce(lambda a,b: a + u" or " + b, sorted(cleaned_pairs))
            else:
                return ''

    con.create_function("shpf_name", 5, create_shpf_name)
    con.create_aggregate("attriblist", 1, AttribList)
    con.create_aggregate("condition_clause", 2, SelectClause)


def compose_condition_clause(osm_key_list, osm_val_list):
    def single_clause(key,val):
        return "'{s_key}'='{s_val}'".format(s_key=key, s_val=val)

    clause_list = map(single_clause, osm_key_list, osm_val_list)
    # print clause_list, my_or_list
    return str_reduced_from_list(clause_list, " OR ")

##def str_reduced_from_list(the_list, seperator=", "):
##    def concat_list(a,b): return a + seperator + b
##    return reduce(concat_list, sorted(the_list))


def compose_ogr2ogr_cmd(data_cat, geom_type, osm_atrbs, condition, pbf_filename,
output_filename, output_path):

    if geom_type == "pt":
        source_geom = "POINTS"
        source_table = "POINTS"
    elif geom_type == "py":
        source_geom = "POLYGON"
        source_table = "multipolygons"
    elif geom_type == "ln":
        source_geom = "LINES"
        source_table = "LINES"
    elif geom_type == "rel":
        source_geom = "UNKNOWN"
        source_table = "other_relations"

    output_filepath = os.path.join(output_path, output_filename)

    # Example cmd str
    # ogr2ogr -overwrite -sql "SELECT osm_id, osm_way_id, name, building FROM
    # 'multipolygons' where 'building'='barn'" -f "ESRI Shapefile"
    # oxford_barns.shp oxfordshire-latest.osm.pbf -lco "SHP=POLYGON"
    #
    cmd_str = ur'''C:\OSGeo4W64\OSGeo4W.bat ogr2ogr -overwrite -sql "SELECT {s_atrbs} from '{s_source_table}' where {s_condition}" -f "ESRI Shapefile" "{s_output_filepath}" "{s_pbf_filename}" -lco "SHP={s_source_geom}"'''.format(
    s_atrbs=osm_atrbs, s_source_table=source_table,
    s_condition=condition, s_output_filepath=output_filepath,
    s_pbf_filename=pbf_filename, s_source_geom=source_geom)

    return cmd_str

def compose_ogrinfo_cmd(data_cat, geom_type, osm_atrbs, condition, pbf_filename):

    if geom_type == "pt":
        source_geom = "POINTS"
        source_table = "POINTS"
    elif geom_type == "py":
        source_geom = "POLYGON"
        source_table = "multipolygons"
    elif geom_type == "ln":
        source_geom = "LINES"
        source_table = "LINES"
    elif geom_type == "rel":
        source_geom = "UNKNOWN"
        source_table = "other_relations"

    # Example cmd str
    # ogr2ogr -overwrite -sql "SELECT osm_id, osm_way_id, name, building FROM
    # 'multipolygons' where 'building'='barn'" -f "ESRI Shapefile"
    # oxford_barns.shp oxfordshire-latest.osm.pbf -lco "SHP=POLYGON"
    #
    cmd_str = ur'''C:\OSGeo4W64\OSGeo4W.bat ogrinfo -ro -so -fields=no -geom=no "{s_pbf_filename}" -sql "SELECT {s_atrbs} from '{s_source_table}' where {s_condition}" '''.format(
    s_atrbs=osm_atrbs, s_source_table=source_table,
    s_condition=condition, s_pbf_filename=pbf_filename, s_source_geom=source_geom)

    return cmd_str


def check_feature_count(data_cat, geom_type, attribs, where_clause, pbf_file):
    cmd_str = compose_ogrinfo_cmd(data_cat, geom_type, attribs, where_clause, pbf_file)
    print cmd_str
    result_str = None
    try:
        result_str = subprocess.check_output(cmd_str.decode('utf-8'))
    except (subprocess.CalledProcessError, OSError):
        print "feature count command failed"
    else:
        # print result_str
        # print "feature count command completed"
        re_match = re.search(ur'\sFeature Count: (?P<featurecount>\d+)\s', result_str, re.IGNORECASE)
        # print re_match
        if re_match is not None:
            print "feature count = " + re_match.group('featurecount')
            return re_match.group('featurecount') > 0

def create_sub_dir(output_dir, data_cat):
    if os.path.isdir(output_dir):
        cat_dir_path = os.path.join(output_dir,data_cat)
        if not os.path.isdir(cat_dir_path):
            os.mkdir(cat_dir_path)
        return cat_dir_path

def do_ogr2ogr_process(cur, pbf_file, output_dir):
    for shp in cur.execute('''select
                    shpfile_name,
                    cat_value,
                    geom_type,
                    attrib_str,
                    condition_str
            from shpf_list'''):
        shpf_name, data_cat, geom_type, attribs, where_clause = shp
        cat_dir_path = create_sub_dir(output_dir, data_cat)

        cmd_str = compose_ogr2ogr_cmd(data_cat, geom_type, attribs, where_clause, pbf_file, shpf_name, cat_dir_path)
        # print cmd_str
        print
        unicode.decode

        if check_feature_count(data_cat, geom_type, attribs, where_clause, pbf_file):
            try:
                subprocess.check_call(cmd_str.decode('utf-8'))
            except (subprocess.CalledProcessError, OSError):
                print "command failed"
            else:
                print "command completed"

if __name__ == '__main__':
    pbf_file = sys.argv[1]
    excel_file = sys.argv[2]
    output_dir = sys.argv[3]
    geoextent =  sys.argv[4]

    if not (os.path.isfile(pbf_file) and os.path.isfile(excel_file)
        and (os.path.isdir(output_dir)) and isinstance(geoextent, basestring)):
        raise Exception("incorrect input parameters. PBF_FILE, EXCEL_FILE, OUTPUT_DIR, GEOEXTENT")

    print os.path.realpath(pbf_file), excel_file, output_dir

    # os.path.dirname(os.path.realpath(pbf_file))
    # print os.path.split(os.path.realpath(excel_file))[1]
    db = sqlite3.connect(':memory:')
    init_db_funcs(db)
    cur = db.cursor()
    init_db_tables(cur)
    db.commit()
    populate_config_table(cur, load_excel(os.path.split(os.path.realpath(excel_file))[1], "xwalk", os.path.dirname(os.path.realpath(excel_file))))
#    populate_config_table(cur, load_excel("OSM_to_MAv2.xls", "xwalk", r"D:\work\custom-software-group\osm-ma-shp"))
    populate_scratch_table(cur)
    populate_shpfile_table(cur, geoextent, u'su')
    db.commit()
#    do_ogr2ogr_process(cur, r"D:\work\custom-software-group\osm-ma-shp\oxfordshire-latest.osm.pbf", r"D:\work\custom-software-group\osm-ma-shp\outputs")
    start_time = datetime.datetime.now()
    do_ogr2ogr_process(cur, os.path.realpath(pbf_file), output_dir)
    end_time = datetime.datetime.now()
    print "Time to run export:"
    print "    start " + start_time
    print "    end " + end_time