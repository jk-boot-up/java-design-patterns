package com.jk.explore.factorymethod;

import java.util.List;

public class FactoryMethodDemo {

    public static void main(String[] args) {
        Order order = new Order("ORD-2001", "CUST-001", "Edinburgh", 2.5);

        // The client holds creators, not couriers. Nothing here names a
        // courier class, and there is no switch anywhere in the project.
        List<DeliveryService> services = List.of(
                new StandardDelivery(),
                new ExpressDelivery(),
                new SameDayDelivery(),
                new InternationalDelivery());

        for (DeliveryService service : services) {
            Shipment shipment = service.ship(order);

            System.out.println("Shipment: " + shipment);
            System.out.println();
        }
    }
}
