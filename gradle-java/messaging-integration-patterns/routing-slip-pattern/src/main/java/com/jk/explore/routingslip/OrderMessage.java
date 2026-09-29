package com.jk.explore.routingslip;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/**
 * An order travelling through the steps, carrying its routing slip: the steps still to visit, in order.
 */
public final class OrderMessage {

    private final String id;
    private final long pence;
    private final boolean gift;
    private final boolean ageRestricted;
    private final String country;
    private final Deque<String> slip = new ArrayDeque<>();
    private final List<String> visited = new ArrayList<>();
    private boolean ageVerified = true;

    public OrderMessage(String id, long pence, boolean gift, boolean ageRestricted, String country) {
        this.id = id;
        this.pence = pence;
        this.gift = gift;
        this.ageRestricted = ageRestricted;
        this.country = country;
    }

    public OrderMessage slip(List<String> steps) {
        slip.clear();
        slip.addAll(steps);
        return this;
    }

    public String nextStep() {
        return slip.poll();
    }

    public void visited(String step) {
        visited.add(step);
    }

    public List<String> slip() {
        return List.copyOf(slip);
    }

    public List<String> visitedSteps() {
        return visited;
    }

    public String id() {
        return id;
    }

    public long pence() {
        return pence;
    }

    public boolean gift() {
        return gift;
    }

    public boolean ageRestricted() {
        return ageRestricted;
    }

    public String country() {
        return country;
    }

    public boolean ageVerified() {
        return ageVerified;
    }

    public void failAgeCheck() {
        ageVerified = false;
    }
}
