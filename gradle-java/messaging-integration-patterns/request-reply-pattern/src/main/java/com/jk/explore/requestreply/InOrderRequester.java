package com.jk.explore.requestreply;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * Without the pattern: sends several requests, then assumes the replies come back in the same order.
 */
public final class InOrderRequester {

    public static List<String> ask(BlockingQueue<Message> requests, List<String> bodies) throws InterruptedException {
        BlockingQueue<Message> replies = new LinkedBlockingQueue<>();
        for (int i = 0; i < bodies.size(); i++) {
            requests.add(new Message("OLD-" + i, null, replies, bodies.get(i)));
        }
        List<String> matched = new ArrayList<>();
        for (String body : bodies) {
            matched.add(body + " -> " + replies.take().body());
        }
        return matched;
    }

    private InOrderRequester() {
    }
}
