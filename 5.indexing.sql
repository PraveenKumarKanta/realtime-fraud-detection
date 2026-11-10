-- Index the foreign keys used in our JOINs (Crucial for performance)
CREATE INDEX idx_orders_device ON orders(device_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_payments_order ON payments(order_id);

-- Index the WHERE clause filter to instantly find failed payments
CREATE INDEX idx_payments_status ON payments(payment_status);

-- Composite index for the transaction time (helps with the MIN/MAX calculations)
CREATE INDEX idx_payments_status_time ON payments(payment_status, transaction_time);