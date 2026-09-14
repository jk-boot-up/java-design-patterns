package com.jk.explore.saga;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The four-calls-in-a-try-block version, and the point of this class is that every test in it
 * passes.
 *
 * Nothing here is marked as expected to fail, nothing is disabled, and there is no assertion
 * about an exception, because there is no exception. The shop takes the money, keeps the
 * stock reserved, leaves the order confirmed, ships nothing, and writes a line to a log. A
 * suite that only asks "did it throw" says this code is fine.
 */
class NaiveCheckoutServiceTest {

    private static final Money BASKET_TOTAL = Money.pence(3499 + 4 * 899);

    private CallLog log;
    private StockService stock;
    private PaymentService payments;
    private OrderService orders;
    private ShippingService shipping;
    private NaiveCheckoutService checkout;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        log = new CallLog(clock);
        stock = new StockService(clock, log);
        payments = new PaymentService(clock, log);
        orders = new OrderService(clock, log);
        shipping = new ShippingService(clock, log);
        stock.stock("SKU-KETTLE", 20);
        stock.stock("SKU-MUG", 50);
        checkout = new NaiveCheckoutService(stock, payments, orders, shipping, log);
    }

    private SagaContext basket(String orderId) {
        return new SagaContext(orderId, "cust-7", List.of(
                new SagaContext.Line("SKU-KETTLE", 1, Money.pence(3499)),
                new SagaContext.Line("SKU-MUG", 4, Money.pence(899))));
    }

    @Test
    @DisplayName("when nothing goes wrong it is perfectly good code")
    void theHappyPathIsFine() {
        String shipment = checkout.placeOrder(basket("ord-1"));

        assertEquals("shp-1", shipment);
        assertEquals(BASKET_TOTAL, payments.netTaken());
        assertEquals(OrderService.State.CONFIRMED, orders.stateOf("ord-1"));
    }

    @Test
    @DisplayName("when shipping refuses, nothing throws")
    void theFailureIsSilent() {
        shipping.refuseEveryPostcode();

        String shipment = checkout.placeOrder(basket("ord-2"));

        assertNull(shipment);
    }

    @Test
    @DisplayName("the card is still charged")
    void theMoneyStaysTaken() {
        shipping.refuseEveryPostcode();

        checkout.placeOrder(basket("ord-3"));

        assertEquals(BASKET_TOTAL, payments.netTaken());
        assertEquals(1, payments.entries().size());
    }

    @Test
    @DisplayName("the kettle is still off the shelf")
    void theStockStaysReserved() {
        shipping.refuseEveryPostcode();

        checkout.placeOrder(basket("ord-4"));

        assertEquals(19, stock.available("SKU-KETTLE"));
        assertEquals(1, stock.reservationsHeld());
    }

    @Test
    @DisplayName("the order is still confirmed, and nothing will ever ship against it")
    void theOrderStaysConfirmed() {
        shipping.refuseEveryPostcode();

        checkout.placeOrder(basket("ord-5"));

        assertEquals(OrderService.State.CONFIRMED, orders.stateOf("ord-5"));
        assertEquals(0, shipping.shipmentsScheduled());
    }

    @Test
    @DisplayName("all that happened was a line in a log")
    void thereIsALogLineAndNothingElse() {
        shipping.refuseEveryPostcode();

        checkout.placeOrder(basket("ord-6"));

        assertTrue(log.timeline().contains("nothing was undone"), log.timeline());
    }
}
