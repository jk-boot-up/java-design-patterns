package com.jk.explore.contentrouter;

import org.junit.jupiter.api.Test;

import java.util.List;

import static com.jk.explore.contentrouter.ContentRouterDemo.ORDERS;
import static org.junit.jupiter.api.Assertions.*;

class ContentRouterTest {

    @Test
    void eachOrderGoesToTheChannelItsContentSays() {
        Router r = ContentRouterDemo.standard();
        assertEquals("warehouse", r.send(ORDERS.get(0)));
        assertEquals("digital-delivery", r.send(ORDERS.get(1)));
        assertEquals("fraud-review", r.send(ORDERS.get(2)));
        assertEquals("manual-review", r.send(ORDERS.get(4)));
    }

    @Test
    void theFirstMatchingRuleWinsSoOrderMatters() {
        Order big = new Order("X", "gift-card", "UK", 150000);
        Router a = new Router(null).route("hv", o -> o.pence() >= 100000, "fraud").route("gc", o -> o.kind().equals("gift-card"), "digital");
        Router b = new Router(null).route("gc", o -> o.kind().equals("gift-card"), "digital").route("hv", o -> o.pence() >= 100000, "fraud");
        assertEquals("fraud", a.send(big));
        assertEquals("digital", b.send(big));
    }

    @Test
    void aFallbackCatchesWhatNoRuleCoversAndNoFallbackDropsIt() {
        Order odd = new Order("X", "subscription", "UK", 1);
        assertEquals("manual-review", ContentRouterDemo.standard().send(odd));
        Router none = new Router(null).route("p", o -> o.kind().equals("physical"), "warehouse");
        assertNull(none.send(odd));
        assertEquals(1, none.dropped());
    }

    @Test
    void aNewRuleAddsARouteWithoutChangingTheOthers() {
        Router r = ContentRouterDemo.standard();
        r.route("EU", o -> o.region().equals("EU"), "eu-vat-check");
        assertEquals(4, r.rules());
        assertEquals("eu-vat-check", r.send(new Order("X", "subscription", "EU", 1)));
        assertEquals("warehouse", r.send(new Order("Y", "physical", "EU", 1)));
    }

    @Test
    void aRenamedFieldValueMakesTheRuleMissAndFallBack() {
        Router r = new Router("manual-review").route("p", o -> o.kind().equals("physical"), "warehouse");
        assertEquals("manual-review", r.send(new Order("X", "goods", "UK", 1)));
    }

    @Test
    void everyOrderGoesToExactlyOneChannel() {
        Router r = ContentRouterDemo.standard();
        ORDERS.forEach(r::send);
        int total = r.channels().values().stream().mapToInt(List::size).sum();
        assertEquals(ORDERS.size(), total);
    }
}
