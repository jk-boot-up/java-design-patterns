package com.jk.explore.transactionaloutbox;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * Save the order, then publish the event — and every test here passes.
 *
 * That is the point. The last three tests describe an order that was placed, charged, and
 * never announced to anybody, and they are green, because nothing in that sentence throws and
 * the order looks perfect from the Orders service's own side. A suite like this is what lets
 * the two lines live in production for a year before anyone notices.
 */
class NaiveOrderServiceTest {

    private OrderDatabase database;
    private MessageBroker broker;
    private NotificationService notifications;
    private NaiveOrderService orders;

    @BeforeEach
    void setUp() {
        SimulatedClock clock = new SimulatedClock();
        CallLog log = new CallLog(clock);
        database = new OrderDatabase(log);
        broker = new MessageBroker(clock, log);
        notifications = new NotificationService(log);
        broker.subscribe(notifications::on);
        orders = new NaiveOrderService(database, broker, log);
    }

    private static Order order(String orderId) {
        return new Order(orderId, "cust-7", Money.pence(7095));
    }

    @Test
    @DisplayName("on a good day it saves the order and announces it")
    void theHappyPathIsFine() {
        orders.placeOrder(order("ord-1"));

        assertEquals(1, database.orderCount());
        assertEquals(1, broker.deliveredCount());
        assertEquals(1, notifications.emailsSent());
    }

    @Test
    @DisplayName("the crash between the two lines is the only thing that goes wrong")
    void theCrashIsNarrow() {
        orders.dieBetweenTheTwoLines();

        assertThrows(ProcessDiedException.class, () -> orders.placeOrder(order("ord-2")));
    }

    @Test
    @DisplayName("and the order is still there, looking perfectly healthy")
    void theOrderSurvives() {
        orders.dieBetweenTheTwoLines();
        try {
            orders.placeOrder(order("ord-3"));
        } catch (ProcessDiedException expected) {
            // In production this catch block does not run. The JVM is gone.
        }

        assertNotNull(database.find("ord-3"));
        assertEquals(Money.pence(7095), database.find("ord-3").total());
    }

    @Test
    @DisplayName("nobody was told, and nothing is left that knows anybody should be")
    void theEventIsLostForever() {
        orders.dieBetweenTheTwoLines();
        try {
            orders.placeOrder(order("ord-4"));
        } catch (ProcessDiedException expected) {
            // Same again.
        }

        assertEquals(0, broker.deliveredCount());
        assertEquals(0, notifications.emailsSent());
        // There is no out-tray, no pending row, nothing to sweep. Nothing will ever retry.
        assertEquals(0, database.outboxSize());
    }
}
