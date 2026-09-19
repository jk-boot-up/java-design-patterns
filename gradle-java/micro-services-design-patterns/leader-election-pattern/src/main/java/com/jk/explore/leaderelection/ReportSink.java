package com.jk.explore.leaderelection;

import java.util.ArrayList;
import java.util.List;

/**
 * Where the nightly report goes. With fencing on, it refuses a write carrying a token older than one it
 * has already seen, so a leader that has been replaced cannot do harm by not yet knowing it.
 */
public class ReportSink {

    public static class StaleToken extends RuntimeException {
        public StaleToken(long token, long highest) {
            super("token " + token + " is older than " + highest);
        }
    }

    private final boolean fencing;
    private final List<String> written = new ArrayList<>();
    private long highestToken;

    public ReportSink(boolean fencing) {
        this.fencing = fencing;
    }

    public void write(long token, String writer) {
        if (fencing && token < highestToken) {
            throw new StaleToken(token, highestToken);
        }
        highestToken = Math.max(highestToken, token);
        written.add(writer);
    }

    public List<String> written() {
        return List.copyOf(written);
    }
}
