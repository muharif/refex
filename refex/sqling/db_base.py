from collections import OrderedDict
from storm.locals import Store, create_database


tables= ["ensembl", "uniprot", "go", "hpaclass", "hpasubloc", "kegg",
         "ensembl2go","uniprot2hpaclass", "uniprot2hpasubloc", "ensembl2kegg" ]


class DBBase(object):
    def __init__(self, sql_db_path):
        self.sql_db_path= sql_db_path 
        self.__init_database()


    def __init_database(self):    
        """
        creates the sqlite database instance and checks if the database exists in biodb.
        """
        database= create_database("sqlite:%s" % self.sql_db_path)
        print "Created storm database from %s." % self.sql_db_path
        self.store= Store(database)
     
    def drop_table(self, table_name):
        drop_table_string= "drop table %s" %table_name 
        self.store.execute(drop_table_string)


    def drop_tables(self):
        
        drop_table_string= "drop table " 
        
        for table in tables:
            drop_table_str= drop_table_string + table
            try:
                self.store.execute(drop_table_str)
            except:
                continue

        self.store.commit()



    def generate_table_strings(self):

        self.create_ensembl_string=  self.generate_create_table_string("ensembl", 
                                    OrderedDict([("id", "VARCHAR PRIMARY KEY"),
                                            ("entrez_id", "INTEGER"), ("uniprot_id", "VARCHAR"),
                                            ("symbol","VARCHAR"),("synonyms","VARCHAR")]),
                                            {"uniprot_id":("uniprot", "id")}) 
        
        self.create_uniprot_string= self.generate_create_table_string("uniprot",
                                    OrderedDict([("id", "VARCHAR PRIMARY KEY"),
                                              ("name", "VARCHAR") ]) )
        
        self.create_go_string= self.generate_create_table_string("go",
                                    OrderedDict([("id", "VARCHAR PRIMARY KEY"),
                                              ("name", "VARCHAR"), ("domain","INTEGER")]))
        

        self.create_kegg_string= self.generate_create_table_string("kegg",
                                    OrderedDict([("id", "VARCHAR PRIMARY KEY"),
                                     ("name", "VARCHAR")]))

        self.create_hpaclass_string= self.generate_create_table_string("hpaclass",
                                    OrderedDict([("id", "INTEGER PRIMARY KEY"),
                                                ("name", "VARCHAR")]))

        self.create_hpasubloc_string= self.generate_create_table_string("hpasubloc",
                                   OrderedDict([("id", "INTEGER PRIMARY KEY"),
                                                ("name", "VARCHAR")]))
        
        self.create_ensembl2go_string= self.generate_create_table_string("ensembl2go",
                                   OrderedDict([("id", "INTEGER PRIMARY KEY"),
                                                ("ensembl_id", "VARCHAR"), ("go_id", "VARCHAR")]),
                                                
                                                {"ensembl_id":("ensembl", "id"),
                                                 "go_id": ("go","id")})

        self.create_uniprot2hpaclass_string= self.generate_create_table_string("uniprot2hpaclass",
                                    OrderedDict([("id","INTEGER PRIMARY KEY"),
                                                 ("uniprot_id","VARCHAR"), ("hpaclass_id", "INTEGER") ]),
                                                 
                                                 {"uniprot_id":("uniprot","id"), "hpaclass_id":("hpaclass","id")})

        self.create_uniprot2hpasubloc_string= self.generate_create_table_string("uniprot2hpasubloc",
                                    OrderedDict([("id","INTEGER PRIMARY KEY"),
                                                 ("uniprot_id","VARCHAR"), ("hpasubloc_id", "INTEGER") ]),
                                                 {"uniprot_id":("uniprot","id"), "hpasubloc_id":("hpasubloc","id")})

        self.create_ensembl2kegg_string=  self.generate_create_table_string("ensembl2kegg",
                                    OrderedDict([("id","INTEGER PRIMARY KEY"),
                                                 ("ensembl_id","VARCHAR"), ("kegg_id", "VARCHAR") ]),
                                                 {"ensembl_id":("ensembl","id"), "kegg_id":("kegg","id")})



    def create_tables(self):

        create_table_strings= [ self.create_ensembl_string, create_uniprot_string,
                                     self.create_hpaclass_string, create_hpasubloc_string,
                                     self.create_go_string, create_ensembl2go_string,
                                     self.create_uniprot2hpaclass_string, self.create_uniprot2hpasubloc_string, 
                                     self.create_ensembl2kegg_string]

        for create_table_string in create_table_strings:
            self.store.execute(create_table_string)
            self.store.commit() 


    def generate_create_table_string(self, table_name, tables, foreign_keys= {}):
        """
            table_name: str
            tables: OrderedDict with fieldname as keys and type as value
            foreign keys: with source_id as keys, and  (target_table, target_id)
            as values
        """
        
        starter= "CREATE TABLE %s " %table_name

        table_str= ""
        for table, table_type in tables.iteritems():
            table_str+= "%s %s, " %(table, table_type)

            
        table_str = "(%s" %table_str.rstrip(', ')
        
        foreign_key_str=""
        for source_id, (target_name, target_id) in foreign_keys.iteritems():
            foreign_key_str+=", FOREIGN KEY (%s) REFERENCES %s (%s)" %(source_id, target_name, target_id)
        
        foreign_key_str+= ");"

        return "".join([starter, table_str, foreign_key_str]) 



