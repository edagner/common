#common mysqldb python utilities

import MySQLdb


def createSQLConnection(host = machine, user = username, 
                        passwd = password, schema = mysqlschema):
    """
    Create a MySQL connection
    """
    conn = MySQLdb.connection(host, user, passwd, schema)
    conn.autocommit(True)
    return conn

def executeStoredProc(procName = procedure, procvars = variables, 
                      host = machine, in_conn = None):
    """
    Function will execute given a stored routine with or without 
    variables on a specificed host. You may pass it a connection or it 
    will create its own.
    """
    try:
        if conn is None:
            conn = conn = MySQLdb.connection(host, user, passwd, schema)
            conn.autocommit(True)
        else:
            conn = in_conn
        cur = conn.cursor()
        procQuery = "call {0}{1}".format(procName,procvars)
        print procQuery
        cur.execute(procQuery)
        if procvars:
            cur = conn.cursor()
            cur.execlute("SELECT {0}".format(procvars))
            cur.fetchall()
            cur.close()
    except Exception as e:
        print e
        print "Could not execute {}({})".format(procName,procvars)