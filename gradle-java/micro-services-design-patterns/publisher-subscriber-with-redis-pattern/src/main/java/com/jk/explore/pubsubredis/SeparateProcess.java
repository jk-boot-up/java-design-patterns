package com.jk.explore.pubsubredis;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/**
 * Starts {@link LoyaltyProcess} as a second Java program and collects what it prints.
 *
 * <p>This is the difference between the plain-Java twin and this project in one class. There,
 * every subscriber was an object in the same program as the publisher. Here, one of them is
 * not even in the same Java virtual machine.
 */
public class SeparateProcess implements AutoCloseable {

    private final Process process;
    private final List<String> lines = new ArrayList<>();
    private final Thread drain;

    public SeparateProcess(RedisServer server, int ordersToWaitFor) {
        String java = System.getProperty("java.home") + File.separator + "bin" + File.separator + "java";
        ProcessBuilder builder = new ProcessBuilder(java,
                "-cp", System.getProperty("java.class.path"),
                LoyaltyProcess.class.getName(),
                server.host(), String.valueOf(server.port()), String.valueOf(ordersToWaitFor));
        builder.redirectErrorStream(true);
        try {
            this.process = builder.start();
        } catch (IOException e) {
            throw new IllegalStateException("could not start the loyalty process", e);
        }
        this.drain = new Thread(() -> {
            try (BufferedReader out = new BufferedReader(
                    new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = out.readLine()) != null) {
                    synchronized (lines) {
                        lines.add(line);
                    }
                }
            } catch (IOException e) {
                // The process ended; there is nothing more to read.
            }
        }, "loyalty-output");
        drain.setDaemon(true);
        drain.start();
        Poll.until("the loyalty process to be listening", () -> printed().contains(LoyaltyProcess.READY));
    }

    public List<String> printed() {
        synchronized (lines) {
            return List.copyOf(lines);
        }
    }

    /** The order numbers the other process says it received. */
    public List<String> ordersReceived() {
        return printed().stream()
                .filter(line -> line.startsWith(LoyaltyProcess.GOT))
                .map(line -> line.substring(LoyaltyProcess.GOT.length()))
                .toList();
    }

    public boolean isSeparate() {
        return process.pid() != ProcessHandle.current().pid();
    }

    /** Waits for the other process to finish on its own, as it does after its last order. */
    public int awaitExit() {
        Poll.until("the loyalty process to exit", Duration.ofSeconds(30), () -> !process.isAlive());
        Poll.until("the loyalty output to be read", Duration.ofSeconds(5), () -> !drain.isAlive());
        return process.exitValue();
    }

    @Override
    public void close() {
        if (process.isAlive()) {
            process.destroyForcibly();
        }
    }
}
