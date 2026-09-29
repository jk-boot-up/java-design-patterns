package com.jk.explore.guaranteed;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The pattern: every message is written to a file on disk, and forced to the disk, before the sender is told it was accepted.
 *
 * <p>Delivery writes an acknowledgement line. After a crash, a new journal on
 * the same file finds every message that has no acknowledgement, and those
 * are delivered again.
 */
public final class Journal {

    private final Path file;
    private int diskWrites;

    public Journal(Path file) {
        this.file = file;
    }

    /** Accept a message: only returns once it is safely on disk. */
    public void send(String id, String body) {
        append("MSG|" + id + "|" + body);
    }

    /** The message was delivered: record that, so it is not sent again. */
    public void acknowledge(String id) {
        append("ACK|" + id);
    }

    /** Every message on disk that was never acknowledged, in the order they were sent. */
    public Map<String, String> unacknowledged() {
        try {
            if (!Files.exists(file)) {
                return Map.of();
            }
            Map<String, String> sent = new LinkedHashMap<>();
            Set<String> acked = new HashSet<>();
            for (String line : Files.readAllLines(file, StandardCharsets.UTF_8)) {
                String[] p = line.split("\\|", 3);
                if (p[0].equals("MSG")) {
                    sent.put(p[1], p[2]);
                } else {
                    acked.add(p[1]);
                }
            }
            acked.forEach(sent::remove);
            return sent;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private void append(String line) {
        try (FileChannel ch = FileChannel.open(file, StandardOpenOption.CREATE, StandardOpenOption.APPEND,
                StandardOpenOption.WRITE)) {
            ch.write(ByteBuffer.wrap((line + "\n").getBytes(StandardCharsets.UTF_8)));
            ch.force(true);
            diskWrites++;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    public int diskWrites() {
        return diskWrites;
    }

    public List<String> lines() {
        try {
            return Files.exists(file) ? Files.readAllLines(file) : new ArrayList<>();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
