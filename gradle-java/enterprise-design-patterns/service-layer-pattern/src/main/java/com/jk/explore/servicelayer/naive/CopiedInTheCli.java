package com.jk.explore.servicelayer.naive;

import com.jk.explore.servicelayer.domain.CartLine;
import com.jk.explore.servicelayer.domain.EmailService;
import com.jk.explore.servicelayer.domain.Order;
import com.jk.explore.servicelayer.domain.OrderRejectedException;
import com.jk.explore.servicelayer.domain.OrderRequest;
import com.jk.explore.servicelayer.domain.PaymentGateway;
import com.jk.explore.servicelayer.domain.Product;
import com.jk.explore.servicelayer.domain.Shop;
import com.jk.explore.servicelayer.toydb.Database;
import com.jk.explore.servicelayer.toydb.Row;

import java.util.List;

/**
 * <strong>The second door: support staff's command line, with the logic copied.</strong>
 * It was copied before the web door was fixed to reserve stock first, so it
 * still takes payment first. Nobody remembers there are two copies.
 */
public class CopiedInTheCli {

    private final Database db;
    private final List<Product> products;
    private final PaymentGateway payments;
    private final EmailService email;

    public CopiedInTheCli(Database db, List<Product> products, PaymentGateway payments, EmailService email) {
        this.db = db;
        this.products = products;
        this.payments = payments;
        this.email = email;
    }

    public String placeOrder(OrderRequest request) {
        try {
            Order order = Order.from(1, request, products);
            payments.charge(request.customerId(), order.totalPence());
            for (CartLine line : request.lines()) {
                products.get(line.productId() - 1).reserve(line.quantity());
            }
            db.table(Shop.ORDERS).insert(order.id(), Row.of("customer_id", order.customerId()));
            email.confirm(order.customerId(), order.id());
            return "placed";
        } catch (OrderRejectedException e) {
            return "refused: " + e.getMessage();
        }
    }
}
