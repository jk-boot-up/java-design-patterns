package com.jk.explore.locatorconsul.pattern;

import com.jk.explore.locatorconsul.consul.Address;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * <strong>The checkout asks for each remote service by name, when it needs it.</strong>
 * Its constructor takes nothing, so {@code new LocatorCheckout()} always compiles.
 * The service names are strings: a typo compiles too.
 */
public class LocatorCheckout {

    private final HttpClient http = HttpClient.newHttpClient();

    public String place(long pricePence) {
        long discounted = pricePence * 90 / 100;
        String receipt = call(Discovery.find("payment-gateway"), "/charge?pence=" + discounted);
        call(Discovery.find("notifier"), "/send?message=paid+" + discounted);
        return receipt;
    }

    public static String call(HttpClient http, Address address, String path) {
        try {
            return http.send(HttpRequest.newBuilder(URI.create("http://" + address.hostAndPort() + path)).build(),
                    HttpResponse.BodyHandlers.ofString()).body();
        } catch (IOException e) {
            throw new IllegalStateException("could not reach " + address.hostAndPort() + ": " + e.getClass().getSimpleName(), e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    private String call(Address address, String path) {
        return call(http, address, path);
    }
}
