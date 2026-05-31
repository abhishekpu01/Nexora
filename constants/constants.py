COLOR_MAPPING = {
    "Black": [
        "Black", "Jet Black", "Charcoal Black"
    ],

    "White": [
        "White", "Off White", "Ivory", "Cream"
    ],

    "Grey": [
        "Grey", "Gray", "Charcoal Grey", "Ash Grey", "Slate Grey", "Charcoal Gray", "Slate Gray", "Dark Grey"
    ],

    "Blue": [
        "Blue", "Navy Blue", "Midnight Blue",
        "Royal Blue", "Sky Blue", "Baby Blue", "Cobalt Blue"
    ],

    "Beige": [
        "Beige", "Sand", "Khaki", "Cream Beige"
    ],

    "Brown": [
        "Brown", "Dark Brown", "Chocolate Brown",
        "Coffee Brown", "Tan", "Camel"
    ],

    "Green": [
        "Green", "Olive Green", "Forest Green",
        "Sage Green", "Mint Green", "Emerald Green"
    ],

    "Red": [
        "Red", "Maroon", "Burgundy", "Wine Red",
        "Crimson"
    ],

    "Pink": [
        "Pink", "Blush Pink", "Rose Pink",
        "Hot Pink", "Dusty Pink"
    ],

    "Purple": [
        "Purple", "Lavender", "Violet", "Plum"
    ],

    "Yellow": [
        "Yellow", "Mustard", "Golden Yellow"
    ],

    "Orange": [
        "Orange", "Rust", "Burnt Orange",
        "Terracotta"
    ]
}

ANALYSED_PRODUCTS_QUERY = """
WITH combinations (
    top_type,
    top_color,
    bottom_type,
    bottom_color
) AS (
    VALUES {values}
)
SELECT
top.product_name       AS top_product_name,
top.type  AS top_product_type,
top.product_id ::TEXT        AS top_product_id,
top_variant.variant_id ::TEXT AS top_variant_id,
top_variant.color      AS top_color,
top_variant.image_url  AS top_image,
bottom.product_name       AS bottom_product_name,
bottom.type  AS bottom_product_type,
bottom.product_id ::TEXT         AS bottom_product_id,
bottom_variant.variant_id ::TEXT AS bottom_variant_id,
bottom_variant.color      AS bottom_color,
bottom_variant.image_url  AS bottom_image
FROM combinations c

JOIN products top
    ON top.type = c.top_type

JOIN product_variants top_variant
    ON top_variant.product_id = top.product_id
    AND top_variant.color = c.top_color

JOIN products bottom
    ON bottom.type = c.bottom_type

JOIN product_variants bottom_variant
    ON bottom_variant.product_id = bottom.product_id
    AND bottom_variant.color = c.bottom_color

WHERE
    top_variant.quantity > 0
    AND bottom_variant.quantity > 0;
"""