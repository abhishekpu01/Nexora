from mcp.server.fastmcp import FastMCP
from constants.constants import COLOR_MAPPING, ANALYSED_PRODUCTS_QUERY
from .db import SessionLocal
from sqlalchemy import text

mcp = FastMCP("nexous-products")

@mcp.tool()
def fetch_analysed_products(outfit_types:list, color_combinations:list):

    for combination in color_combinations:
        for category,color in combination.items():
            for mapping,variants in COLOR_MAPPING.items():
                if color in variants:
                    combination[category] = mapping
    values= []
    db = SessionLocal()

    for color in color_combinations:
        for outfit in outfit_types:
            values.append(
                    f"('{outfit['top']}', '{color['top']}', "
                    f"'{outfit['bottom']}', '{color['bottom']}')"
                )
    query = ANALYSED_PRODUCTS_QUERY.format(
        values=",\n".join(values)
    )
    # Query DB here
    try:
        result = db.execute(text(query))
        rows = result.fetchall()

        return [dict(row._mapping) for row in rows]

    finally:
        db.close()