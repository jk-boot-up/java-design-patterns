package com.jk.explore.hedgedgrpc;

import io.grpc.Context;
import io.grpc.Server;
import io.grpc.ServerServiceDefinition;
import io.grpc.netty.shaded.io.grpc.netty.NettyServerBuilder;
import io.grpc.stub.ServerCalls;
import java.net.InetSocketAddress;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The price service, as a real gRPC server on a local port. Usually it answers in 20 ms, but one
 * call in 33 lands on a paused worker and takes a second, as a garbage-collection pause would.
 */
public final class PriceServer implements AutoCloseable {

    private final AtomicInteger priceCalls = new AtomicInteger();
    private final AtomicInteger cancelled = new AtomicInteger();
    private final AtomicInteger ordersPlaced = new AtomicInteger();
    private final Server server;

    public PriceServer() throws Exception {
        ServerServiceDefinition prices = ServerServiceDefinition.builder("shop.Prices")
                .addMethod(Shop.PRICE, ServerCalls.asyncUnaryCall((sku, reply) -> {
                    int call = priceCalls.incrementAndGet();
                    pause(call % 33 == 0 ? 1000 : 20);
                    if (Context.current().isCancelled()) {
                        cancelled.incrementAndGet();   // the caller already has an answer from another attempt
                        return;
                    }
                    reply.onNext(sku + " = 19.99");
                    reply.onCompleted();
                }))
                .build();
        ServerServiceDefinition orders = ServerServiceDefinition.builder("shop.Orders")
                .addMethod(Shop.PLACE_ORDER, ServerCalls.asyncUnaryCall((order, reply) -> {
                    ordersPlaced.incrementAndGet();
                    pause(20);
                    reply.onNext("placed " + order);
                    reply.onCompleted();
                }))
                .build();
        server = NettyServerBuilder.forAddress(new InetSocketAddress("127.0.0.1", 0))
                .addService(prices)
                .addService(orders)
                .build()
                .start();
    }

    private static void pause(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    public int port() {
        return server.getPort();
    }

    public int priceCalls() {
        return priceCalls.get();
    }

    public int cancelled() {
        return cancelled.get();
    }

    public int ordersPlaced() {
        return ordersPlaced.get();
    }

    public void reset() {
        priceCalls.set(0);
        cancelled.set(0);
        ordersPlaced.set(0);
    }

    @Override
    public void close() throws Exception {
        server.shutdownNow().awaitTermination();
    }
}
