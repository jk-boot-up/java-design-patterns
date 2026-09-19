package com.jk.explore.frontcontroller;

import com.jk.explore.frontcontroller.naive.NaiveHandlers;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class FrontControllerTest {

    private final Journal journal = new Journal();
    private final FrontController front = FrontController.forTheStore(journal);

    @Test
    void theForgottenLoginCheckIsARealHoleInTheNaiveVersion() {
        assertEquals(200, new NaiveHandlers(new Journal()).orders(Request.get("/orders", null)).status());
        assertEquals(401, front.handle(Request.get("/orders", null)).status());
    }

    @Test
    void publicPathsNeedNoTokenAndOthersDo() {
        assertEquals(200, front.handle(Request.get("/products", null)).status());
        assertEquals(401, front.handle(Request.get("/account", null)).status());
        assertEquals(200, front.handle(Request.get("/account", "t-ada")).status());
    }

    @Test
    void unknownPathsAndWrongMethodsAreAnsweredCentrally() {
        assertEquals(404, front.handle(Request.get("/nowhere", "t-ada")).status());
        assertEquals(405, front.handle(new Request("POST", "/products", "t-ada")).status());
    }

    @Test
    void everyRequestIsLoggedIncludingRefusedOnes() {
        front.handle(Request.get("/orders", null));
        front.handle(Request.get("/nowhere", "t-ada"));
        assertEquals(List.of("GET /orders -> 401", "GET /nowhere -> 404"), journal.lines());
    }

    @Test
    void aFailureNeverLeaksItsMessageToTheCustomer() {
        Response r = front.handle(Request.get("/broken", "t-ada"));
        assertEquals(500, r.status());
        assertFalse(r.body().contains("hunter2"));
        assertTrue(journal.lines().get(0).contains("hunter2"));
    }

    @Test
    void aBuggyFilterBringsEveryRouteDown() {
        FrontController f = new FrontController(new Journal()).filter(Filters.buggy())
                .route("GET", "/a", Handlers.products()).route("GET", "/b", Handlers.orders());
        assertEquals(500, f.handle(Request.get("/a", null)).status());
        assertEquals(500, f.handle(Request.get("/b", null)).status());
    }

    @Test
    void filtersRunInTheOrderTheyWereAdded() {
        Journal j = new Journal();
        FrontController f = new FrontController(j)
                .filter((r, next) -> { j.add("first in"); Response x = next.apply(r); j.add("first out"); return x; })
                .filter((r, next) -> { j.add("second in"); Response x = next.apply(r); j.add("second out"); return x; })
                .route("GET", "/a", Handlers.products());
        f.handle(Request.get("/a", null));
        assertEquals(List.of("first in", "second in", "second out", "first out"), j.lines());
    }
}
