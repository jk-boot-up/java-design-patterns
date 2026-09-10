package com.jk.explore.facade;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Tests for the requirement that is easiest to break by accident: the four
 * subsystems stay usable on their own. A facade is a convenience, not a wall,
 * and the moment a service is locked down to force callers through the facade
 * the project is teaching the wrong lesson.
 */
class SubsystemsTest {

    @Test
    void everySubsystemCanBeUsedWithoutTheFacade() {
        assertTrue(new InventoryService().reserveStock("SKU-1234", 2));
        assertTrue(new PaymentService().charge("CUST-001", 49.98).startsWith("PMT-"));
        assertTrue(new ShippingService().scheduleShipment("ORD-1", "221B Baker Street").startsWith("TRK-"));

        // Returns nothing, so the assertion is simply that a caller outside the
        // facade is allowed to make the call at all.
        new NotificationService().sendOrderConfirmation("CUST-001", "ORD-1", "TRK-1");
    }

    @Test
    void everySubsystemClassAndItsMethodsArePublic() {
        for (Class<?> service : new Class<?>[] {InventoryService.class, PaymentService.class,
                                                ShippingService.class, NotificationService.class}) {
            assertTrue(Modifier.isPublic(service.getModifiers()), service.getSimpleName() + " should be public");
            for (Method method : service.getDeclaredMethods()) {
                if (method.isSynthetic()) {
                    continue;
                }
                assertTrue(Modifier.isPublic(method.getModifiers()),
                        service.getSimpleName() + "." + method.getName() + " should stay public");
            }
        }
    }

    @Test
    void theFacadeExposesOneMethodAndOnePublicConstructor() {
        long publicMethods = java.util.Arrays.stream(OrderFacade.class.getDeclaredMethods())
                .filter(method -> !method.isSynthetic())
                .filter(method -> Modifier.isPublic(method.getModifiers()))
                .count();

        assertEquals(1, publicMethods, "placeOrder is the whole public surface of the facade");
        assertEquals(1, java.util.Arrays.stream(OrderFacade.class.getDeclaredConstructors())
                .filter(constructor -> Modifier.isPublic(constructor.getModifiers()))
                .count(), "the four-service constructor is package-private on purpose");
    }

    @Test
    void identifiersAreUniquePerCall() {
        PaymentService payments = new PaymentService();
        ShippingService shipping = new ShippingService();

        assertNotEquals(payments.charge("CUST-001", 1.0), payments.charge("CUST-001", 1.0));
        assertNotEquals(shipping.scheduleShipment("ORD-1", "London"),
                shipping.scheduleShipment("ORD-1", "London"));
    }

    @Test
    void theValueObjectsCarryTheRequestAndTheConfirmation() {
        OrderRequest request = new OrderRequest("CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

        assertEquals("CUST-001", request.customerId());
        assertEquals("SKU-1234", request.productId());
        assertEquals(2, request.quantity());
        assertEquals(49.98, request.amount());
        assertEquals("221B Baker Street, London", request.shippingAddress());

        OrderConfirmation confirmation = new OrderConfirmation("ORD-1", "PMT-1", "TRK-1");
        assertEquals(new OrderConfirmation("ORD-1", "PMT-1", "TRK-1"), confirmation,
                "records give the confirmation value equality for free");
    }

    @Test
    void theDemoRuns() {
        // The output is quoted in the top-level README, so the demo failing is a
        // documentation bug as much as a code one.
        FacadeDemo.main(new String[0]);
    }
}
