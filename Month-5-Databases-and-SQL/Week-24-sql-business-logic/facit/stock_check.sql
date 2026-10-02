-- Uppgift 3: beviset. Varje produkts lager jämfört med summan av dess
-- lagerrörelser. Om lagret alltid är rätt är kolumnen difference 0 överallt.
SELECT p.sku,
       p.stock,
       COALESCE(SUM(m.change), 0)           AS sum_of_movements,
       p.stock - COALESCE(SUM(m.change), 0) AS difference
FROM products AS p
LEFT JOIN stock_movements AS m ON m.product_id = p.id
GROUP BY p.id, p.sku, p.stock
ORDER BY p.sku;
