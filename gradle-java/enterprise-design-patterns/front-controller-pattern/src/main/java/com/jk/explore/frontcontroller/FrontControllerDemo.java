package com.jk.explore.frontcontroller;

import com.jk.explore.frontcontroller.naive.NaiveHandlers;

public class FrontControllerDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static String show(Response r) {
        return r.status() + " " + r.body();
    }

    private static void one() {
        System.out.println("ONE. Every handler looks after itself.");
        Journal journal = new Journal();
        NaiveHandlers naive = new NaiveHandlers(journal);
        System.out.println("  /orders with no sign-in: " + show(naive.orders(Request.get("/orders", null))));
        System.out.println("  /account with no sign-in: " + show(naive.account(Request.get("/account", null))));
        System.out.println("  requests logged: " + journal.lines().size() + " of 2. the orders handler has no login check and no log line, and the account handler logs only what it accepts.");
    }

    private static void two() {
        System.out.println("TWO. One entry point.");
        Journal journal = new Journal();
        FrontController front = FrontController.forTheStore(journal);
        System.out.println("  /orders with no sign-in: " + show(front.handle(Request.get("/orders", null))));
        System.out.println("  /orders signed in:       " + show(front.handle(Request.get("/orders", "t-ada"))));
        System.out.println("  /products, public:       " + show(front.handle(Request.get("/products", null))));
        System.out.println("  the login check is written once. no handler can forget it, because no handler has it.");
    }

    private static void three() {
        System.out.println("THREE. Routes in one table.");
        FrontController front = FrontController.forTheStore(new Journal());
        System.out.println("  /nowhere:        " + show(front.handle(Request.get("/nowhere", "t-ada"))));
        System.out.println("  POST /products:  " + show(front.handle(new Request("POST", "/products", "t-ada"))));
        System.out.println("  every unknown page and wrong method is answered the same way, in one place.");
    }

    private static void four() {
        System.out.println("FOUR. Everything is logged, even what is refused.");
        Journal journal = new Journal();
        FrontController front = FrontController.forTheStore(journal);
        front.handle(Request.get("/orders", null));
        front.handle(Request.get("/orders", "t-ada"));
        front.handle(Request.get("/nowhere", "t-ada"));
        journal.lines().forEach(l -> System.out.println("  " + l));
        System.out.println("  the refused request and the missing page are in the log. the naive handlers logged neither.");
    }

    private static void five() {
        System.out.println("FIVE. Failures are handled once.");
        Journal journal = new Journal();
        FrontController front = FrontController.forTheStore(journal);
        Response r = front.handle(Request.get("/broken", "t-ada"));
        System.out.println("  a handler throws. the customer sees: " + show(r) + ".");
        System.out.println("  the log has the detail: " + journal.lines().get(0) + ".");
        System.out.println("  the message with the password stayed in the log, and never reached the customer.");
    }

    private static void six() {
        System.out.println("SIX. The bill: one door.");
        Journal journal = new Journal();
        FrontController front = new FrontController(journal)
                .filter(Filters.buggy())
                .route("GET", "/products", Handlers.products())
                .route("GET", "/orders", Handlers.orders())
                .route("GET", "/account", Handlers.account());
        System.out.println("  one filter with a bug in it. /products: " + show(front.handle(Request.get("/products", null)))
                + ", /orders: " + show(front.handle(Request.get("/orders", "t-ada")))
                + ", /account: " + show(front.handle(Request.get("/account", "t-ada"))) + ".");
        System.out.println("  every page is down at once. the front controller is the one place everything depends on.");
    }
}
