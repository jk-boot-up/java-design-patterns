package com.jk.explore.templatemethod;

import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Tests the base class on its own, against a route that exists only here.
 *
 * <p>Nothing in this file mentions warehouses, sellers or licence keys. If
 * {@code FulfilmentProcess} needed to know about any of them, these tests
 * could not be written.
 */
@DisplayName("FulfilmentProcess — the template method")
class FulfilmentProcessTest {

    /**
     * A route that records nothing but the fact that it was called. Every
     * required step appends its own name to a list, so a test can read back
     * the exact order the base class ran them in.
     */
    static class RecordingRoute extends FulfilmentProcess {

        final List<String> calls = new ArrayList<>();

        @Override
        protected String routeName() {
            return "recording";
        }

        @Override
        protected void reserveStock(Order order, FulfilmentReport report) {
            calls.add("reserveStock");
            report.step("reserve", "-");
        }

        @Override
        protected void charge(Order order, FulfilmentReport report) {
            calls.add("charge");
            report.charged(order.subtotal());
            report.step("charge", "-");
        }

        @Override
        protected void dispatch(Order order, FulfilmentReport report) {
            calls.add("dispatch");
            report.dispatchedAs("REF-" + order.id());
            report.step("dispatch", "-");
        }

        @Override
        protected void pack(Order order, FulfilmentReport report) {
            calls.add("pack");
            super.pack(order, report);
        }

        @Override
        protected void notifyCustomer(Order order, FulfilmentReport report) {
            calls.add("notifyCustomer");
            super.notifyCustomer(order, report);
        }

        @Override
        protected void afterFulfilment(Order order, FulfilmentReport report) {
            calls.add("afterFulfilment");
        }
    }

    private static Order order() {
        return Order.shipped("A-1", "grace@example.com", "4 Blackfriars Road, London",
                List.of(new OrderLine("H-100", "Wireless headphones", Money.pounds(89.99), 2)));
    }

    @Nested
    @DisplayName("the sequence")
    class Sequence {

        @Test
        @DisplayName("runs the steps in the order the base class fixed")
        void runsStepsInOrder() {
            RecordingRoute route = new RecordingRoute();
            route.fulfil(order());
            assertEquals(
                    List.of("reserveStock", "charge", "pack", "dispatch", "notifyCustomer",
                            "afterFulfilment"),
                    route.calls);
        }

        @Test
        @DisplayName("dispatch always runs before the customer is notified")
        void dispatchBeforeNotify() {
            RecordingRoute route = new RecordingRoute();
            route.fulfil(order());
            assertTrue(route.calls.indexOf("dispatch") < route.calls.indexOf("notifyCustomer"));
        }

        @Test
        @DisplayName("stock is reserved before the card is charged")
        void reserveBeforeCharge() {
            RecordingRoute route = new RecordingRoute();
            route.fulfil(order());
            assertTrue(route.calls.indexOf("reserveStock") < route.calls.indexOf("charge"));
        }

        @Test
        @DisplayName("the report names the same six steps whatever the route did")
        void reportNamesSixSteps() {
            FulfilmentReport report = new RecordingRoute().fulfil(order());
            assertEquals(List.of("validate", "reserve", "charge", "pack", "dispatch", "notify"),
                    report.stepNames());
        }

        @Test
        @DisplayName("a step that throws stops the ones after it")
        void aThrowingStepStopsTheRest() {
            RecordingRoute route = new RecordingRoute() {
                @Override
                protected void charge(Order o, FulfilmentReport r) {
                    calls.add("charge");
                    throw new FulfilmentException("card declined");
                }
            };
            assertThrows(FulfilmentException.class, () -> route.fulfil(order()));
            assertFalse(route.calls.contains("dispatch"));
            assertFalse(route.calls.contains("notifyCustomer"));
        }

        @Test
        @DisplayName("the report carries the route's own name")
        void reportCarriesRouteName() {
            assertEquals("recording", new RecordingRoute().fulfil(order()).route());
        }
    }

    @Nested
    @DisplayName("validation, which no route can replace")
    class Validation {

        @Test
        @DisplayName("an order with no lines is refused")
        void refusesEmptyOrder() {
            Order empty = Order.shipped("A-2", "grace@example.com", "London", List.of());
            FulfilmentException e = assertThrows(FulfilmentException.class,
                    () -> new RecordingRoute().fulfil(empty));
            assertTrue(e.getMessage().contains("no lines"));
        }

        @Test
        @DisplayName("an order with no customer email is refused")
        void refusesMissingEmail() {
            Order noEmail = new Order("A-3", "  ", "London",
                    List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), 1)));
            FulfilmentException e = assertThrows(FulfilmentException.class,
                    () -> new RecordingRoute().fulfil(noEmail));
            assertTrue(e.getMessage().contains("no customer email"));
        }

        @Test
        @DisplayName("validation runs before any step of the route's own")
        void validationRunsFirst() {
            RecordingRoute route = new RecordingRoute();
            Order empty = Order.shipped("A-4", "grace@example.com", "London", List.of());
            assertThrows(FulfilmentException.class, () -> route.fulfil(empty));
            assertTrue(route.calls.isEmpty());
        }

        @Test
        @DisplayName("validate is the first step on the report")
        void validateIsRecordedFirst() {
            FulfilmentReport report = new RecordingRoute().fulfil(order());
            assertEquals("validate", report.steps().get(0).name());
        }
    }

    @Nested
    @DisplayName("the hooks")
    class Hooks {

        @Test
        @DisplayName("by default a shipping address is required")
        void addressRequiredByDefault() {
            Order noAddress = Order.addressless("A-5", "grace@example.com",
                    List.of(new OrderLine("H-100", "Headphones", Money.pounds(89.99), 1)));
            FulfilmentException e = assertThrows(FulfilmentException.class,
                    () -> new RecordingRoute().fulfil(noAddress));
            assertTrue(e.getMessage().contains("no shipping address"));
        }

        @Test
        @DisplayName("a route that answers false gets an addressless order through")
        void hookCanWaiveTheAddress() {
            FulfilmentProcess route = new RecordingRoute() {
                @Override
                protected boolean requiresShippingAddress() {
                    return false;
                }
            };
            Order noAddress = Order.addressless("A-6", "grace@example.com",
                    List.of(new OrderLine("E-777", "E-book", Money.pounds(9.99), 1)));
            assertEquals(6, route.fulfil(noAddress).stepNames().size());
        }

        @Test
        @DisplayName("waiving the address does not waive the rest of validation")
        void hookOnlyAnswersOneQuestion() {
            FulfilmentProcess route = new RecordingRoute() {
                @Override
                protected boolean requiresShippingAddress() {
                    return false;
                }
            };
            Order empty = Order.addressless("A-7", "grace@example.com", List.of());
            assertThrows(FulfilmentException.class, () -> route.fulfil(empty));
        }

        @Test
        @DisplayName("afterFulfilment does nothing unless a route overrides it")
        void afterFulfilmentIsEmptyByDefault() {
            FulfilmentProcess plain = new FulfilmentProcess() {
                @Override
                protected String routeName() {
                    return "plain";
                }

                @Override
                protected void reserveStock(Order o, FulfilmentReport r) {
                    r.step("reserve", "-");
                }

                @Override
                protected void charge(Order o, FulfilmentReport r) {
                    r.step("charge", "-");
                }

                @Override
                protected void dispatch(Order o, FulfilmentReport r) {
                    r.step("dispatch", "-");
                }
            };
            assertTrue(plain.fulfil(order()).notes().isEmpty());
        }

        @Test
        @DisplayName("a note from afterFulfilment does not become a seventh step")
        void notesAreNotSteps() {
            FulfilmentProcess route = new RecordingRoute() {
                @Override
                protected void afterFulfilment(Order o, FulfilmentReport r) {
                    r.note("posted to the ledger");
                }
            };
            FulfilmentReport report = route.fulfil(order());
            assertEquals(6, report.stepNames().size());
            assertEquals(List.of("posted to the ledger"), report.notes());
        }
    }

    @Nested
    @DisplayName("the defaults")
    class Defaults {

        @Test
        @DisplayName("a route that overrides nothing optional still packs and notifies")
        void defaultsFillThemselvesIn() {
            FulfilmentReport report = new RecordingRoute().fulfil(order());
            assertEquals("2 item(s) boxed and labelled",
                    report.steps().get(3).detail());
            assertEquals(List.of("grace@example.com: Order A-1 is on its way. Tracking: REF-A-1"),
                    report.notifications());
        }

        @Test
        @DisplayName("the default notification quotes what dispatch produced")
        void notificationSeesTheDispatchReference() {
            FulfilmentReport report = new RecordingRoute().fulfil(order());
            assertTrue(report.notifications().get(0).contains(report.dispatchReference()));
        }

        @Test
        @DisplayName("a route can replace pack without touching anything else")
        void packCanBeReplaced() {
            FulfilmentProcess route = new RecordingRoute() {
                @Override
                protected void pack(Order o, FulfilmentReport r) {
                    r.step("pack", "nothing to pack");
                }
            };
            FulfilmentReport report = route.fulfil(order());
            assertEquals("nothing to pack", report.steps().get(3).detail());
            assertEquals(List.of("validate", "reserve", "charge", "pack", "dispatch", "notify"),
                    report.stepNames());
        }
    }
}
