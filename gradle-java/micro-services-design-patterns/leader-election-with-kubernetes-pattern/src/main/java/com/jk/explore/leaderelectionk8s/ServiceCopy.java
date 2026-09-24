package com.jk.explore.leaderelectionk8s;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * The demo's handle on one copy of the reporting service: a separate Java process running
 * {@link Candidate}. The demo can give it an order, hear what it says, freeze it, wake it,
 * shut it down cleanly or kill it outright.
 */
public final class ServiceCopy implements AutoCloseable {

    private final String name;
    private final Process process;
    private final Writer orders;
    private final List<String> heard = new ArrayList<>();

    private ServiceCopy(String name, Process process, Inbox inbox) {
        this.name = name;
        this.process = process;
        this.orders = new OutputStreamWriter(process.getOutputStream(), StandardCharsets.UTF_8);
        Thread listener = new Thread(() -> listen(inbox), "listen-" + name);
        listener.setDaemon(true);
        listener.start();
    }

    /** Starts a copy that joins the election on {@code lease}, or, when {@code elect} is false, one that never asks. */
    public static ServiceCopy start(String name, Path kubeconfig, String lease, boolean elect, Inbox inbox) {
        String java = ProcessHandle.current().info().command().orElse("java");
        String classpath = System.getProperty("candidate.classpath", System.getProperty("java.class.path"));
        try {
            Process p = new ProcessBuilder(java, "-Xmx96m", "-XX:+UseSerialGC", "-XX:TieredStopAtLevel=1",
                    "-cp", classpath, Candidate.class.getName(),
                    name, kubeconfig.toString(), lease, elect ? "elect" : "no-election")
                    .redirectError(ProcessBuilder.Redirect.INHERIT)
                    .start();
            return new ServiceCopy(name, p, inbox);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    private void listen(Inbox inbox) {
        try (BufferedReader out = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = out.readLine()) != null) {
                if (line.startsWith("SEND ")) {
                    inbox.receive(name, Integer.parseInt(line.substring(5)));
                }
                synchronized (heard) {
                    heard.add(line);
                }
            }
        } catch (IOException ignored) {
            // the process has gone
        }
    }

    public String name() {
        return name;
    }

    /** True once the copy has said {@code line}, exactly. */
    public boolean said(String line) {
        synchronized (heard) {
            return heard.contains(line);
        }
    }

    /** The first thing the copy said that starts with {@code prefix}, without the prefix. */
    public String saidAfter(String prefix) {
        synchronized (heard) {
            return heard.stream().filter(l -> l.startsWith(prefix)).map(l -> l.substring(prefix.length()))
                    .findFirst().orElse("");
        }
    }

    public void awaitSaying(String line) {
        Poll.until(name + " to say " + line, () -> said(line));
    }

    public void awaitSayingSomething(String prefix) {
        Poll.until(name + " to say " + prefix, () -> !saidAfter(prefix).isEmpty());
    }

    /** Sends one order to the copy, such as "report". */
    public void tell(String order) {
        try {
            orders.write(order + "\n");
            orders.flush();
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    /** Stops every thread in the process at once, the way a long garbage-collection pause would. */
    public void freeze() {
        Shell.run("kill", "-STOP", Long.toString(process.pid()));
    }

    public void wake() {
        Shell.run("kill", "-CONT", Long.toString(process.pid()));
    }

    /** Asks the process to shut down, so its shutdown code runs. */
    public void stopCleanly() {
        process.destroy();
        waitForExit();
    }

    /** Kills the process outright. Nothing in it gets to run again. */
    public void kill() {
        process.destroyForcibly();
        waitForExit();
    }

    private void waitForExit() {
        try {
            if (!process.waitFor(30, TimeUnit.SECONDS)) {
                throw new IllegalStateException(name + " did not exit");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() {
        if (process.isAlive()) {
            kill();
        }
    }
}
