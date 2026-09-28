package com.jk.explore.eventsourcingeventstoredb;

import io.kurrent.dbclient.AppendToStreamOptions;
import io.kurrent.dbclient.EventData;
import io.kurrent.dbclient.KurrentDBClient;
import io.kurrent.dbclient.ReadAllOptions;
import io.kurrent.dbclient.ReadStreamOptions;
import io.kurrent.dbclient.ResolvedEvent;
import io.kurrent.dbclient.StreamNotFoundException;
import io.kurrent.dbclient.StreamState;
import io.kurrent.dbclient.WrongExpectedVersionException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

/**
 * The shop's loyalty log, kept in KurrentDB. One stream per customer, named loyalty-C-4417 and
 * so on, holding that customer's events oldest first.
 *
 * <p>There are three things this class can do to a stream, and that is the whole interface the
 * server offers for events: add to the end, read from the start, and delete the whole stream.
 * There is no way to change one event, and no way to remove one event from the middle.
 *
 * <p>Every event in a stream has a number, starting at 0, that KurrentDB calls its revision.
 * The revision of the last event is the stream's current revision. An append can say "only if
 * the stream is still at revision 3" — and that one sentence is optimistic concurrency.
 */
public final class LoyaltyLog implements AutoCloseable {

    /** What an append can say about the stream it expects to find. */
    public enum Check { NONE, EXPECTED_REVISION }

    /** A stream read from the start: its events, and the revision of the last one. */
    public record History(List<LoyaltyEvent> events, long revision) {
        public int balance() {
            return Balance.of(events);
        }
    }

    /** The server refused an append because the stream had moved on. */
    public static final class StreamMovedOn extends RuntimeException {
        private final long expected;
        private final long actual;

        StreamMovedOn(long expected, long actual) {
            super("expected revision " + expected + ", but the stream is at revision " + actual);
            this.expected = expected;
            this.actual = actual;
        }

        public long expected() {
            return expected;
        }

        public long actual() {
            return actual;
        }
    }

    private final KurrentDBClient client;

    public LoyaltyLog(KurrentDBClient client) {
        this.client = client;
    }

    public static String streamFor(String customerId) {
        return "loyalty-" + customerId;
    }

    /** Appends with no check at all: KurrentDB's "any" — whatever state the stream is in. */
    public long append(String customerId, EventData... events) {
        return append(customerId, StreamState.any(), events);
    }

    /** Appends only if the stream's last event is still the given revision. */
    public long appendExpecting(String customerId, long expectedRevision, EventData... events) {
        return append(customerId, StreamState.streamRevision(expectedRevision), events);
    }

    /** Appends only if the stream does not exist yet: KurrentDB's "no stream". */
    public long appendToNewStream(String customerId, EventData... events) {
        return append(customerId, StreamState.noStream(), events);
    }

    /** Returns the revision of the last event in the stream after the append. */
    private long append(String customerId, StreamState expected, EventData... events) {
        AppendToStreamOptions options = AppendToStreamOptions.get().streamState(expected);
        try {
            return client.appendToStream(streamFor(customerId), options, events).get()
                    .getNextExpectedRevision().toRawLong();
        } catch (ExecutionException e) {
            if (e.getCause() instanceof WrongExpectedVersionException wrong) {
                throw new StreamMovedOn(wrong.getExpectedState().toRawLong(), wrong.getActualState().toRawLong());
            }
            throw new IllegalStateException(e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** Reads the customer's stream from its first event to its last. */
    public History read(String customerId) {
        try {
            List<ResolvedEvent> resolved = client.readStream(streamFor(customerId),
                    ReadStreamOptions.get().forwards().fromStart()).get().getEvents();
            List<LoyaltyEvent> events = new ArrayList<>();
            long revision = -1;
            for (ResolvedEvent r : resolved) {
                events.add(EventJson.fromRecorded(r.getOriginalEvent()));
                revision = r.getOriginalEvent().getRevision();
            }
            return new History(List.copyOf(events), revision);
        } catch (ExecutionException e) {
            if (e.getCause() instanceof StreamNotFoundException) {
                throw (StreamNotFoundException) e.getCause();
            }
            throw new IllegalStateException(e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** True if reading the stream finds it; false if the server says there is no such stream. */
    public boolean exists(String customerId) {
        try {
            read(customerId);
            return true;
        } catch (StreamNotFoundException e) {
            return false;
        }
    }

    /**
     * Deletes the whole stream, the way KurrentDB calls a soft delete. The stream stops being
     * readable at once. The events themselves are not removed from the disk until a later clean-up
     * the server calls a scavenge, and the stream's name can be written to again.
     */
    public void delete(String customerId) {
        try {
            client.deleteStream(streamFor(customerId)).get();
        } catch (ExecutionException e) {
            throw new IllegalStateException(e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /**
     * Reads the store's single log of everything — every event in every stream, in the order the
     * server wrote them, which KurrentDB calls $all — and counts the ones that belong to one
     * customer's stream.
     */
    public int countInWholeLog(String customerId) {
        try {
            List<ResolvedEvent> all = client.readAll(ReadAllOptions.get().forwards().fromStart()).get().getEvents();
            int count = 0;
            for (ResolvedEvent r : all) {
                if (r.getOriginalEvent().getStreamId().equals(streamFor(customerId))) {
                    count++;
                }
            }
            return count;
        } catch (ExecutionException e) {
            throw new IllegalStateException(e.getCause());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        try {
            client.shutdown().get();
        } catch (Exception e) {
            // closing quietly is fine: the container is about to go too
        }
    }
}
