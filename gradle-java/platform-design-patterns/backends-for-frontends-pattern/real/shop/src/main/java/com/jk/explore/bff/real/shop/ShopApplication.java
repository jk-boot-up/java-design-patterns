package com.jk.explore.bff.real.shop;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * The shop as it was before anybody wrote a backend for a frontend.
 *
 * <p>Five services and one shared endpoint in front of them, in a single process on
 * port 8082. Collapsing five services into one process is a simplification and the
 * README says so out loud; what matters to this pattern is that they are five separate
 * <em>calls</em>, each with its own path and its own shape, and that a client which
 * wants all five has to make all five.
 */
@SpringBootApplication
public class ShopApplication {

    public static void main(String[] args) {
        SpringApplication.run(ShopApplication.class, args);
    }
}
