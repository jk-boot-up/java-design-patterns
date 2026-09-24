package com.jk.explore.transactionaloutboxdebezium;

/** One order, as the Orders service stores it. The total is held in whole pence. */
public record Order(String orderId, String customer, long totalPence) {

    /** The order the demo places as number {@code n}: ORD-1, ORD-2 and so on. */
    public static Order number(int n) {
        return new Order("ORD-" + n, "customer-" + n, 1995L + 1000L * n);
    }

    /** The message body the outbox row carries, and that Kafka ends up holding. */
    public String asJson() {
        return "{\"orderId\":\"" + orderId + "\",\"customer\":\"" + customer + "\",\"totalPence\":" + totalPence + "}";
    }
}
