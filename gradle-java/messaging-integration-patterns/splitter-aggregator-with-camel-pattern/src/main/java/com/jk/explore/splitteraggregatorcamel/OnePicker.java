package com.jk.explore.splitteraggregatorcamel;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * The picture before the pattern: one worker takes the whole order and walks every line of it, one after
 * another, on a single thread. It counts the steps it took and the threads it used, so the demo can say
 * plainly how much of the work was done at once, which is none of it.
 */
public class OnePicker implements Processor {

    private int steps;
    private final Set<String> threads = new LinkedHashSet<>();

    @Override
    public void process(Exchange exchange) {
        Order order = exchange.getIn().getBody(Order.class);
        int total = 0;
        for (OrderLine line : order.lines()) {
            steps++;
            threads.add(Thread.currentThread().getName());
            total += line.linePence();
        }
        exchange.getIn().setBody(total);
    }

    public int steps() {
        return steps;
    }

    public int threadsUsed() {
        return threads.size();
    }
}
