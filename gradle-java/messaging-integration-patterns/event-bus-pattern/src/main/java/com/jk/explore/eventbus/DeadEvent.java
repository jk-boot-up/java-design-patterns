package com.jk.explore.eventbus;

/** Posted by the bus itself when an event had nobody listening. */
public record DeadEvent(Object event) {
}
