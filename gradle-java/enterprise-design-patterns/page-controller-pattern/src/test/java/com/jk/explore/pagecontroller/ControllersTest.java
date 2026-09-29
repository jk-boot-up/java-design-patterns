package com.jk.explore.pagecontroller;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ControllersTest {

    private HttpServer server;
    private int port;

    @BeforeEach
    void start() throws IOException {
        server = PageControllerDemo.start();
        server.createContext("/product", new Controllers.ProductController());
        server.createContext("/basket", new Controllers.BasketController());
        server.start();
        port = server.getAddress().getPort();
    }

    @AfterEach
    void stop() {
        server.stop(0);
    }

    @Test
    void productPage() {
        assertEquals("200 mug, £8.00", Web.get(port, "/product?sku=MUG-1", false));
    }

    @Test
    void unknownProductIs404() {
        assertEquals("404 no product X", Web.get(port, "/product?sku=X", false));
    }

    @Test
    void basketNeedsLogin() {
        assertEquals("401 please log in", Web.get(port, "/basket?add=MUG-1", false));
    }

    @Test
    void basketDefaultsToOne() {
        assertEquals("200 basket: 1 x MUG-1", Web.get(port, "/basket?add=MUG-1", true));
    }

    @Test
    void badQuantityIs400() {
        assertEquals("400 quantity must be a number", Web.get(port, "/basket?add=MUG-1&qty=x", true));
    }
}
