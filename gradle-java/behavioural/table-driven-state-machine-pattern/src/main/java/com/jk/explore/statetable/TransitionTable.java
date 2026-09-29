package com.jk.explore.statetable;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/**
 * The pattern: every allowed move, in one table. From this status, on this action, go to that status.
 *
 * <p>Anything not in the table is not allowed. The table can list its own
 * rows, and say which actions are allowed from a status, which is what a page
 * needs to decide which buttons to show.
 */
public final class TransitionTable {

    private final Map<Status, Map<Action, Status>> rows = new EnumMap<>(Status.class);

    public TransitionTable allow(Status from, Action action, Status to) {
        rows.computeIfAbsent(from, k -> new EnumMap<>(Action.class)).put(action, to);
        return this;
    }

    public Optional<Status> next(Status from, Action action) {
        return Optional.ofNullable(rows.getOrDefault(from, Map.of()).get(action));
    }

    public Set<Action> allowed(Status from) {
        return rows.getOrDefault(from, Map.of()).keySet();
    }

    public int transitions() {
        return rows.values().stream().mapToInt(Map::size).sum();
    }

    /** One printable line per status that has moves, e.g. "PLACED: PAY -> PAID, CANCEL -> CANCELLED". */
    public List<String> describe() {
        List<String> out = new ArrayList<>();
        rows.forEach((from, moves) -> {
            List<String> parts = new ArrayList<>();
            moves.forEach((a, to) -> parts.add(a + " -> " + to));
            out.add(from + ": " + String.join(", ", parts));
        });
        return out;
    }

    /** The shop's rules. */
    public static TransitionTable orders() {
        return new TransitionTable()
                .allow(Status.PLACED, Action.PAY, Status.PAID)
                .allow(Status.PLACED, Action.CANCEL, Status.CANCELLED)
                .allow(Status.PAID, Action.SHIP, Status.SHIPPED)
                .allow(Status.PAID, Action.REFUND, Status.REFUNDED)
                .allow(Status.SHIPPED, Action.DELIVER, Status.DELIVERED);
    }
}
