package com.jk.explore.deadletterrabbit;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

/** Runs the demo once for the whole test run and keeps what it printed, so one container serves every test. */
final class Demo {

    private static String captured;

    private Demo() {
    }

    static synchronized String output() throws Exception {
        if (captured == null) {
            PrintStream original = System.out;
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            try {
                System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
                RabbitDeadLetterDemo.main(new String[0]);
            } finally {
                System.setOut(original);
            }
            captured = buffer.toString(StandardCharsets.UTF_8);
        }
        return captured;
    }
}
