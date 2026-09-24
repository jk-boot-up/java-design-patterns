package com.jk.explore.leaderelectionk8s;

import java.util.ArrayList;
import java.util.List;

/**
 * The store manager's inbox, where the nightly sales report is delivered.
 *
 * <p>It lives in the demo's own process, outside every copy of the service. When it is told to
 * check tokens, it remembers the highest token it has seen and refuses any report carrying a
 * lower one. That check, done by the thing being written to, is called fencing.
 */
public final class Inbox {

    private final boolean checksTokens;
    private final List<String> senders = new ArrayList<>();
    private final List<String> refusals = new ArrayList<>();
    private int highestToken = -1;

    public Inbox(boolean checksTokens) {
        this.checksTokens = checksTokens;
    }

    /** A report arrives from {@code sender}, which believed it led with {@code token}. */
    public synchronized void receive(String sender, int token) {
        if (checksTokens && token < highestToken) {
            refusals.add(sender + ": token " + token + " is older than " + highestToken);
            return;
        }
        highestToken = Math.max(highestToken, token);
        senders.add(sender);
    }

    /** Who the report was accepted from, in the order it arrived. */
    public synchronized List<String> senders() {
        return List.copyOf(senders);
    }

    public synchronized List<String> refusals() {
        return List.copyOf(refusals);
    }

    /** Reports received, accepted or refused. */
    public synchronized int received() {
        return senders.size() + refusals.size();
    }
}
