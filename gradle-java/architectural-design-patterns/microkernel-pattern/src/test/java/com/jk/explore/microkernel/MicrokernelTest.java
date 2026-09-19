package com.jk.explore.microkernel;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class MicrokernelTest {

    @Test
    void monolithIgnoresAFeatureItDoesNotHave() {
        MonolithCheckout m = new MonolithCheckout();
        assertFalse(m.supports("gift-wrap"));
        assertEquals(10000, m.total(10000, Set.of("gift-wrap")));
    }

    @Test
    void pluginsRunInOrder() {
        Kernel k = new Kernel();
        k.register(new PercentOff("d", 10));
        k.register(new Fee("f", 500));
        assertEquals(9500, k.total(10000));
    }

    @Test
    void orderChangesTheResult() {
        Kernel a = new Kernel();
        a.register(new PercentOff("d", 10));
        a.register(new Fee("f", 500));
        Kernel b = new Kernel();
        b.register(new Fee("f", 500));
        b.register(new PercentOff("d", 10));
        assertEquals(9500, a.total(10000));
        assertEquals(9450, b.total(10000));
    }

    @Test
    void registerStartsAndUnregisterStops() {
        Kernel k = new Kernel();
        Fee wrap = new Fee("wrap", 300);
        k.register(wrap);
        assertTrue(wrap.running());
        assertTrue(k.unregister("wrap"));
        assertFalse(wrap.running());
        assertFalse(k.unregister("wrap"));
        assertEquals(10000, k.total(10000));
    }

    @Test
    void aBrokenPluginDoesNotStopTheOthers() {
        Kernel k = new Kernel();
        k.register(new BrokenPlugin("x"));
        k.register(new Fee("f", 500));
        assertEquals(10500, k.total(10000));
        assertEquals(List.of("x: x lost its connection"), k.failures());
    }
}
