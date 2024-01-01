from config import config
import api_handling
import data_processing
import BinanceAPIHandler
from DatabaseConnector import PostgreSQLConnection


if __name__ == '__main__':

    key_params = config("Key")
    all_isolated_margin_symbols = BinanceAPIHandler.symbols(**key_params)

    interval_sites = [
        [f'https://api.binance.com/api/v3/klines?symbol={margin_symbol["symbol"]}&interval=6h',
         margin_symbol["symbol"]] for margin_symbol in all_isolated_margin_symbols
    ]

    downloaded_sites = api_handling.download_all_sites(interval_sites)

    organized_data = {symbol: data_processing.framed_candles(data) for data, symbol in downloaded_sites}

    print(organized_data)

    db_params = config("postgresql")
    with PostgreSQLConnection(db_params) as conn:
        cursor = conn.cursor()

        for symbol, df in organized_data.items():
            table_name = f"table_{symbol}"
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (INDEX SERIAL PRIMARY KEY, "
            create_table_query += ", ".join([f"{col} VARCHAR" for col in df.columns]) + ")"

            cursor.execute(create_table_query)
            conn.commit()

            rows_to_insert = df.head(10).values.tolist()

            insert_query = (f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES "
                            f"({', '.join(['%s'] * len(df.columns))})")

            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()

        cursor.close()
