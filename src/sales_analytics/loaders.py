from pathlib import Path
from sqlite3 import Connection
import pandas as pd
import logging

from .config import DATA_DIR

def load_all_data(conn: Connection) -> None:
    load_customers(conn)
    load_orders(conn)
    load_order_items(conn)

def load_customers(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "customers.csv")

    expected_rows = len(df)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    final_rows = rows_after_load(conn, "customers")

    if expected_rows != final_rows:
        logging.warning("Row count mismatch for customers. Expected: %d, got: %d", expected_rows, final_rows)

def load_orders(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "orders.csv")
    df["total_amount"] = df["total_amount"].fillna(0.0)
    negative_total_amount = df[df["total_amount"] < 0]
    if len(negative_total_amount) > 0:
        logging.warning("Found %d order rows with a negative value for the total amount", len(negative_total_amount))
    missing_fk = df["customer_id"].isna().sum()
    if missing_fk > 0:
        logging.warning("Found %d order rows without customer id (fk)", missing_fk)
   
    expected_rows = len(df)
    df.to_sql("orders", conn, if_exists="replace", index=False)
    final_rows = rows_after_load(conn, "orders")

    if expected_rows != final_rows:
        logging.warning("Row count mismatch for orders. Expected: %d, got: %d", expected_rows, final_rows)


def load_order_items(conn: Connection) -> None:
    df = pd.read_csv(Path(DATA_DIR) / "order_items.csv")
    expected_rows = len(df)

    df.to_sql("order_items", conn, if_exists="replace", index=False)
    final_rows = rows_after_load(conn, "order_items")

    if expected_rows != final_rows:
        logging.warning("Row count mismatch for order_items. Expected: %d, got: %d", expected_rows, final_rows)


def rows_after_load(conn: Connection, table: str):
    query = f"""
    SELECT COUNT(*)
    FROM {table}
    """
    return pd.read_sql_query(query, conn).iloc[0, 0]

