WITH top_customers AS (
    SELECT
        o.customer_id,
        SUM(o.total_amount) AS total_spent
    FROM
        Orders o
        JOIN Order_Items oi ON o.order_id = oi.order_id
    WHERE
        o.order_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY
        o.customer_id
    ORDER BY
        SUM(o.total_amount) DESC
    LIMIT 5
),
top_5_customer_orders AS (
    SELECT
        o.customer_id,
        o.order_id,
        tc.total_spent
    FROM
        top_customers tc
        JOIN Orders o ON tc.customer_id = o.customer_id
)
SELECT DISTINCT ON (c.customer_id)
    c.customer_id,
    c.customer_name,
    c.email,
    t5co.total_spent,
    p.category AS most_purchased_category
FROM
    top_5_customer_orders t5co
    JOIN Order_Items oi ON t5co.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    JOIN Customers c ON t5co.customer_id = c.customer_id
ORDER BY
    c.customer_id,
    oi.quantity * oi.price_per_unit DESC
;