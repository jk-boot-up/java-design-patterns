package com.jk.explore.saga;

import java.util.List;

/**
 * The five steps of placing an order, each paired with the action that cancels it out.
 *
 * Read them as five short pairs rather than as a class. Reserve the stock, release the
 * stock. Take the money, give the money back. Create the order, cancel the order. Schedule
 * the shipment, cancel the shipment. Send the email — and nothing, because there is nothing
 * to be done about a sent email.
 *
 * <p>The order they are listed in is a design decision, not an accident. Stock is reserved
 * first because releasing it is the cheapest and most reliable compensation in the set.
 * Payment comes before the order exists so that a declined card costs nothing but a
 * released reservation. The email is last precisely because it cannot be undone.
 */
public final class PlaceOrderSteps {

    private PlaceOrderSteps() {
    }

    /** The whole saga, in the order it runs. */
    public static List<SagaStep> allOf(StockService stock, PaymentService payments,
                                       OrderService orders, ShippingService shipping,
                                       EmailService email) {
        return List.of(
                new ReserveStock(stock),
                new TakePayment(payments),
                new CreateOrder(orders),
                new ScheduleShipment(shipping),
                new SendConfirmationEmail(email));
    }

    /**
     * The same five steps with the email moved up before shipping — the wrong order.
     *
     * This exists to be shown failing. Put a step that cannot be undone in the middle and a
     * later refusal leaves the shop having promised something in writing that it then has to
     * take back. The saga still unwinds everything it can, and reports that it could not
     * unwind this. Nothing in the code is broken; the sequence is.
     */
    public static List<SagaStep> withTheEmailInTheWrongPlace(
            StockService stock, PaymentService payments, OrderService orders,
            ShippingService shipping, EmailService email) {
        return List.of(
                new ReserveStock(stock),
                new TakePayment(payments),
                new CreateOrder(orders),
                new SendConfirmationEmail(email),
                new ScheduleShipment(shipping));
    }

    /** Step one. Its compensation is the cheapest in the saga, which is why it is first. */
    public static final class ReserveStock implements SagaStep {

        private final StockService stock;

        public ReserveStock(StockService stock) {
            this.stock = stock;
        }

        @Override
        public String name() {
            return "reserve stock";
        }

        @Override
        public void execute(SagaContext context) {
            context.reservationRef(stock.reserve(context));
        }

        @Override
        public void compensate(SagaContext context) {
            stock.release(context.reservationRef());
        }
    }

    /** Step two. Compensating this one costs the shop a fee and the customer a phone call. */
    public static final class TakePayment implements SagaStep {

        private final PaymentService payments;

        public TakePayment(PaymentService payments) {
            this.payments = payments;
        }

        @Override
        public String name() {
            return "take payment";
        }

        @Override
        public void execute(SagaContext context) {
            context.chargeRef(payments.charge(context));
        }

        @Override
        public void compensate(SagaContext context) {
            payments.refund(context.chargeRef());
        }
    }

    /** Step three. Cancelling an order sets a state; it does not delete anything. */
    public static final class CreateOrder implements SagaStep {

        private final OrderService orders;

        public CreateOrder(OrderService orders) {
            this.orders = orders;
        }

        @Override
        public String name() {
            return "create order";
        }

        @Override
        public void execute(SagaContext context) {
            context.orderRef(orders.create(context));
        }

        @Override
        public void compensate(SagaContext context) {
            orders.cancel(context.orderRef());
        }
    }

    /** Step four, and the one most likely to refuse for reasons nobody here controls. */
    public static final class ScheduleShipment implements SagaStep {

        private final ShippingService shipping;

        public ScheduleShipment(ShippingService shipping) {
            this.shipping = shipping;
        }

        @Override
        public String name() {
            return "schedule shipment";
        }

        @Override
        public void execute(SagaContext context) {
            context.shipmentRef(shipping.schedule(context));
        }

        @Override
        public void compensate(SagaContext context) {
            shipping.cancel(context.shipmentRef());
        }
    }

    /**
     * Step five, last on purpose: there is no way to unsend it.
     *
     * {@link #canBeCompensated()} returns false, and {@link #compensate} does nothing but
     * say so. A step that cannot be compensated is not a bug to be fixed — it is a fact
     * about the world, and the only thing a saga can do with it is put it last.
     */
    public static final class SendConfirmationEmail implements SagaStep {

        private final EmailService email;

        public SendConfirmationEmail(EmailService email) {
            this.email = email;
        }

        @Override
        public String name() {
            return "send confirmation email";
        }

        @Override
        public void execute(SagaContext context) {
            email.send(context);
            context.emailSent(true);
        }

        @Override
        public void compensate(SagaContext context) {
            // Deliberately empty. See canBeCompensated.
        }

        @Override
        public boolean canBeCompensated() {
            return false;
        }
    }
}
