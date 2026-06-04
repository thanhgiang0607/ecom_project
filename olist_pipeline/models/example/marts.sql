WITH base_cleaned AS (
    SELECT * FROM {{ ref('staging') }}
),

order_payments_aggregated AS (
    SELECT 
        order_id,
        SUM(payment_value) as total_amount_paid
    FROM read_csv_auto('data/raw/olist_order_payments_dataset.csv')
    GROUP BY order_id
),

order_metrics AS (
    SELECT 
        order_id,
        customer_id,
        order_status,
        purchase_at,
        product_category,
        SUM(price) as total_item_price,
        SUM(freight_value) as total_shipping_cost,
        COUNT(product_id) as total_items_ordered,
        
        CASE 
            WHEN customer_delivered_at IS NOT NULL 
            THEN date_diff('day', purchase_at, customer_delivered_at)
            ELSE NULL 
        END as actual_delivery_days,
        
        CASE 
            WHEN customer_delivered_at IS NOT NULL 
            THEN date_diff('day', estimated_at, customer_delivered_at)
            ELSE NULL 
        END as days_delayed_vs_estimate
    FROM base_cleaned
    GROUP BY 
        order_id, customer_id, order_status, purchase_at, product_category, customer_delivered_at, estimated_at
)

SELECT 
    m.*,
    COALESCE(p.total_amount_paid, 0) as total_amount_paid
FROM order_metrics m
LEFT JOIN order_payments_aggregated p ON m.order_id = p.order_id