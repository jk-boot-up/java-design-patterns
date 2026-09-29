package com.jk.explore.lenses;

/**
 * One small lens per field, written once. Deeper lenses are built by joining them.
 */
public final class Lenses {

    public static final Lens<Order, Customer> ORDER_CUSTOMER =
            new Lens<>(Order::customer, (o, c) -> new Order(o.id(), c, o.lines()));

    public static final Lens<Customer, Address> CUSTOMER_ADDRESS =
            new Lens<>(Customer::address, (c, a) -> new Customer(c.name(), a));

    public static final Lens<Address, String> ADDRESS_POSTCODE =
            new Lens<>(Address::postcode, (a, p) -> new Address(a.street(), a.city(), p));

    public static final Lens<Address, String> ADDRESS_CITY =
            new Lens<>(Address::city, (a, c) -> new Address(a.street(), c, a.postcode()));

    /** Joined: from an order straight to its delivery address. */
    public static final Lens<Order, Address> ORDER_ADDRESS = ORDER_CUSTOMER.andThen(CUSTOMER_ADDRESS);

    public static final Lens<Order, String> ORDER_POSTCODE = ORDER_ADDRESS.andThen(ADDRESS_POSTCODE);

    public static final Lens<Order, String> ORDER_CITY = ORDER_ADDRESS.andThen(ADDRESS_CITY);

    private Lenses() {
    }
}
