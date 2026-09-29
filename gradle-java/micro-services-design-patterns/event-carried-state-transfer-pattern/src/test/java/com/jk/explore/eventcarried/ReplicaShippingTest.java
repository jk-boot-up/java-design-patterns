package com.jk.explore.eventcarried;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

import org.junit.jupiter.api.Test;

class ReplicaShippingTest {

    @Test
    void unknownCustomerHasNoLabel() {
        assertNull(new ReplicaShipping(true).label("O", "nobody"));
    }

    @Test
    void newerVersionReplacesOlder() {
        ReplicaShipping s = new ReplicaShipping(true);
        s.on(new Events.AddressChanged("C", new Address("a", "x"), 1));
        s.on(new Events.AddressChanged("C", new Address("b", "y"), 2));
        assertEquals("O -> b, y", s.label("O", "C"));
    }

    @Test
    void duplicateEventIsHarmless() {
        ReplicaShipping s = new ReplicaShipping(true);
        Events.AddressChanged e = new Events.AddressChanged("C", new Address("a", "x"), 1);
        s.on(e);
        s.on(e);
        assertEquals(1, s.copies());
    }
}
