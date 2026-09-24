package com.jk.explore.leaderelectionk8s;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.TimeUnit;

/** Runs a command, such as kind or kill, and returns what it printed. */
public final class Shell {

    private Shell() {
    }

    public static String run(String... command) {
        try {
            Process p = new ProcessBuilder(List.of(command)).redirectErrorStream(true).start();
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
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** True when the command runs and succeeds; false when it is missing or fails. */
    public static boolean works(String... command) {
        try {
            run(command);
            return true;
        } catch (RuntimeException e) {
            return false;
        }
    }
}
