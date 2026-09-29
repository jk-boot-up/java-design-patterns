package com.jk.explore.eventcarried;

/**
 * Before: shipping keeps no customer data, so every label means a call to the customer service.
 */
public final class CallbackShipping {

    private final CustomerService customers;

    public CallbackShipping(CustomerService customers) {
        this.customers = customers;
    }

    public void on(Events.CustomerChanged event) {
        // a thin event says only "something changed": nothing to keep
    }

    /** The label, or null if it could not be printed. */
    public String label(String orderId, String customerId) {
        try {
            return orderId + " -> " + customers.lookup(customerId);
        } catch (IllegalStateException down) {
            return null;
        }
    }
}
