package com.jk.explore.factorymethod;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DeliveryServiceTest {

    private static final Order ORDER = new Order("ORD-2001", "CUST-001", "Edinburgh", 2.5);

    private final PrintStream originalOut = System.out;
    private ByteArrayOutputStream captured;

    @BeforeEach
    void captureOutput() {
        captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreOutput() {
        System.setOut(originalOut);
    }

    static Stream<DeliveryService> allServices() {
        return Stream.of(new StandardDelivery(), new ExpressDelivery(),
                new SameDayDelivery(), new InternationalDelivery());
    }

    @Test
    @DisplayName("each subclass creates its own courier")
    void eachSubclassCreatesItsOwnCourier() {
        assertAll(
                () -> assertInstanceOf(PostalCourier.class, new StandardDelivery().createCourier()),
                () -> assertInstanceOf(AirCourier.class, new ExpressDelivery().createCourier()),
                () -> assertInstanceOf(BikeCourier.class, new SameDayDelivery().createCourier()),
                () -> assertInstanceOf(GlobalCourier.class,
                        new InternationalDelivery().createCourier()));
    }

    @ParameterizedTest
    @MethodSource("allServices")
    @DisplayName("every tier ships successfully through the shared workflow")
    void everyTierShips(DeliveryService service) {
        Shipment shipment = service.ship(ORDER);

        assertNotNull(shipment.trackingId());
        assertEquals(service.createCourier().name(), shipment.carrier());
        assertTrue(shipment.cost() > 0, "cost should be positive");
        assertTrue(shipment.etaDays() >= 0, "eta should not be negative");
    }

    @Test
    @DisplayName("the same order routes to a different carrier per tier")
    void sameOrderDifferentCarrier() {
        assertAll(
                () -> assertEquals("Royal Post", new StandardDelivery().ship(ORDER).carrier()),
                () -> assertEquals("SkyLink Air", new ExpressDelivery().ship(ORDER).carrier()),
                () -> assertEquals("CityRide Bikes", new SameDayDelivery().ship(ORDER).carrier()),
                () -> assertEquals("TransWorld Freight",
                        new InternationalDelivery().ship(ORDER).carrier()));
    }

    @Test
    @DisplayName("same day arrives today, standard does not")
    void tiersDifferInSpeed() {
        assertEquals(0, new SameDayDelivery().ship(ORDER).etaDays());
        assertEquals(5, new StandardDelivery().ship(ORDER).etaDays());
    }

    @Test
    @DisplayName("the factory method returns a fresh courier each call")
    void freshCourierEachCall() {
        StandardDelivery service = new StandardDelivery();

        assertNotSame(service.createCourier(), service.createCourier());
    }

    @Test
    @DisplayName("the shared workflow runs around the courier, in order")
    void workflowWrapsTheCourier() {
        new ExpressDelivery().ship(ORDER);

        String out = captured.toString();
        int prepared = out.indexOf("Express: preparing");
        int dispatched = out.indexOf("SkyLink Air: booking");
        int booked = out.indexOf("Express: booked");

        assertTrue(prepared >= 0 && dispatched >= 0 && booked >= 0, out);
        assertTrue(prepared < dispatched, "the service prepares before the courier runs");
        assertTrue(dispatched < booked, "the service confirms after the courier runs");
    }

    @Test
    @DisplayName("the shared guard rejects a weightless order for every tier")
    void guardAppliesToEveryTier() {
        Order weightless = new Order("ORD-2002", "CUST-001", "Edinburgh", 0);

        allServices().forEach(service ->
                assertThrows(IllegalArgumentException.class, () -> service.ship(weightless)));
    }

    @Test
    @DisplayName("a brand new tier plugs in without touching existing code")
    void newTierNeedsNoExistingChange() {
        DeliveryService droneDelivery = new DeliveryService() {
            @Override
            protected Courier createCourier() {
                return new Courier() {
                    @Override
                    public String name() {
                        return "SkyDrop Drones";
                    }

                    @Override
                    public Shipment dispatch(Order order) {
                        return new Shipment("SD-TEST", name(), 0, 15.0);
                    }
                };
            }

            @Override
            public String tier() {
                return "Drone";
            }
        };

        Shipment shipment = droneDelivery.ship(ORDER);

        assertEquals("SkyDrop Drones", shipment.carrier());
        assertTrue(captured.toString().contains("Drone: booked SD-TEST"));
    }
}
