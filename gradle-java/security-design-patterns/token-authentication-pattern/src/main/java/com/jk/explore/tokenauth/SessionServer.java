package com.jk.explore.tokenauth;

import java.util.HashMap;
import java.util.Map;

/**
 * Before: each server remembers its signed-in customers in its own memory, keyed by a session identifier.
 */
public final class SessionServer {

    private final String name;
    private final Map<String, String> sessions = new HashMap<>();
    private int next = 1;

    public SessionServer(String name) {
        this.name = name;
    }

    public String signIn(String customer) {
        String sessionId = name + "-session-" + next++;
        sessions.put(sessionId, customer);
        return sessionId;
    }

    public String cart(String sessionId) {
        String customer = sessions.get(sessionId);
        return customer == null ? "401 please sign in" : "200 " + customer + "'s cart";
    }
}
