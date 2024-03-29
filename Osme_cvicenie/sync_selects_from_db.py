import psycopg2
import time


def connect_to_db():
    con = psycopg2.connect(
        database="",
        user="",
        password="",
        host="",
        port="5432")
    print("Database opened successfully")
    print("-------------------------------")
    return con


def execute_sql_instruction(cursor, sql_instr, count):
    cursor.execute(sql_instr)
    data = cursor.fetchall()
    for row in data:
        count += 1
        print(row)
    return count


def main():
    rows_count = 0
    connection = connect_to_db()
    cursor = connection.cursor()
    sql_queries = [
        "SELECT * FROM BOOKS WHERE count < 3",
        "SELECT * FROM BOOKS WHERE count > 3",
        "SELECT * FROM BOOKS WHERE count > 3 AND count < 15 "
        "ORDER BY count",
        "SELECT * FROM BOOKS WHERE count > 10 OR count <= 2 "
        "ORDER BY count",
        "SELECT * FROM BOOKS WHERE count < 3",
        "SELECT * FROM BOOKS WHERE count > 3",
        "SELECT * FROM BOOKS WHERE count > 3 AND count < 15 "
        "ORDER BY count",
        "SELECT * FROM BOOKS WHERE count > 10 OR count <= 2 "
        "ORDER BY count"]

    for query in sql_queries:
        rows_count = execute_sql_instruction(cursor, query, rows_count)

    print("Rows count: ", rows_count)
    connection.close()


if __name__ == '__main__':
    start_time = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time for sync_program: {elapsed:.2f}")
