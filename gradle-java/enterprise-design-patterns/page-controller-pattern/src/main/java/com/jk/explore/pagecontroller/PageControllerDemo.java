package com.jk.explore.pagecontroller;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: one handler for every page, a controller per page, errors that stay on their page, a new page, and the bill.
 */
public final class PageControllerDemo {

    public static void main(String[] args) throws IOException {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static HttpServer start() throws IOException {
        return HttpServer.create(new InetSocketAddress("localhost", 0), 0);
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws IOException {
        List<String> out = new ArrayList<>();

        out.add("ONE. One handler for every page.");
        HttpServer old = start();
        old.createContext("/", new OneHandler());
        old.start();
        int p1 = old.getAddress().getPort();
        out.add("  GET /basket?add=MUG-1&qty=2    -> " + Web.get(p1, "/basket?add=MUG-1&qty=2", true));
        out.add("  GET /product?sku=KETTLE-1      -> " + Web.get(p1, "/product?sku=KETTLE-1", true));
        out.add("  quantity parsing was added at the top for the basket; it now runs for every page");
        old.stop(0);

        out.add("");
        out.add("TWO. A page controller for each page.");
        HttpServer server = start();
        server.createContext("/product", new Controllers.ProductController());
        server.createContext("/basket", new Controllers.BasketController());
        server.createContext("/checkout", new Controllers.CheckoutController());
        server.start();
        int port = server.getAddress().getPort();
        out.add("  GET /product?sku=KETTLE-1      -> " + Web.get(port, "/product?sku=KETTLE-1", true));
        out.add("  GET /basket?add=MUG-1&qty=2    -> " + Web.get(port, "/basket?add=MUG-1&qty=2", true));

        out.add("");
        out.add("THREE. Each page handles its own input and its own errors.");
        out.add("  GET /product?sku=SOFA-9        -> " + Web.get(port, "/product?sku=SOFA-9", true));
        out.add("  GET /basket?add=MUG-1&qty=two  -> " + Web.get(port, "/basket?add=MUG-1&qty=two", true));
        out.add("  GET /product?sku=MUG-1         -> " + Web.get(port, "/product?sku=MUG-1", true));

        out.add("");
        out.add("FOUR. A new page is a new class and one line.");
        server.createContext("/reviews", new Controllers.ReviewsController());
        out.add("  GET /reviews?sku=KETTLE-1      -> " + Web.get(port, "/reviews?sku=KETTLE-1", true));
        out.add("  no other controller was opened");

        out.add("");
        out.add("FIVE. The bill: shared checks are repeated on every page.");
        out.add("  GET /basket, not logged in      -> " + Web.get(port, "/basket?add=MUG-1", false));
        out.add("  GET /checkout, not logged in    -> " + Web.get(port, "/checkout", false));
        out.add("  checkout's author forgot the login check that basket repeats");
        server.stop(0);
        return out;
    }

    private PageControllerDemo() {
    }
}
