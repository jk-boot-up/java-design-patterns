package com.jk.explore.hedgedgrpc;

import io.grpc.CallOptions;
import io.grpc.ManagedChannel;
import io.grpc.stub.ClientCalls;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * The five acts, with a real gRPC server and gRPC's own hedging policy.
 */
public final class GrpcHedgedRequestsDemo {

    static final int REQUESTS = 100;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (PriceServer server = new PriceServer()) {

            out.add("ONE. One call per price, and a slow tail.");
            ManagedChannel plain = Channels.plain(server.port());
            int slow = lookups(plain, REQUESTS);
            out.add("  " + REQUESTS + " price lookups: " + slow + " took about a second; the rest about 20 ms");
            out.add("  so the 99th percentile is a whole second, and so is that product page");
            close(plain);

            out.add("");
            out.add("TWO. gRPC's hedging policy: a second attempt after 50 ms.");
            server.reset();
            ManagedChannel hedged = Channels.hedged(server.port(), "shop.Prices", "0.05s");
            slow = lookups(hedged, REQUESTS);
            int extra = server.priceCalls() - REQUESTS;
            out.add("  " + REQUESTS + " lookups: " + slow + " took over 0.2 s; extra calls sent by gRPC: " + extra);
            out.add("  no hedging code in the shop: one policy in the channel's service config");

            out.add("");
            out.add("THREE. The loser is cancelled.");
            final int losers = extra;
            waitFor(() -> server.cancelled() >= losers);   // the losing attempts finish their pause, then see the cancel
            out.add("  slow attempts that noticed they were cancelled, and never replied: " + server.cancelled());
            close(hedged);

            out.add("");
            out.add("FOUR. Hedge at once: hedgingDelay 0.");
            server.reset();
            ManagedChannel eager = Channels.hedged(server.port(), "shop.Prices", "0s");
            lookups(eager, REQUESTS);
            out.add("  " + REQUESTS + " lookups sent " + server.priceCalls() + " calls: twice the load on the price service");
            close(eager);

            out.add("");
            out.add("FIVE. The bill: never hedge what is not safe to repeat.");
            server.reset();
            ManagedChannel wrong = Channels.hedged(server.port(), "shop.Orders", "0s");
            String reply = ClientCalls.blockingUnaryCall(wrong, Shop.PLACE_ORDER, CallOptions.DEFAULT, "ORD-1");
            waitFor(() -> server.ordersPlaced() >= 2);
            out.add("  PlaceOrder hedged by mistake: the customer saw \"" + reply + "\"; the server placed "
                    + server.ordersPlaced() + " orders");
            out.add("  hedge only reads; and cap hedges with gRPC's retryThrottling, so an overloaded service is not sent more");
            close(wrong);
        }
        return out;
    }

    /** Looks up {@code n} prices one after another; returns how many took over 0.2 s. */
    private static int lookups(ManagedChannel channel, int n) {
        int slow = 0;
        for (int i = 1; i <= n; i++) {
            long start = System.nanoTime();
            ClientCalls.blockingUnaryCall(channel, Shop.PRICE, CallOptions.DEFAULT, "MUG-" + i);
            if ((System.nanoTime() - start) / 1_000_000 > 200) {
                slow++;
            }
        }
        return slow;
    }

    /** Waits for a real condition, checking often, for at most five seconds. Never a fixed sleep. */
    private static void waitFor(java.util.function.BooleanSupplier condition) throws InterruptedException {
        long deadline = System.currentTimeMillis() + 5_000;
        while (!condition.getAsBoolean() && System.currentTimeMillis() < deadline) {
            TimeUnit.MILLISECONDS.sleep(10);
        }
    }

    private static void close(ManagedChannel channel) throws InterruptedException {
        channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
    }

    private GrpcHedgedRequestsDemo() {
    }
}
