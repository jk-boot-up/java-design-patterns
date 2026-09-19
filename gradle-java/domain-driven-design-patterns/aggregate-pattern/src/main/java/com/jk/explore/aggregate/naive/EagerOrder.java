package com.jk.explore.aggregate.naive;

/** An order that holds the whole customer object, so loading an order loads the customer too. */
public class EagerOrder {

    private final CustomerRecord customer;

    public EagerOrder(CustomerRecord customer) {
        this.customer = customer;
    }

    public String customerName() {
        return customer.name();
    }
}
