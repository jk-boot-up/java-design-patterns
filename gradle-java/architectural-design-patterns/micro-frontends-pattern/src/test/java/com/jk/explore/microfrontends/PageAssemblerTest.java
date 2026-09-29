package com.jk.explore.microfrontends;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class PageAssemblerTest {

    @Test
    void assemblesFragmentsInSlotOrder() throws Exception {
        try (TeamApp a = new TeamApp("a", () -> "A"); TeamApp b = new TeamApp("b", () -> "B")) {
            assertEquals("[first] A | [second] B", new PageAssembler().slot("first", a.url()).slot("second", b.url()).render());
        }
    }

    @Test
    void failingFragmentGetsAFallback() throws Exception {
        try (TeamApp a = new TeamApp("a", () -> "A")) {
            a.release(() -> {
                throw new IllegalStateException();
            });
            assertEquals("[x] (x unavailable)", new PageAssembler().slot("x", a.url()).render());
        }
    }

    @Test
    void slowFragmentGetsAFallback() throws Exception {
        try (TeamApp a = new TeamApp("a", () -> "A")) {
            a.slowDown(1000);
            assertEquals("[x] (x unavailable)", new PageAssembler().slot("x", a.url()).render());
        }
    }

    @Test
    void oneFrontEndFailsAsAWhole() {
        OneFrontEnd f = new OneFrontEnd();
        f.breakRecommendations();
        assertThrows(IllegalStateException.class, () -> f.productPage("K"));
    }
}
