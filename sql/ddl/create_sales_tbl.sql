CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    customer_id INT REFERENCES customers(customer_id),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- CREATE INDEXES
CREATE INDEX idx_product_id ON sales(product_id);
CREATE INDEX idx_customer_id ON sales(customer_id);