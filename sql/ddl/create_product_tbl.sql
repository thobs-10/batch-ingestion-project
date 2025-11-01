CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    sale_id INT REFERENCES sales(sale_id),
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    sku_number VARCHAR(100) UNIQUE,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- indexes
CREATE INDEX idx_sku_number ON products(sku_number);
