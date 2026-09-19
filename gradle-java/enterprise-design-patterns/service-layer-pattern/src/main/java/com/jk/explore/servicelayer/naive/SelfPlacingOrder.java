package com.jk.explore.servicelayer.naive;

import com.jk.explore.servicelayer.domain.EmailService;
import com.jk.explore.servicelayer.domain.PaymentGateway;
import com.jk.explore.servicelayer.domain.Product;
import com.jk.explore.servicelayer.toydb.Database;

import java.util.List;

/**
 * <strong>The other naive version: put it all in the domain object.</strong>
 * {@code order.place()} looks tidy, until the order needs a payment gateway,
 * an email service, the products and a database. It is no longer a domain
 * object; the constructor shows it.
 */
public class SelfPlacingOrder {

    private final int id;
    private final int customerId;
    private final PaymentGateway payments;
    private final EmailService email;
    private final Database db;
    private final List<Product> products;

    public SelfPlacingOrder(int id, int customerId, PaymentGateway payments, EmailService email,
                            Database db, List<Product> products) {
        this.id = id;
        this.customerId = customerId;
        this.payments = payments;
        this.email = email;
        this.db = db;
        this.products = products;
    }

    public int id() {
        return id;
    }

    public int customerId() {
        return customerId;
    }
}
