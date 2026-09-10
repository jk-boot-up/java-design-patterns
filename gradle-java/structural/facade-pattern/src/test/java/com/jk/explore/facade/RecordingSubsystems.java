package com.jk.explore.facade;

import java.util.ArrayList;
import java.util.List;

/**
 * Test doubles for the four subsystems.
 *
 * <p>Each one subclasses the real service, writes what it was asked into a
 * shared log, and returns a predictable value instead of a random identifier.
 * That gives the tests two things the real services cannot: the exact order the
 * facade called them in, and the arguments it passed, so a step that is skipped
 * or handed the wrong value fails a test rather than merely looking odd in the
 * console output.
 */
final class RecordingSubsystems {

    /** Every call, in the order it happened, across all four subsystems. */
    final List<String> calls = new ArrayList<>();

    final Inventory inventory;
    final Payment payment = new Payment();
    final Shipping shipping = new Shipping();
    final Notifications notifications = new Notifications();

    RecordingSubsystems() {
        this(true);
    }

    RecordingSubsystems(boolean stockAvailable) {
        this.inventory = new Inventory(stockAvailable);
    }

    OrderFacade facade() {
        return new OrderFacade(inventory, payment, shipping, notifications);
    }

    final class Inventory extends InventoryService {
        private final boolean stockAvailable;

        Inventory(boolean stockAvailable) {
            this.stockAvailable = stockAvailable;
        }

        @Override
        public boolean reserveStock(String productId, int quantity) {
            calls.add("reserveStock:" + productId + ":" + quantity);
            return stockAvailable;
        }
    }

    final class Payment extends PaymentService {
        @Override
        public String charge(String customerId, double amount) {
            calls.add("charge:" + customerId + ":" + amount);
            return "PMT-TEST";
        }
    }

    final class Shipping extends ShippingService {
        @Override
        public String scheduleShipment(String orderId, String address) {
            calls.add("scheduleShipment:" + orderId + ":" + address);
            return "TRK-TEST";
        }
    }

    final class Notifications extends NotificationService {
        @Override
        public void sendOrderConfirmation(String customerId, String orderId, String trackingId) {
            calls.add("sendOrderConfirmation:" + customerId + ":" + orderId + ":" + trackingId);
        }
    }
}
