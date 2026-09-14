package com.jk.explore.saga;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The orchestrated saga: forwards, backwards, and when backwards goes wrong. */
class SagaTest {

    private static final String CUSTOMER = "cust-7";
    private static final Money BASKET_TOTAL = Money.pence(3499 + 4 * 899);

    private CallLog log;
    private StockService stock;
    private PaymentService payments;
    private OrderService orders;
    private ShippingService shipping;
    private EmailService email;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        stock = new StockService(clock, log);
        payments = new PaymentService(clock, log);
        orders = new OrderService(clock, log);
        shipping = new ShippingService(clock, log);
        email = new EmailService(clock, log);
        stock.stock("SKU-KETTLE", 20);
        stock.stock("SKU-MUG", 50);
    }

    private SagaOrchestrator saga() {
        return new SagaOrchestrator(
                PlaceOrderSteps.allOf(stock, payments, orders, shipping, email), log);
    }

    private SagaContext basket(String orderId) {
        return new SagaContext(orderId, CUSTOMER, List.of(
                new SagaContext.Line("SKU-KETTLE", 1, Money.pence(3499)),
                new SagaContext.Line("SKU-MUG", 4, Money.pence(899))));
    }

    @Test
    @DisplayName("all five steps run and the order is placed")
    void theHappyPath() {
        SagaOutcome outcome = saga().run(basket("ord-1"));

        assertTrue(outcome.succeeded());
        assertEquals(19, stock.available("SKU-KETTLE"));
        assertEquals(BASKET_TOTAL, payments.netTaken());
        assertEquals(OrderService.State.CONFIRMED, orders.stateOf("ord-1"));
        assertEquals(1, shipping.shipmentsScheduled());
        assertEquals(1, email.sent().size());
    }

    @Test
    @DisplayName("a refusal at the last step undoes the four before it")
    void itCompensatesInReverse() {
        shipping.refuseEveryPostcode();

        SagaOutcome outcome = saga().run(basket("ord-2"));

        assertEquals(SagaOutcome.Status.COMPENSATED, outcome.status());
        assertEquals("schedule shipment", outcome.failedStep());
        assertEquals(List.of("create order", "take payment", "reserve stock"),
                outcome.compensated());
    }

    @Test
    @DisplayName("after compensating, the shop is holding no money and no reservation")
    void compensationPutsTheShopBack() {
        shipping.refuseEveryPostcode();

        saga().run(basket("ord-3"));

        assertEquals(Money.pence(0), payments.netTaken());
        assertEquals(20, stock.available("SKU-KETTLE"));
        assertEquals(50, stock.available("SKU-MUG"));
        assertEquals(0, stock.reservationsHeld());
        assertEquals(OrderService.State.CANCELLED, orders.stateOf("ord-3"));
        assertEquals(0, shipping.shipmentsScheduled());
    }

    @Test
    @DisplayName("compensation is not rollback: the charge and the refund both stay")
    void aRefundIsANewFactNotAnErasure() {
        shipping.refuseEveryPostcode();

        saga().run(basket("ord-4"));

        List<PaymentService.Entry> ledger = payments.entries();
        assertEquals(2, ledger.size());
        assertEquals("CHARGE", ledger.get(0).kind());
        assertEquals("REFUND", ledger.get(1).kind());
        assertEquals(BASKET_TOTAL, ledger.get(0).amount());
        assertEquals(Money.pence(0), payments.netTaken());
    }

    @Test
    @DisplayName("a declined card costs nothing but a released reservation")
    void anEarlyFailureIsCheap() {
        payments.declineEverything();

        SagaOutcome outcome = saga().run(basket("ord-5"));

        assertEquals("take payment", outcome.failedStep());
        assertEquals(List.of("reserve stock"), outcome.compensated());
        assertEquals(20, stock.available("SKU-KETTLE"));
        assertEquals(0, payments.entries().size());
        assertNull(orders.stateOf("ord-5"));
    }

    @Test
    @DisplayName("the first step failing leaves nothing to compensate")
    void nothingToUndo() {
        stock.stock("SKU-KETTLE", 0);

        SagaOutcome outcome = saga().run(basket("ord-6"));

        assertEquals("reserve stock", outcome.failedStep());
        assertEquals(List.of(), outcome.compensated());
        assertEquals(SagaOutcome.Status.COMPENSATED, outcome.status());
    }

    @Test
    @DisplayName("a failed compensation is reported, not swallowed")
    void aFailedCompensationNeedsAHuman() {
        shipping.refuseEveryPostcode();
        payments.failNextRefund(1);

        SagaOutcome outcome = saga().run(basket("ord-7"));

        assertTrue(outcome.needsHumanHelp());
        assertEquals(List.of("take payment"), outcome.couldNotCompensate());
        assertEquals(BASKET_TOTAL, payments.netTaken());
    }

    @Test
    @DisplayName("a failed compensation does not stop the other compensations")
    void unwindingCarriesOn() {
        shipping.refuseEveryPostcode();
        payments.failNextRefund(1);

        SagaOutcome outcome = saga().run(basket("ord-8"));

        assertEquals(List.of("create order", "reserve stock"), outcome.compensated());
        assertEquals(OrderService.State.CANCELLED, orders.stateOf("ord-8"));
        assertEquals(20, stock.available("SKU-KETTLE"));
    }

    @Test
    @DisplayName("the saga never throws, whatever happens underneath")
    void itAlwaysReturnsAnOutcome() {
        shipping.refuseEveryPostcode();
        payments.failNextRefund(1);
        orders.failNextCancel(1);
        stock.failNextRelease(1);

        SagaOutcome outcome = saga().run(basket("ord-9"));

        assertTrue(outcome.needsHumanHelp());
        assertEquals(3, outcome.couldNotCompensate().size());
        assertEquals(List.of(), outcome.compensated());
    }

    @Test
    @DisplayName("an outage is reported the same way a refusal is")
    void anOutageIsJustAnotherFailedStep() {
        shipping.failNextSchedule(1);

        SagaOutcome outcome = saga().run(basket("ord-10"));

        assertEquals(SagaOutcome.Status.COMPENSATED, outcome.status());
        assertEquals(Money.pence(0), payments.netTaken());
    }

    @Test
    @DisplayName("a step that cannot be undone is named, not quietly skipped")
    void theEmailCannotBeCompensated() {
        shipping.refuseEveryPostcode();

        SagaOutcome outcome = new SagaOrchestrator(
                PlaceOrderSteps.withTheEmailInTheWrongPlace(stock, payments, orders,
                        shipping, email), log).run(basket("ord-11"));

        assertTrue(outcome.needsHumanHelp());
        assertEquals(List.of("send confirmation email"), outcome.couldNotCompensate());
        assertEquals(1, email.sent().size());
        // Everything that could be undone still was: the money is back and the shelf is full.
        assertEquals(Money.pence(0), payments.netTaken());
        assertEquals(20, stock.available("SKU-KETTLE"));
    }

    @Test
    @DisplayName("in the right order, the email is only ever sent for orders that stand")
    void theEmailGoesLast() {
        shipping.refuseEveryPostcode();

        saga().run(basket("ord-12"));

        assertEquals(0, email.sent().size());
    }

    @Test
    @DisplayName("the timeline shows the steps forwards and the undo backwards")
    void theTimelineTellsTheStory() {
        shipping.refuseEveryPostcode();

        saga().run(basket("ord-13"));

        String timeline = log.timeline();
        assertTrue(timeline.contains("STEP-OK"), timeline);
        assertTrue(timeline.contains("STEP-FAILED"), timeline);
        assertTrue(timeline.contains("UNDONE"), timeline);
        assertTrue(timeline.indexOf("STEP-FAILED") < timeline.indexOf("UNDONE"), timeline);
    }

    @Test
    @DisplayName("each step commits on its own, with no transaction spanning them")
    void everyStepIsAlreadyCommittedWhenTheNextOneStarts() {
        shipping.refuseEveryPostcode();
        SagaContext context = basket("ord-14");

        saga().run(context);

        // The references are still in the context: these were real, committed operations
        // that had to be actively cancelled out rather than rolled back.
        assertFalse(context.chargeRef() == null);
        assertFalse(context.reservationRef() == null);
        assertNull(context.shipmentRef());
    }
}
