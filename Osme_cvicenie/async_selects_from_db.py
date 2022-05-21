import asyncio
import time
import asyncpg


async def connect_to_db():
    conn = await asyncpg.connect(
        database="",
        user="",
        password="",
        host="",
        port="5432")
    print("Database opened successfully")
    print("-------------------------------")
    return conn


async def select_sql_instruction(conn, sql, count):
    data = await conn.fetch(sql)
    for row in data:
        count = count + 1
        print(row)
    return count


async def run():
    rows_count = 0
    connection = await connect_to_db()
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
        rows_count = \
            await select_sql_instruction(connection, query, rows_count)

    print("Rows count: ", rows_count)
    await connection.close()


if __name__ == '__main__':
    start_time = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    elapsed = time.perf_counter() - start_time
    print(f"\nTotal elapsed time for async_program: {elapsed:.2f}")
