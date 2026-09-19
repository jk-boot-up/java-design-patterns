package com.jk.explore.frontcontroller;

/** The store's three handlers, each written as if everything around it were somebody else's job. */
public final class Handlers {

    private Handlers() {
    }

    public static Handler products() {
        return r -> Response.ok("the catalogue: mug, tea, machine");
    }

    public static Handler orders() {
        return r -> Response.ok("ada's orders: ORD-1, ORD-2");
    }

    public static Handler account() {
        return r -> Response.ok("ada's account: ada@example.com");
    }

    public static Handler faulty() {
        return r -> {
            throw new IllegalStateException("database password is hunter2");
        };
    }
}
