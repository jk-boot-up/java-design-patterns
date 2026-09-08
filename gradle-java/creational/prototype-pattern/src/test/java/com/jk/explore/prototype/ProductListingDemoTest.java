package com.jk.explore.prototype;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("ProductListingDemo — runs end to end and proves clone independence")
class ProductListingDemoTest {

    private final PrintStream realOut = System.out;
    private ByteArrayOutputStream captured;

    @BeforeEach
    void captureStdout() {
        captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreStdout() {
        System.setOut(realOut);
    }

    @Test
    void demoRuns() {
        ProductListingDemo.main(new String[0]);

        String out = captured.toString();

        assertAll(
                () -> assertTrue(out.contains("master.images() unaffected: [earbuds-black-1.jpg, earbuds-black-2.jpg]"), out),
                () -> assertTrue(out.contains("master.attributes() unaffected: {color=Black"), out),
                () -> assertTrue(out.contains("shippingProfile is the same instance: true"), out),
                () -> assertTrue(out.contains("registry copies are independent instances: true"), out),
                () -> assertTrue(out.contains("Rejected: no listing template registered under: does-not-exist"), out));
    }
}
