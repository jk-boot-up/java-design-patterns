package com.jk.explore.splitteraggregator;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

/**
 * Collects the pieces of each order by its id. When every piece has arrived it puts them back in their original
 * order and emits one result. A piece that arrives twice is counted once. An order that has not completed by its
 * timeout is emitted as partial, and says which pieces are missing.
 */
public class Aggregator {

    public record Result(String orderId, List<String> contents, List<Integer> missing) {

        public boolean complete() {
            return missing.isEmpty();
        }
    }

    private static final class Open {
        final int total;
        final long startedAt;
        final Map<Integer, String> received = new TreeMap<>();

        Open(int total, long startedAt) {
            this.total = total;
            this.startedAt = startedAt;
        }
    }

    private final Map<String, Open> open = new HashMap<>();
    private final Clock clock;
    private final long timeoutMinutes;
    private int duplicates;

    public Aggregator(Clock clock, long timeoutMinutes) {
        this.clock = clock;
        this.timeoutMinutes = timeoutMinutes;
    }

    /** Takes one piece. Returns the completed order if this piece was the last one. */
    public Optional<Result> accept(Part part) {
        Open o = open.computeIfAbsent(part.orderId(), id -> new Open(part.total(), clock.now()));
        if (o.received.putIfAbsent(part.index(), part.content()) != null) {
            duplicates++;
            return Optional.empty();
        }
        if (o.received.size() == o.total) {
            open.remove(part.orderId());
            return Optional.of(new Result(part.orderId(), new ArrayList<>(o.received.values()), List.of()));
        }
        return Optional.empty();
    }

    /** Gives up on orders that have waited too long, and returns what they had, with the missing pieces named. */
    public List<Result> expire() {
        List<Result> partial = new ArrayList<>();
        open.entrySet().removeIf(e -> {
            Open o = e.getValue();
            if (clock.now() - o.startedAt < timeoutMinutes) {
                return false;
            }
            List<Integer> missing = new ArrayList<>();
            for (int i = 1; i <= o.total; i++) {
                if (!o.received.containsKey(i)) {
                    missing.add(i);
                }
            }
            partial.add(new Result(e.getKey(), new ArrayList<>(o.received.values()), missing));
            return true;
        });
        return partial;
    }

    public int openOrders() {
        return open.size();
    }

    public int duplicates() {
        return duplicates;
    }
}
