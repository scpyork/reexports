def get_trade(year,item):

    import psycopg2
    import pandas as pd
    import pandas.io.sql as sqlio

    try:
        conn = psycopg2.connect(user = "admin",
                                      password = "admin",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "faostat")

        #localhost server - change this when using something else.

        cursor = conn.cursor()
        # Print PostgreSQL Connection properties
        print ( conn.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


    def q(sql):
        import pandas.io.sql as sqlio
        return sqlio.read_sql_query(sql, conn)

##########


    cidr = q(
    '''SELECT DISTINCT "Reporter Countries","Reporter Country Code"
    FROM %s
    WHERE "Reporter Country Code" < 270 AND "Year" = %d
     ;'''%('trade_matrix',int(year)))

    cidp = q(
        '''SELECT DISTINCT "Partner Countries","Partner Country Code"
        FROM %s
        WHERE "Partner Country Code" < 270 AND "Year" = %d
         ;'''%('trade_matrix',int(year)))


    cidp.columns = cidr.columns = ['name','id']

    cid = cidr.merge(cidp,how='outer')
    #cid = cid.merge(pid,how='outer')


###########


    P = q(
    '''SELECT "Area","Area Code","Value"
    FROM %s
    WHERE "Year" = %d AND "Item" = '%s'
    AND "Unit"='tonnes' AND "Value" > 0 AND "Area Code" < 270 AND "Element"='Production'
     ;'''%('production',int(year),item))


###########


    trade =  q(
    '''SELECT "Reporter Countries","Partner Countries","Reporter Country Code","Partner Country Code","Element","Value"
    FROM %s
    WHERE "Year" = %d AND "Item" = '%s'
    AND "Unit"='tonnes' AND "Value" > 0 AND "Reporter Country Code" < 270 AND "Partner Country Code" < 270
     ;'''%('trade_matrix',int(year),item))

    imports = trade[trade.Element == 'Import Quantity']
    exports = trade[trade.Element == 'Export Quantity']

    imports.columns = '~'.join(imports.columns).replace('Reporter Country Code','target').replace('Partner Country Code','source').split('~')

    exports.columns = '~'.join(exports.columns).replace('Reporter Country Code','source').replace('Partner Country Code','target').split('~')

    D = pd.concat([imports,exports],axis = 0, sort = True)



    print ('Data Loaded \n\n\n')
    conn = None
    return D,P, cid.set_index('id').to_dict()['name']






def get(sql,db):

    import psycopg2
    import pandas as pd
    import pandas.io.sql as sqlio

    try:
        conn = psycopg2.connect(user = "admin",
                                      password = "admin",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = db)

        #localhost server - change this when using something else.

        cursor = conn.cursor()
        # Print PostgreSQL Connection properties
        print ( conn.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


    def q(sql):
        import pandas.io.sql as sqlio
        return sqlio.read_sql_query(sql, conn)

##########


    return q(sql)



if __name__ == '__main__':
    D,P,cid = get_trade(2003,'Soybeans')
    print cid, D, P
