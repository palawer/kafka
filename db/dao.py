"""
Generic class that provides a simple layer to interact with db
"""
import uuid
import logging
from datetime import datetime
import psycopg2
from config import db_config



class DataObject():
    """
    Class that should be overriden by each entity that belongs to the project
    """
    __type__sql_type = {
        type('')       : "text",
        type(0)        : "integer",
        type(0.0)      : "float",
        type(datetime) : "TIMESTAMP",
    }
    
    @classmethod
    def db_connect(cls):
        """ connects to db """
        con = psycopg2.connect(**db_config)
        return con
    
    @classmethod
    def get_fields(cls):
        """ 
        for a given class, tipically a child of DataObject, 
        return its fields 
        """
        obj   = cls()
        fields = []
        for f in dir(obj) :
            if not f.startswith('__') and f!='_DataObject__type__sql_type':
                _type = cls.__type__sql_type.get(getattr(obj,f),None)
                if  _type: 
                    fields.append(
                        f
                    )
        
        return fields
    
    
    @classmethod
    def get_delete_statement(cls):
        """ 
        for a given class, tipically a child of DataObject, 
        return its drop table statement 
        """
        obj   = cls()
        name  = obj.__class__.__name__
        sql   = f"DROP TABLE {name}"
        
        return sql
    
    @classmethod
    def get_create_statement(cls):
        """ 
        for a given class, tipically a child of DataObject, 
        return its create table statement
         """
        obj   = cls()
        name  = obj.__class__.__name__
        sql   = [
            f"CREATE TABLE {name} ("
        ]
        fields = []
        for f in cls.get_fields():
            f_type = getattr(obj,f)
            _type  = cls.__type__sql_type.get(f_type,None)
            if  _type: 
                _f = cls.get_field_statetement(f,f_type)
                if _f:
                    fields.append(
                        _f
                    )
        
        sql.append(",".join(fields))
        sql.append(")")
        return " ".join(sql)
    
    @classmethod
    def get_field_statetement(cls,name,_type):
        """
        for a given class, tipically a child of DataObject, 
        and field name, returns the sql-compilant field statement 
        """
        
        sql_type = cls.__type__sql_type.get(_type,None)
        if not sql_type:
            logging.warning(f"{_type} is not supported!")
            return
        
        return f"{name} {sql_type}"
    
    def __init__(self,**kwargs):
        """
        returns an instance of a concrete class 
        with all populated fields got from kwargs
        """
        for k,v in kwargs.items():
            if hasattr(self,k):
                setattr(self,k,v)
    
    def save(self):
        """
        method that stores to db current object.
        It can perform insert or update operations
        depending on id field: 
        if None -> insert
        else    -> update
        """
        table_name  = self.__class__.__name__
        con         = self.db_connect()
        
        with con.cursor() as cursor:
            if self.id and type(self.id)==type(''):
                #update
                pass
            else:
                #insert
                self.id = str(uuid.uuid1())
                fields  = self.get_fields()
                values  = []
                _fields = []
                for f in fields:
                    _value = None
                    if hasattr(self,f):
                        _value = getattr(self,f)
                        #its a concrete value
                        if not isinstance(_value, type):
                            _fields.append(f)
                            values.append(_value)
                
                _values = ",".join(["%s"]*len(_fields))
                _fields = ",".join(_fields)
                sql = f"insert into {table_name} ({_fields}) values ({_values})"
                logging.info(sql)
                cursor.execute(sql,tuple(values))
                con.commit()
    
    @classmethod
    def get_by_filters(cls,**kwargs):
        """
        returns an a list of concrete instances
        by fields got from kwargs
        """
        fields  = cls.get_fields()
        _fields = ",".join(fields)
        
        filters = {
            k:v
            for k,v in kwargs.items()
            if k in fields
        }
        table_name  = cls.__name__
        con         = cls.db_connect()
        sql = [
            f"SELECT {_fields} FROM {table_name}"
        ]
        if filters:
            for idx,(k,v) in enumerate(filters.items()):
                if idx==0:
                    sql.append(
                        f"WHERE {k}='{v}'"
                    )
                else:
                    sql.append(
                        f"AND {k}='{v}'"
                    )
        objs = []
        with con.cursor() as cursor:
            cursor.execute(" ".join(sql))
            for values in cursor.fetchall():
                instance_data = dict(
                    zip(
                        fields,
                        values
                    )
                )
                objs.append(
                    cls(**instance_data)
                )
        return objs
    
    @classmethod
    def count_by_filters(cls,**kwargs):
        """
        returns the count of concrete instances
        by fields got from kwargs
        """
        fields  = cls.get_fields()
        filters = {
            k:v
            for k,v in kwargs.items()
            if k in fields
        }
        table_name  = cls.__name__
        con         = cls.db_connect()
        sql = [
            f"SELECT COUNT(*) FROM {table_name}"
        ]
        if filters:
            for idx,(k,v) in enumerate(filters.items()):
                if idx==0:
                    sql.append(
                        f"WHERE {k}='{v}'"
                    )
                else:
                    sql.append(
                        f"AND {k}='{v}'"
                    )
        count = 0
        with con.cursor() as cursor:
            logging.info(sql)
            cursor.execute(" ".join(sql))
            for values in cursor.fetchall():
                count = values[0]
        return count
        

