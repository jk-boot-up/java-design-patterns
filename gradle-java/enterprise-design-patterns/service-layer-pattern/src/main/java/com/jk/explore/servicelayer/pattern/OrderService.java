package com.jk.explore.servicelayer.pattern;

import com.jk.explore.servicelayer.domain.CartLine;
import com.jk.explore.servicelayer.domain.EmailService;
import com.jk.explore.servicelayer.domain.Order;
import com.jk.explore.servicelayer.domain.OrderRequest;
import com.jk.explore.servicelayer.domain.PaymentGateway;
import com.jk.explore.servicelayer.domain.Product;
import com.jk.explore.servicelayer.domain.Shop;
import com.jk.explore.servicelayer.toydb.Database;
import com.jk.explore.servicelayer.toydb.Row;

import java.util.List;

/**
 * <strong>The service layer: one {@code placeOrder}.</strong> It owns the
 * orchestration and the transaction boundary. The rules, that a cart is not
 * empty and that stock cannot go negative, are the domain's, called from here.
 */
public class OrderService {

    private final Database db;
    private final List<Product> products;
    private final PaymentGateway payments;
    private final EmailService email;

    public OrderService(Database db, List<Product> products, PaymentGateway payments, EmailService email) {
        this.db = db;
        this.products = products;
        this.payments = payments;
        this.email = email;
    }

    public Order placeOrder(OrderRequest request) {
        db.begin();
        try {
            Order order = Order.from(1, request, products);
            for (CartLine line : request.lines()) {
                products.get(line.productId() - 1).reserve(line.quantity());
            }
            payments.charge(request.customerId(), order.totalPence());
            db.table(Shop.ORDERS).insert(order.id(), Row.of("customer_id", order.customerId()));
            db.commit();
            email.confirm(order.customerId(), order.id());
            return order;
        } catch (RuntimeException e) {
            db.rollback();
            throw e;
        }
    }
}
