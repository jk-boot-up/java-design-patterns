package com.jk.explore.wiretap;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: logging typed into the services, a wire tap, taps on and off, a second tap, and the bill.
 */
public final class WireTapDemo {

    static final List<PaymentMessage> TRAFFIC = List.of(
            new PaymentMessage("CHARGE", "ORD-1", 6344, "4929123412341234"),
            new PaymentMessage("CHARGE", "ORD-2", 1999, "4929555566667777"),
            new PaymentMessage("REFUND", "ORD-1", 3000, "4929123412341234"),
            new PaymentMessage("CHARGE", "ORD-3", 499, "4929000011112222"));

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. Logging typed into the payment service by hand.");
        List<String> handLog = new ArrayList<>();
        Channel c1 = new Channel(new PaymentService(handLog));
        TRAFFIC.forEach(c1::send);
        out.add("  messages sent: " + TRAFFIC.size() + "; messages in the log: " + handLog.size());
        out.add("  the refund path was never given logging, and the log shows full card numbers:");
        out.add("  " + handLog.get(0));

        out.add("");
        out.add("TWO. A wire tap on the channel.");
        PaymentService payment = new PaymentService(null);
        Channel c2 = new Channel(payment);
        WireTaps.AuditLog audit = new WireTaps.AuditLog(true);
        c2.attach(audit);
        TRAFFIC.forEach(c2::send);
        audit.lines().forEach(l -> out.add("  audit: " + l));
        out.add("  " + audit.lines().size() + " of " + TRAFFIC.size() + " copied; payment handled " + payment.handled());
        out.add("  neither checkout nor the payment service was changed");

        out.add("");
        out.add("THREE. Attach while investigating, detach afterwards.");
        c2.detach(audit);
        c2.send(new PaymentMessage("CHARGE", "ORD-4", 1200, "4929999988887777"));
        out.add("  tap detached; ORD-4 flows as normal; audit still has " + audit.lines().size() + " lines");

        out.add("");
        out.add("FOUR. A second tap, for a sales dashboard.");
        WireTaps.SalesMeter meter = new WireTaps.SalesMeter();
        Channel c4 = new Channel(new PaymentService(null));
        c4.attach(meter);
        TRAFFIC.forEach(c4::send);
        out.add("  net takings seen by the meter: " + String.format("£%d.%02d", meter.net() / 100, meter.net() % 100));

        out.add("");
        out.add("FIVE. The bill: a slow tap slows the real traffic.");
        Channel c5 = new Channel(new PaymentService(null));
        c5.attach(WireTaps.slow(new WireTaps.AuditLog(true), 100));
        long t0 = System.nanoTime();
        TRAFFIC.forEach(c5::send);
        long syncMs = (System.nanoTime() - t0) / 1_000_000;
        out.add("  a tap that takes 100 ms per copy: 4 payments took " + (syncMs >= 400 ? "over 0.4 s" : syncMs + " ms"));
        Channel c6 = new Channel(new PaymentService(null));
        try (WireTaps.Async async = new WireTaps.Async(WireTaps.slow(new WireTaps.AuditLog(true), 100))) {
            c6.attach(async);
            long t1 = System.nanoTime();
            TRAFFIC.forEach(c6::send);
            long asyncMs = (System.nanoTime() - t1) / 1_000_000;
            out.add("  the same tap on its own thread: " + (asyncMs < 50 ? "under 0.05 s" : asyncMs + " ms"));
        }
        out.add("  and a tap sees everything: mask card numbers before anything is copied");
        return out;
    }

    private WireTapDemo() {
    }
}
