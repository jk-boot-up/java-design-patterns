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

import java.util.List;

/**
 * <strong>The logic in the controller.</strong> Where every application
 * starts, and with one entry point it works. Validate, reserve stock, take
 * payment, write the order, send the email.
 */
public class ControllerLogic {

    private final Database db;
    private final List<Product> products;
    private final PaymentGateway payments;
    private final EmailService email;

    public ControllerLogic(Database db, List<Product> products, PaymentGateway payments, EmailService email) {
        this.db = db;
        this.products = products;
        this.payments = payments;
        this.email = email;
    }

    /** The web door: stock is reserved first, so a refused order costs the customer nothing. */
    public String placeOrder(OrderRequest request) {
        try {
            Order order = Order.from(1, request, products);
            for (CartLine line : request.lines()) {
                products.get(line.productId() - 1).reserve(line.quantity());
            }
            payments.charge(request.customerId(), order.totalPence());
            db.table(Shop.ORDERS).insert(order.id(), com.jk.explore.servicelayer.toydb.Row.of("customer_id", order.customerId()));
            email.confirm(order.customerId(), order.id());
            return "placed";
        } catch (OrderRejectedException e) {
            return "refused: " + e.getMessage();
        }
    }
}
