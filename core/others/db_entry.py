import psycopg
from psycopg import Connection
import datetime
from datetime import datetime as DT, timedelta, date
from bot_market_learn.core.settings import settings


async def database_entry():
    with psycopg.connect(f"host={settings.host} port=5432 dbname={settings.database} user={settings.user} "
                         f"password={settings.password} connect_timeout=10") as conn:

        if await get_count_row(conn) < 1:
            query = await get_query(3, str(DT.today().date()))
        else:
            query = await get_query(1, str(DT.today().date()))

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()


async def get_count_row(conn: Connection):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM booking")
        count = cur.fetchone()

    return count[0]


async def get_query(count_days, target_day):
    query = 'INSERT INTO booking (b_date, b_time, b_statuse, b_datetime) VALUES'

    target = DT.strptime(target_day, "%Y-%m-%d").date() + datetime.timedelta(days=1)
    # print(target)

    for x in range(count_days):
        date_target = target + datetime.timedelta(days=x)

        for i in range(0, 10*60, 60):
            time_delta = f'{(DT.combine(date.today(), datetime.time(8, 0)) + timedelta(minutes=i)).time().strftime("%H:%M")}'
            # print(time_delta)
            full_date_time = f"{date_target} {time_delta}"
            # print(full_date_time)
            line = f"\r\n('{date_target}', '{time_delta}', 'free', '{full_date_time}'),"

            query += line

    query = f"{query.rstrip(query[-1])};"
    return query


# print(get_query(3, str(DT.today().date())))
