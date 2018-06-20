#common mysqldb python utilities
import MySQLdb
import MySQLdb.cursors

class MySQLTools:

    def __init__(self, host, user, password, schema):
        self.host = host
        self.user = user
        self.password = password
        self.schema = schema

    def create_connection(self, cursor=None):
        if cursor is None:
            cur_class = MySQLdb.cursors.cursor
        elif cursor == "server_side":
            cur_class = MySQLdb.cursors.SSCursor
        elif cursor == "dict":
            cur_class = MySQLdb.cursors.DictCursor
        conn = MySQLdb.connect(host=self.host, 
                               user=self.user, 
                               passwd=self.password,
                               db=self.schema,
                               cursorclass=cur_class)
        conn.autocommit(True)
        return conn

    def execute_stored_proc(self, proc_name, proc_vars=None, connection=None):
        if connection is None:
            conn = self.create_connection()
        else:
            conn = connection
        cur = conn.cursor()
        proc_query = "call {proc}{vars}".format(proc=proc_name,vars=proc_vars)
        print proc_query
        cur.execute(proc_query)
        if proc_vars:
            cur.execute("SELECT {0}".format(proc_vars))
            cur.fetchall()
            cur.close()
        if connection is None:
            conn.close()

    def execute_query(self, query, get_results=None, cur_class=None, connection=None):
        if connection is None:
            conn = self.create_connection(cur_class)
        else:
            conn = connection
        cur.conn.cursor()
        cur.execute(query)
        if get_results == 1:
            result = cur.fetchone()[0]
        elif get_results == "row":
            result = cur.fetchall()[0]
        elif get_results == "column_result":
            result = [fetch[0] for fetch in cur.fetchall()]
        elif get_results == "all":
            result = cur.fetchall()
        else:
            result = None

        if connection is None:
            cur.close()
            conn.close()

        return result

