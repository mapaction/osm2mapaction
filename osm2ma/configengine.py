#-------------------------------------------------------------------------------
# Name:        configengine
# Purpose:
#
# Author:      asmith
#
# Created:     20/08/2014
# Copyright:   (c) asmith 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sqlite3
import logging

logging.basicConfig(level=logging.INFO)


class RawConfigIterator:
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
            logging.debug(utf8_rtn_list)
            return utf8_rtn_list



class ConfigXWalk:
    def _init_db_tables(self):
        cur = self.cursor
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



    def _populate_config_table(self, area2d):
        cur = self.cursor

        mysheet, rowxlo, rowxhi, colxlo, colxhi = area2d

    ##    for r in RowsFromSheet(area2d):
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
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', RawConfigIterator(area2d))


    ##    for r in cur.execute("select osm_key_name,osm_key_value from config where osm_key_name='power'"):
    ##        print r

    def _populate_scratch_table(self):
        cur = self.cursor

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

    def _populate_shpfile_table(self, geo_extd, scale):
        cur = self.cursor

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


    def _init_db_funcs(self):
        con = self.db
        # TODO This funciton is not specific to the internal DB, and encapsulates
        # knowledge of the MA DNC. Therefore it should be moved from this class
        # and passed as a value.
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

    # TODO this function really shouldn't be necessary as it is exposing the workings of the class
    # def getCursor(self):
    #    return self.cursor

    def getXWalk(self):
        cur = self.cursor
        return cur.execute('''select
                    shpfile_name,
                    cat_value,
                    geom_type,
                    attrib_str,
                    condition_str
            from shpf_list''').fetchall()

    def __init__(self, area2d, geoextent_clause, scale_clause):
        # excel_file = r"D:\work\custom-software-group\code\mapaction-toolbox\OSMChangeToolbox\osm2ma\testfiles\OSM_to_MA_short.xls"
        self.db = sqlite3.connect(':memory:')
        self.cursor = self.db.cursor()
        self._init_db_funcs()
        self._init_db_tables()
        self.db.commit()
        self._populate_config_table(area2d)
        self._populate_scratch_table()
        self._populate_shpfile_table(geoextent_clause, scale_clause)
        self.db.commit()

def xWalkFromRawConfig(raw_config, geoextent_clause, scale_clause):
    return ConfigXWalk(raw_config, geoextent_clause, scale_clause).getXWalk()
