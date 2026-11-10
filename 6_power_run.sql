CREATE OR REPLACE VIEW vw_fraud_velocity_alerts AS
WITH DeviceVelocity AS (
    SELECT 
        d.device_id,
        d.ip_address,
        u.email,
        COUNT(p.payment_id) AS failed_attempts,
        SUM(o.order_amount) AS total_fraud_value,
        MIN(p.transaction_time) AS first_attempt,
        MAX(p.transaction_time) AS last_attempt,
        TIMESTAMPDIFF(SECOND, MIN(p.transaction_time), MAX(p.transaction_time)) AS duration_seconds
    FROM devices d
    JOIN orders o ON d.device_id = o.device_id
    JOIN payments p ON o.order_id = p.order_id
    JOIN users u ON o.user_id = u.user_id
    WHERE p.payment_status = 'failed'
    GROUP BY 
        d.device_id, 
        d.ip_address, 
        u.email
)
SELECT * FROM DeviceVelocity
WHERE failed_attempts >= 3 AND duration_seconds < 60;