package com.jk.explore.remotefacade;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: many small remote calls, one facade call, a change in one call, cheap calls inside, and the bill.
 */
public final class RemoteFacadeDemo {

    public static void main(String[] args) throws IOException {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static HttpServer serve(Order order) throws IOException {
        HttpServer s = HttpServer.create(new InetSocketAddress("localhost", 0), 0);
        FineGrainedApi.register(s, order);
        OrderFacade.register(s, order);
        s.start();
        return s;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws IOException {
        List<String> out = new ArrayList<>();
        String newAddress = Http.encode("12 High Street, York");

        out.add("ONE. The phone app asks for each fact separately.");
        HttpServer s1 = serve(new Order());
        Http.Phone phone = new Http.Phone(s1.getAddress().getPort());
        for (String fact : new String[] {"customer", "items", "total", "address", "slot"}) {
            out.add("  GET /order/" + fact + " -> " + phone.get("/order/" + fact));
        }
        out.add("  order screen: " + phone.trips() + " round trips, " + phone.waitedMs() + " ms on a mobile network");

        out.add("");
        out.add("TWO. A remote facade: the whole screen in one call.");
        Http.Phone phone2 = new Http.Phone(s1.getAddress().getPort());
        out.add("  GET /order-summary -> " + phone2.get("/order-summary"));
        out.add("  order screen: " + phone2.trips() + " round trip, " + phone2.waitedMs() + " ms");
        s1.stop(0);

        out.add("");
        out.add("THREE. A change in one call: all or nothing.");
        Order o1 = new Order();
        HttpServer s2 = serve(o1);
        Http.Phone fine = new Http.Phone(s2.getAddress().getPort());
        out.add("  small calls: " + fine.get("/order/change-address?to=" + newAddress) + ", then "
                + fine.get("/order/book-slot?slot=" + Http.encode("Sun 9-12")));
        out.add("  the order now: new address, old slot: " + o1.address() + ", " + o1.slot());
        s2.stop(0);
        Order o2 = new Order();
        HttpServer s3 = serve(o2);
        Http.Phone coarse = new Http.Phone(s3.getAddress().getPort());
        out.add("  facade: " + coarse.get("/order-change-delivery?to=" + newAddress + "&slot=" + Http.encode("Sun 9-12")));
        out.add("  the order is unchanged: " + o2.address() + ", " + o2.slot());
        out.add("  facade, valid slot: " + coarse.get("/order-change-delivery?to=" + newAddress + "&slot=" + Http.encode("Tue 9-12")));
        out.add("  the order now: " + o2.address() + ", " + o2.slot());
        s3.stop(0);

        out.add("");
        out.add("FOUR. Inside, the order stays fine-grained.");
        Order o3 = new Order();
        long start = System.nanoTime();
        OrderFacade.summary(o3);
        long micros = (System.nanoTime() - start) / 1000;
        out.add("  the facade made 6 small calls on the order, in-process: " + (micros < 5000 ? "under 5 ms" : micros + " µs"));
        out.add("  the business rules (valid slots) stay on the Order; the facade only packs and unpacks");

        out.add("");
        out.add("FIVE. The bill: sometimes too much, and one more layer.");
        HttpServer s4 = serve(new Order());
        Http.Phone slot = new Http.Phone(s4.getAddress().getPort());
        slot.get("/order/slot");
        Http.Phone whole = new Http.Phone(s4.getAddress().getPort());
        whole.get("/order-summary");
        out.add("  a widget that shows only the slot: " + slot.bytes() + " bytes with the small call, "
                + whole.bytes() + " with the summary");
        out.add("  and each new screen may want its own facade method");
        s4.stop(0);
        return out;
    }

    static String pounds(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }

    private RemoteFacadeDemo() {
    }
}
