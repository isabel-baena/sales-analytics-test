from pathlib import Path
from sqlite3 import Connection
import pandas as pd

def compute_revenue_per_customer_month(conn: Connection) -> pd.DataFrame:
    query = """
    SELECT o.customer_id, c.name, c.country, strftime('%Y-%m', o.order_date) AS year_month, SUM(o.total_amount) as revenue
    FROM orders AS o
    LEFT JOIN customers as c ON o.customer_id = c.customer_id
    WHERE o.total_amount >= 0
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
    ORDER BY year_month ASC, revenue DESC
    """

    return pd.read_sql_query(query, conn)

def compute_top_products(conn: Connection, limit: int = 5) -> pd.DataFrame:
    
    query = """
    SELECT product_name, SUM(quantity * unit_price) as total_revenue
    FROM order_items
    GROUP BY product_name
    ORDER BY total_revenue DESC
    LIMIT ?
    """
    return pd.read_sql_query(query, conn, params=(limit,))

def generate_reports(conn: Connection, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    df_rev = compute_revenue_per_customer_month(conn)
    df_rev.to_csv(output_dir / "revenue_per_customer_per_month.csv", index=False)

    df_top = compute_top_products(conn, limit=5)
    df_top.to_csv(output_dir / "top_products.csv", index=False)
