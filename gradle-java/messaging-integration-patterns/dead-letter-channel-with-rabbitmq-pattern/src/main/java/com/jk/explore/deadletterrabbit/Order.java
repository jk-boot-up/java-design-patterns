package com.jk.explore.deadletterrabbit;

import java.nio.charset.StandardCharsets;

/** One order from the shop. The body is what the customer's checkout wrote down, exactly as it was sent. */
public record Order(String id, String body) {

    public static Order of(String id, String rest) {
        return new Order(id, id + " " + rest);
    }

    public static Order fromBody(byte[] body) {
        String text = new String(body, StandardCharsets.UTF_8);
        int space = text.indexOf(' ');
        return new Order(space < 0 ? text : text.substring(0, space), text);
    }

    public byte[] bytes() {
        return body.getBytes(StandardCharsets.UTF_8);
    }
}
