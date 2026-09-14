package com.jk.explore.saga;

/**
 * Four calls in a row inside a try block. What everybody writes first, and it compiles.
 *
 * The method below carries a comment where a real version of this class would carry
 * {@code @Transactional}, and that annotation would be the most dangerous thing in the file.
 * It does exactly what it says: it wraps this method in a transaction on <em>this service's
 * own database</em>. It has no reach into Stock's database, none into Payments, and none over
 * the card network. Rolling back a transaction that never touched the money does not bring
 * the money back.
 *
 * <p>So when shipping refuses, this method lands in the catch block, writes a line to a log,
 * and returns null. The stock stays reserved, the card stays charged, the order stays
 * confirmed, and nothing ships. Every test in {@code NaiveCheckoutServiceTest} passes,
 * because nothing in that sentence throws.
 *
 * <p>The log line, incidentally, is read for the first time three weeks later by somebody
 * investigating a complaint.
 */
public final class NaiveCheckoutService {

    private final StockService stock;
    private final PaymentService payments;
    private final OrderService orders;
    private final ShippingService shipping;
    private final CallLog log;

    public NaiveCheckoutService(StockService stock, PaymentService payments,
                                OrderService orders, ShippingService shipping,
                                CallLog log) {
        this.stock = stock;
        this.payments = payments;
        this.orders = orders;
        this.shipping = shipping;
        this.log = log;
    }

    /**
     * Places the order, or does not, and either way tells the caller very little.
     *
     * @return the shipment reference, or {@code null} if something went wrong somewhere
     */
    // @Transactional  <- a real one would be here, and it would protect nothing
    public String placeOrder(SagaContext context) {
        try {
            context.reservationRef(stock.reserve(context));
            context.chargeRef(payments.charge(context));
            context.orderRef(orders.create(context));
            context.shipmentRef(shipping.schedule(context));
            return context.shipmentRef();
        } catch (RuntimeException failure) {
            log.note("NaiveCheckout", "LOGGED-IT", failure.getMessage()
                    + " (nothing was undone)");
            return null;
        }
    }
}
