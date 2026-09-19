CREATE TABLE orders (
    order_number VARCHAR(20) PRIMARY KEY,
    customer     VARCHAR(40) NOT NULL,
    total_pence  BIGINT      NOT NULL
);

CREATE TABLE stock (
    sku      VARCHAR(20) PRIMARY KEY,
    on_hand  INT         NOT NULL CHECK (on_hand >= 0)
);

INSERT INTO orders VALUES ('ORD-000001', 'asha', 2499);
INSERT INTO orders VALUES ('ORD-000002', 'ben', 8000);
INSERT INTO orders VALUES ('ORD-000003', 'asha', 1250);
INSERT INTO stock VALUES ('MUG-BLUE', 3);
