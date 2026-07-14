-- =====================================================
-- TOTAL REVENUE
-- =====================================================

SELECT
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS total_revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id;

-- =====================================================
-- MONTHLY SALES TREND
-- =====================================================

SELECT
strftime('%Y-%m', o.order_date) AS month,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
GROUP BY month
ORDER BY month;

-- =====================================================
-- BLACK FRIDAY ANALYSIS
-- =====================================================

SELECT
strftime('%Y-%m', o.order_date) AS month,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
WHERE strftime('%m', o.order_date) IN ('11','12')
GROUP BY month
ORDER BY month;

-- =====================================================
-- REVENUE BY REGION
-- =====================================================

SELECT
o.region,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
GROUP BY o.region
ORDER BY revenue DESC;

-- =====================================================
-- REVENUE BY CATEGORY
-- =====================================================

SELECT
p.category,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- =====================================================
-- REVENUE BY CUSTOMER SEGMENT
-- =====================================================

SELECT
c.segment,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
GROUP BY c.segment
ORDER BY revenue DESC;

-- =====================================================
-- DISCOUNT ELASTICITY
-- =====================================================

SELECT
oi.discount,
ROUND(AVG(oi.quantity), 2) AS avg_quantity
FROM order_items oi
GROUP BY oi.discount
ORDER BY oi.discount;

-- =====================================================
-- PAYMENT METHOD ANALYSIS
-- =====================================================

SELECT
o.payment_method,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id
GROUP BY o.payment_method
ORDER BY revenue DESC;

-- =====================================================
-- TOP PRODUCTS
-- =====================================================

SELECT
p.product_name,
ROUND(SUM(
    (p.selling_price * oi.quantity) *
    (1 - oi.discount)
), 2) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- =====================================================
-- PROFIT BY CATEGORY
-- =====================================================

SELECT
p.category,

ROUND(SUM(
    ((p.selling_price - p.cost_price)
    * oi.quantity)
    * (1 - oi.discount)
), 2) AS profit

FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id

GROUP BY p.category
ORDER BY profit DESC;