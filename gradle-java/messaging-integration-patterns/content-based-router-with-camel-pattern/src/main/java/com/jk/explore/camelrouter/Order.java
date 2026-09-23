package com.jk.explore.camelrouter;

/**
 * An order, as it travels on the broker. What it contains is the only thing that decides where it goes:
 * nothing outside the message says the destination.
 *
 * <p>The body on the wire is plain text, one field per part, so that the router really is reading the
 * content and not a label somebody stuck on the outside.
 */
public record Order(String id, String kind, String shipping, String region, long pence) {

    /** Turns the order into the text that is actually put on the queue. */
    public String body() {
        return "id=" + id + ";kind=" + kind + ";shipping=" + shipping + ";region=" + region + ";pence=" + pence;
    }

    /** Reads an order back out of a message body. */
    public static Order parse(String body) {
        String id = "";
        String kind = "";
        String shipping = "";
        String region = "";
        long pence = 0;
        for (String field : body.split(";")) {
            int eq = field.indexOf('=');
            if (eq < 0) {
                continue;
            }
            String name = field.substring(0, eq);
            String value = field.substring(eq + 1);
            switch (name) {
                case "id" -> id = value;
                case "kind" -> kind = value;
                case "shipping" -> shipping = value;
                case "region" -> region = value;
                case "pence" -> pence = Long.parseLong(value);
                default -> {
                }
            }
        }
        return new Order(id, kind, shipping, region, pence);
    }

    /** The price in pounds, for people to read. The wire carries pence. */
    public String pounds() {
        return String.format("%d.%02d", pence / 100, pence % 100);
    }

    public String describe() {
        return id + " (" + kind + ", " + shipping + ", " + region + ", " + pounds() + ")";
    }
}
