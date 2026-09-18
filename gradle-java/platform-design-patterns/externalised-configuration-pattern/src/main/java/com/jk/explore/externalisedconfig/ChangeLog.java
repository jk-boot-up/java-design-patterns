package com.jk.explore.externalisedconfig;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Every change ever made to the configuration, in the order it happened.
 *
 * <p>When you move a number out of the program you lose three things that were
 * protecting it without anyone having to think about it: the compiler, the code
 * review, and the version history. The compiler and the review have to be
 * replaced by validation — see {@link MoneySetting} and {@link GuardedSettings}.
 * The version history has to be replaced by this.
 *
 * <p>Note that it is append-only. There is no method here to edit or delete a
 * past entry, and that is not an oversight. An audit trail that can be tidied up
 * afterwards answers no questions at all, because the one occasion you most need
 * it is the one occasion somebody has a reason to tidy it.
 *
 * <p>{@link #valueBefore(String)} is what makes rollback cheap. It walks
 * backwards to the most recent change to a key and hands back what that key held
 * beforehand, so undoing a bad change is a lookup rather than a recollection.
 */
public final class ChangeLog {

    private final List<ConfigChange> changes = new ArrayList<>();

    /** Appends one change and hands it back, numbered. */
    public ConfigChange record(LocalDateTime at, String key, String was, String now, String who) {
        ConfigChange change = new ConfigChange(changes.size() + 1, at, key, was, now, who);
        changes.add(change);
        return change;
    }

    /** Everything recorded, oldest first. The list cannot be altered. */
    public List<ConfigChange> changes() {
        return List.copyOf(changes);
    }

    /** Just the changes to one key, oldest first. */
    public List<ConfigChange> changesTo(String key) {
        return changes.stream().filter(c -> c.key().equals(key)).toList();
    }

    /**
     * What this key held immediately before its most recent change.
     *
     * <p>Empty if the key has never been changed, or if its most recent change
     * was the one that created it — in both cases there is nothing to roll back
     * to, and saying so honestly is better than inventing a value.
     */
    public Optional<String> valueBefore(String key) {
        List<ConfigChange> history = changesTo(key);
        if (history.isEmpty()) {
            return Optional.empty();
        }
        String was = history.get(history.size() - 1).was();
        return ConfigChange.NOT_SET.equals(was) ? Optional.empty() : Optional.of(was);
    }

    /** How many changes have been recorded in total. */
    public int size() {
        return changes.size();
    }
}
