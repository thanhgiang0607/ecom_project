WITH clean_orders AS (
    SELECT 
        order_id,
        customer_id,
        order_status,
        CAST(order_purchase_timestamp AS TIMESTAMP) as purchase_at,
        CAST(order_approved_at AS TIMESTAMP) as approved_at,
        CAST(order_delivered_carrier_date AS TIMESTAMP) as carrier_delivered_at,
        CAST(order_delivered_customer_date AS TIMESTAMP) as customer_delivered_at,
        CAST(order_estimated_delivery_date AS TIMESTAMP) as estimated_at
    FROM read_csv_auto('data/raw/olist_orders_dataset.csv')
),

clean_products AS (
    SELECT 
        p.product_id,
        COALESCE(t.product_category_name_english, 'unknown') as category_english,
        p.product_weight_g
    FROM read_csv_auto('data/raw/olist_products_dataset.csv') p
    LEFT JOIN read_csv_auto('data/raw/product_category_name_translation.csv') t 
        ON p.product_category_name = t.product_category_name
),

clean_items AS (
    SELECT 
        order_id,
        product_id,
        price,
        freight_value
    FROM read_csv_auto('data/raw/olist_order_items_dataset.csv')
)

SELECT 
    o.*,
    i.product_id,
    i.price,
    i.freight_value,
    p.category_english as product_category
FROM clean_orders o
LEFT JOIN clean_items i ON o.order_id = i.order_id
LEFT JOIN clean_products p ON i.product_id = p.product_id