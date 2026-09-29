package com.jk.explore.broker;

import com.sun.net.httpserver.HttpServer;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: hard-coded addresses, calls through a broker, a service that moves, several instances, and the bill.
 */
public final class BrokerDemo {

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Checkout knows the stock service's address.");
        HttpServer stock = Services.stock();
        String hardCoded = Http.url(stock);
        out.add("  checkout asks " + "the stock service directly: KETTLE-1 -> " + Http.get(hardCoded + "/?sku=KETTLE-1"));
        stock.stop(0);
        HttpServer moved = Services.stock();
        out.add("  the stock service moves to a new machine");
        out.add("  checkout, still using the old address: " + Http.get(hardCoded + "/?sku=KETTLE-1"));
        moved.stop(0);

        try (Broker broker = new Broker()) {
            out.add("");
            out.add("TWO. A broker: services register by name, clients call by name.");
            HttpServer stock2 = Services.stock();
            Http.get(broker.url() + "/register?name=stock&url=" + Http.url(stock2));
            out.add("  stock service registers as \"stock\"");
            out.add("  checkout calls the broker: /call/stock?sku=KETTLE-1 -> " + Http.get(broker.url() + "/call/stock?sku=KETTLE-1"));
            out.add("  checkout knows only the broker's address");

            out.add("");
            out.add("THREE. A service moves; clients do not notice.");
            stock2.stop(0);
            HttpServer stock3 = Services.stock();
            Http.get(broker.url() + "/register?name=stock&url=" + Http.url(stock3));
            out.add("  the stock service moves, and registers its new address");
            out.add("  checkout, unchanged: /call/stock?sku=MUG-1 -> " + Http.get(broker.url() + "/call/stock?sku=MUG-1"));

            out.add("");
            out.add("FOUR. Several instances of one service.");
            HttpServer priceA = Services.price("price-a");
            HttpServer priceB = Services.price("price-b");
            broker.addInstance("price", Http.url(priceA));
            broker.addInstance("price", Http.url(priceB));
            for (int i = 1; i <= 4; i++) {
                out.add("  call " + i + ": " + Http.get(broker.url() + "/call/price?sku=KETTLE-1"));
            }
            out.add("  the broker takes turns; checkout never chose an instance");

            out.add("");
            out.add("FIVE. The bill: an extra hop, and one thing everyone needs.");
            int before = broker.forwarded();
            Http.get(broker.url() + "/call/stock?sku=KETTLE-1");
            out.add("  one call from checkout = " + (1 + broker.forwarded() - before) + " network requests (checkout -> broker -> stock)");
            String brokerUrl = broker.url();
            broker.close();
            out.add("  the broker stops: " + Http.get(brokerUrl + "/call/stock?sku=KETTLE-1") + "; every service is unreachable");
            stock3.stop(0);
            priceA.stop(0);
            priceB.stop(0);
        }
        return out;
    }

    private BrokerDemo() {
    }
}
