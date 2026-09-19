CREATE TABLE products (
    sku VARCHAR(20) PRIMARY KEY,
    price_pence BIGINT NOT NULL,
    cost_pence BIGINT NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0)
);
CREATE TABLE orders (
    id VARCHAR(20) PRIMARY KEY,
    customer VARCHAR(40) NOT NULL,
    sku VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    total_pence BIGINT NOT NULL,
    cost_pence BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL
);
INSERT INTO products VALUES ('ESP-001', 30000, 21000, 5);
INSERT INTO products VALUES ('BNS-220', 1250, 600, 10);
