package com.jk.explore.observer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/** The subject: what it promises, and what it deliberately does not. */
class OrderTest {

    /** A listener that only records what it was told. */
    private static final class Recorder implements OrderListener {
        private final String name;
        private final List<String> seen = new ArrayList<>();

        Recorder(String name) {
            this.name = name;
        }

        @Override
        public String name() {
            return name;
        }

        @Override
        public void onStatusChanged(OrderEvent event) {
            seen.add(event.describe());
        }
    }

    @Nested
    @DisplayName("notification")
    class Notification {

        @Test
        @DisplayName("every attached listener is told, and told the same thing")
        void everyListenerIsTold() {
            Order order = new Order("A-1");
            Recorder first = new Recorder("first");
            Recorder second = new Recorder("second");
            order.addListener(first);
            order.addListener(second);

            order.moveTo(OrderStatus.PAID);

            assertEquals(List.of("A-1: Placed -> Paid"), first.seen);
            assertEquals(first.seen, second.seen);
        }

        @Test
        @DisplayName("an order with no listeners still changes status")
        void noListenersIsFine() {
            Order order = new Order("A-2");

            assertTrue(order.moveTo(OrderStatus.PAID).isEmpty());
            assertEquals(OrderStatus.PAID, order.status());
        }

        @Test
        @DisplayName("moving to the status it is already in fires nothing")
        void noEventWhenNothingChanged() {
            Order order = new Order("A-3");
            Recorder recorder = new Recorder("r");
            order.addListener(recorder);

            order.moveTo(OrderStatus.PAID);
            order.moveTo(OrderStatus.PAID);

            assertEquals(1, recorder.seen.size(),
                    "a second move to the same status must not send a second email");
        }

        @Test
        @DisplayName("the event carries the status the order came from")
        void eventCarriesTheOldStatus() {
            Order order = new Order("A-4");
            Recorder recorder = new Recorder("r");
            order.addListener(recorder);

            order.moveTo(OrderStatus.PAID);
            order.moveTo(OrderStatus.SHIPPED);

            assertEquals(List.of("A-4: Placed -> Paid", "A-4: Paid -> Shipped"), recorder.seen);
        }

        @Test
        @DisplayName("a listener sees the new status if it looks")
        void statusIsUpdatedBeforeListenersRun() {
            Order order = new Order("A-5");
            List<OrderStatus> observed = new ArrayList<>();
            order.addListener(new OrderListener() {
                @Override
                public String name() {
                    return "peeker";
                }

                @Override
                public void onStatusChanged(OrderEvent event) {
                    observed.add(order.status());
                }
            });

            order.moveTo(OrderStatus.SHIPPED);

            assertEquals(List.of(OrderStatus.SHIPPED), observed);
        }
    }

    @Nested
    @DisplayName("subscription")
    class Subscription {

        @Test
        @DisplayName("a removed listener stops being told")
        void removedListenerStopsHearing() {
            Order order = new Order("A-6");
            Recorder recorder = new Recorder("r");
            order.addListener(recorder);

            order.moveTo(OrderStatus.PAID);
            assertTrue(order.removeListener(recorder));
            order.moveTo(OrderStatus.SHIPPED);

            assertEquals(1, recorder.seen.size());
        }

        @Test
        @DisplayName("removing a listener that was never added reports false")
        void removingAnUnknownListener() {
            assertFalse(new Order("A-7").removeListener(new Recorder("stranger")));
        }

        @Test
        @DisplayName("a listener may unsubscribe itself while being notified")
        void selfRemovalDuringNotification() {
            // The one-shot subscription: "tell me when this ships, then forget
            // me". An ArrayList would throw ConcurrentModificationException.
            Order order = new Order("A-8");
            List<String> fired = new ArrayList<>();
            OrderListener oneShot = new OrderListener() {
                @Override
                public String name() {
                    return "one-shot";
                }

                @Override
                public void onStatusChanged(OrderEvent event) {
                    fired.add(event.describe());
                    order.removeListener(this);
                }
            };
            order.addListener(oneShot);

            order.moveTo(OrderStatus.PAID);
            order.moveTo(OrderStatus.SHIPPED);

            assertEquals(List.of("A-8: Placed -> Paid"), fired);
            assertEquals(0, order.listenerCount());
        }

        @Test
        @DisplayName("null is not a listener and not a status")
        void nullsAreRejected() {
            Order order = new Order("A-9");
            assertThrows(NullPointerException.class, () -> order.addListener(null));
            assertThrows(NullPointerException.class, () -> order.moveTo(null));
        }
    }

    @Nested
    @DisplayName("failure isolation")
    class FailureIsolation {

        private OrderListener throwing(String name, String message) {
            return new OrderListener() {
                @Override
                public String name() {
                    return name;
                }

                @Override
                public void onStatusChanged(OrderEvent event) {
                    throw new IllegalStateException(message);
                }
            };
        }

        @Test
        @DisplayName("a listener that throws does not stop the ones after it")
        void oneFailureDoesNotStopTheRest() {
            Order order = new Order("A-10");
            Recorder before = new Recorder("before");
            Recorder after = new Recorder("after");
            order.addListener(before);
            order.addListener(throwing("email", "SMTP timeout after 30s"));
            order.addListener(after);

            List<ListenerFailure> failures = order.moveTo(OrderStatus.SHIPPED);

            assertEquals(1, before.seen.size());
            assertEquals(1, after.seen.size(), "the listener after the failure must still run");
            assertEquals(List.of(new ListenerFailure("email", "SMTP timeout after 30s")), failures);
        }

        @Test
        @DisplayName("the status change stands even when a listener fails")
        void statusStillChanges() {
            Order order = new Order("A-11");
            order.addListener(throwing("email", "SMTP timeout after 30s"));

            order.moveTo(OrderStatus.SHIPPED);

            assertEquals(OrderStatus.SHIPPED, order.status());
        }

        @Test
        @DisplayName("several failures are all reported, in notification order")
        void everyFailureIsReported() {
            Order order = new Order("A-12");
            order.addListener(throwing("email", "SMTP timeout after 30s"));
            order.addListener(throwing("analytics", "collector unreachable"));

            List<ListenerFailure> failures = order.moveTo(OrderStatus.SHIPPED);

            assertEquals(List.of("email", "analytics"),
                    failures.stream().map(ListenerFailure::listenerName).toList());
        }

        @Test
        @DisplayName("an exception with no message is reported by its type")
        void failureWithoutAMessage() {
            Order order = new Order("A-13");
            order.addListener(new OrderListener() {
                @Override
                public String name() {
                    return "silent";
                }

                @Override
                public void onStatusChanged(OrderEvent event) {
                    throw new IllegalStateException();
                }
            });

            assertEquals(List.of(new ListenerFailure("silent", "IllegalStateException")),
                    order.moveTo(OrderStatus.SHIPPED));
        }
    }
}
