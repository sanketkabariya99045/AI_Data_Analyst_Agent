from backend.database.schema import schema_manager


def get_sales_sql():

    schema = schema_manager.get_database_schema()

    table_name = list(schema.keys())[0]

    return {

        "total_sales": f'''
            SELECT
                SUM("Sales") AS value
            FROM "{table_name}";
        ''',

        "total_profit": f'''
            SELECT
                SUM("Profit") AS value
            FROM "{table_name}";
        ''',

        "total_orders": f'''
            SELECT
                COUNT(*) AS value
            FROM "{table_name}";
        ''',

        "total_customers": f'''
            SELECT
                COUNT(DISTINCT "Customer ID") AS value
            FROM "{table_name}";
        ''',

        "sales_region": f'''
            SELECT
                "Region",
                SUM("Sales") AS TotalSales
            FROM "{table_name}"
            GROUP BY "Region"
            ORDER BY TotalSales DESC;
        ''',

        "category_sales": f'''
            SELECT
                "Category",
                SUM("Sales") AS TotalSales
            FROM "{table_name}"
            GROUP BY "Category"
            ORDER BY TotalSales DESC;
        ''',

        "monthly_sales": f'''
            SELECT
                "Order Date",
                SUM("Sales") AS TotalSales
            FROM "{table_name}"
            GROUP BY "Order Date"
            ORDER BY "Order Date";
        '''
    }