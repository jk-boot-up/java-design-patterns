package com.jk.explore.pollingconsumer;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayDeque;
import java.util.Deque;
import org.junit.jupiter.api.Test;

class PollingConsumerTest {

    @Test
    void takesAtMostWhatItCanHandle() {
        Deque<String> q = PollingConsumerDemo.burst(12);
        PollingConsumer c = new PollingConsumer(q, new LabelPrinter());
        assertEquals(5, c.tick());
        assertEquals(7, q.size());
    }

    @Test
    void pausedConsumerTakesNothing() {
        Deque<String> q = PollingConsumerDemo.burst(3);
        PollingConsumer c = new PollingConsumer(q, new LabelPrinter());
        c.pause();
        assertEquals(0, c.tick());
        assertEquals(3, q.size());
    }

    @Test
    void emptyPollsAreCounted() {
        PollingConsumer c = new PollingConsumer(new ArrayDeque<>(), new LabelPrinter());
        c.tick();
        c.tick();
        assertEquals(2, c.emptyPolls());
    }

    @Test
    void pushOverflows() {
        LabelPrinter p = new LabelPrinter();
        int refused = 0;
        for (int i = 0; i < 15; i++) {
            if (!p.push("x")) {
                refused++;
            }
        }
        assertEquals(5, refused);
    }
}
