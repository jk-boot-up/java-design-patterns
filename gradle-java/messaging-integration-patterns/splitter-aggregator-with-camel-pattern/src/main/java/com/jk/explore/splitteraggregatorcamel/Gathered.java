package com.jk.explore.splitteraggregatorcamel;

/**
 * One finished answer that came out of the aggregator, and the reason it came out: either every expected
 * shipment had arrived, or the aggregator's patience ran out. Camel records that reason itself, and the
 * demo prints Camel's own word for it rather than one of its own.
 */
public record Gathered(Gathering order, String completedBy) {

    public boolean byTimeout() {
        return "timeout".equals(completedBy);
    }
}
