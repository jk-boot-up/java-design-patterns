package com.jk.explore.flagd;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.TimeUnit;

/** Runs a command and returns what it printed. */
public final class Shell {

    private Shell() {
    }

    public static String run(String... command) {
        return runWithInput(null, command);
    }

    public static String runWithInput(String stdin, String... command) {
        try {
            ProcessBuilder pb = new ProcessBuilder(List.of(command)).redirectErrorStream(true);
            Process p = pb.start();
            if (stdin != null) {
                p.getOutputStream().write(stdin.getBytes(StandardCharsets.UTF_8));
            }
            p.getOutputStream().close();
            String out = new String(p.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
            if (!p.waitFor(300, TimeUnit.SECONDS)) {
                p.destroyForcibly();
                throw new IllegalStateException("timed out: " + String.join(" ", command));
            }
            if (p.exitValue() != 0) {
                throw new IllegalStateException(String.join(" ", command) + " failed:\n" + out);
            }
            return out.strip();
        } catch (IOException | InterruptedException e) {
            throw new IllegalStateException(e);
        }
    }

    public static boolean works(String... command) {
        try {
            run(command);
            return true;
        } catch (RuntimeException e) {
            return false;
        }
    }
}
