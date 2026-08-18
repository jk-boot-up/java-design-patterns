package com.jk.explore.factorymethod;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

class CourierTest {

    private static final Order ORDER = new Order("ORD-2001", "CUST-001", "Edinburgh", 2.0);

    private final PrintStream originalOut = System.out;

    @BeforeEach
    void muteOutput() {
        System.setOut(new PrintStream(new ByteArrayOutputStream()));
    }

    @AfterEach
    void restoreOutput() {
        System.setOut(originalOut);
    }

    static Stream<Arguments> couriers() {
        return Stream.of(
                arguments(new PostalCourier(), "Royal Post", "RP-", 5, 4.99),
                arguments(new AirCourier(), "SkyLink Air", "SL-", 2, 14.90),
                arguments(new BikeCourier(), "CityRide Bikes", "CR-", 0, 8.60),
                arguments(new GlobalCourier(), "TransWorld Freight", "TW-", 9, 28.20));
    }

    @ParameterizedTest(name = "{1}")
    @MethodSource("couriers")
    @DisplayName("each courier stamps its own name, prefix, ETA and price")
    void courierProducesItsOwnShipment(Courier courier, String name, String prefix,
                                       int etaDays, double cost) {
        Shipment shipment = courier.dispatch(ORDER);

        assertEquals(name, shipment.carrier());
        assertTrue(shipment.trackingId().startsWith(prefix),
                "expected a tracking id starting with " + prefix + " but got " + shipment.trackingId());
        assertEquals(etaDays, shipment.etaDays());
        assertEquals(cost, shipment.cost(), 0.0001);
    }

    @Test
    @DisplayName("heavier orders cost more on the same courier")
    void costGrowsWithWeight() {
        Courier courier = new AirCourier();

        double light = courier.dispatch(new Order("ORD-1", "CUST-1", "Leeds", 1.0)).cost();
        double heavy = courier.dispatch(new Order("ORD-2", "CUST-1", "Leeds", 9.0)).cost();

        assertTrue(heavy > light, "9kg should cost more than 1kg");
    }

    @Test
    @DisplayName("every dispatch gets its own tracking id")
    void trackingIdsAreUnique() {
        Courier courier = new PostalCourier();
        Set<String> ids = new HashSet<>();

        for (int i = 0; i < 50; i++) {
            ids.add(courier.dispatch(ORDER).trackingId());
        }

        assertEquals(50, ids.size());
    }
}
