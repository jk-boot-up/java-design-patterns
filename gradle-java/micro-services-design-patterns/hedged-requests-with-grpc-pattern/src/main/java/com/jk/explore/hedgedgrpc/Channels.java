package com.jk.explore.hedgedgrpc;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import java.util.List;
import java.util.Map;

/**
 * gRPC client channels. Hedging is not code: it is a policy in the channel's service config.
 */
public final class Channels {

    public static ManagedChannel plain(int port) {
        return ManagedChannelBuilder.forAddress("127.0.0.1", port).usePlaintext().build();
    }

    /** Hedge calls to {@code service}: send a second attempt if no answer after {@code delay}, e.g. "0.05s". */
    public static ManagedChannel hedged(int port, String service, String delay) {
        Map<String, Object> policy = Map.of(
                "maxAttempts", 2.0,
                "hedgingDelay", delay,
                "nonFatalStatusCodes", List.of());
        Map<String, Object> serviceConfig = Map.of("methodConfig", List.of(Map.of(
                "name", List.of(Map.of("service", service)),
                "hedgingPolicy", policy)));
        return ManagedChannelBuilder.forAddress("127.0.0.1", port)
                .usePlaintext()
                .defaultServiceConfig(serviceConfig)
                .enableRetry()   // hedging is part of gRPC's retry support
                .build();
    }

    private Channels() {
    }
}
