package com.jk.explore.domainevent.infrastructure;

import com.jk.explore.domainevent.domain.DomainEvent;

/** Something that reacts to events. It knows the event, and nothing about the order that raised it. */
public interface EventHandler {
    String name();

    void handle(DomainEvent event);
}
