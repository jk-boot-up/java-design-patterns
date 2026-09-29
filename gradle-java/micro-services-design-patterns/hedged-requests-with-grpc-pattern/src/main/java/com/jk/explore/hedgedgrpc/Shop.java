package com.jk.explore.hedgedgrpc;

import io.grpc.MethodDescriptor;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;

/**
 * The shop's two gRPC methods, described by hand. Requests and replies are plain text.
 */
public final class Shop {

    static final MethodDescriptor.Marshaller<String> TEXT = new MethodDescriptor.Marshaller<>() {
        @Override
        public InputStream stream(String value) {
            return new ByteArrayInputStream(value.getBytes(StandardCharsets.UTF_8));
        }

        @Override
        public String parse(InputStream stream) {
            try {
                return new String(stream.readAllBytes(), StandardCharsets.UTF_8);
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
    };

    /** Reading a price: safe to repeat. */
    public static final MethodDescriptor<String, String> PRICE = method("shop.Prices/Price");

    /** Placing an order: not safe to repeat. */
    public static final MethodDescriptor<String, String> PLACE_ORDER = method("shop.Orders/PlaceOrder");

    private static MethodDescriptor<String, String> method(String name) {
        return MethodDescriptor.<String, String>newBuilder()
                .setType(MethodDescriptor.MethodType.UNARY)
                .setFullMethodName(name)
                .setRequestMarshaller(TEXT)
                .setResponseMarshaller(TEXT)
                .build();
    }

    private Shop() {
    }
}
