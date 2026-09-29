package com.jk.explore.contractwiremock;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The contract between checkout and payments, kept as one JSON file both teams share: each
 * interaction is a request and the reply it gets.
 */
public record Contract(List<Interaction> interactions) {

    public record Interaction(String description, String method, String url, String requestBody, int status, String responseBody) {
    }

    private static final Pattern ONE = Pattern.compile(
            "\"description\": \"(.*?)\".*?\"method\": \"(.*?)\", \"url\": \"(.*?)\", \"body\": \"((?:\\\\\"|[^\"])*)\".*?"
                    + "\"status\": (\\d+), \"body\": \"((?:\\\\\"|[^\"])*)\"", Pattern.DOTALL);

    /** Reads contracts/payments.json from the classpath. */
    public static Contract payments() {
        try (InputStream in = Contract.class.getResourceAsStream("/contracts/payments.json")) {
            String json = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            List<Interaction> list = new ArrayList<>();
            Matcher m = ONE.matcher(json);
            while (m.find()) {
                list.add(new Interaction(m.group(1), m.group(2), m.group(3), unescape(m.group(4)),
                        Integer.parseInt(m.group(5)), unescape(m.group(6))));
            }
            return new Contract(list);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private static String unescape(String s) {
        return s.replace("\\\"", "\"");
    }
}
