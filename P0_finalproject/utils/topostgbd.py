def bd_conn():
    """Connect a postgress SQL engine

    Returns:
        conn: Connection to BD
    """
    import psycopg2

    # CONN setup
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="bd",
        user="ljpcastroc",
        password="password"
    )
    
    return conn

def bd_cursor(conn):
    # Create a cursor for launch SQL statement
    bd_cursor = conn.cursor()
    return bd_cursor

def bd_alltables(cur):
    """_summary_

    Args:
        cur (_type_): _description_
    """
    # This query returns all tables in "public" eschema
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")

def bd_printall(cur):
    """_summary_

    Args:
        cur (_type_): _description_
    """
    # And print all tables in database (db in conn)
    for table in cur.fetchall():
        print(table[0])

def bd_engine():
    """_summary_
    """
    from sqlalchemy import create_engine
    # We use engine
    engine = create_engine('postgresql+psycopg2://ljpcastroc:password@localhost:5432/bd')
    return engine