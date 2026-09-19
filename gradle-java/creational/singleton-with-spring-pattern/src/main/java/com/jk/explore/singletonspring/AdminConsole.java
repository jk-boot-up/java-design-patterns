package com.jk.explore.singletonspring;

import org.springframework.stereotype.Component;

/** One of the three callers that must share a single counter. */
@Component
public class AdminConsole {

    private final OrderSequenceGenerator generator;

    public AdminConsole(OrderSequenceGenerator generator) {
        this.generator = generator;
    }

    public OrderSequenceGenerator generator() {
        return generator;
    }

    public String issue() {
        return generator.nextOrderNumber();
    }
}
