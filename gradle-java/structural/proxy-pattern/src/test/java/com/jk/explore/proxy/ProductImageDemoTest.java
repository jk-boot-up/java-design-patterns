package com.jk.explore.proxy;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ProductImageDemoTest {

    private final PrintStream originalOut = System.out;
    private ByteArrayOutputStream capturedOut;

    @BeforeEach
    void redirectStdout() {
        capturedOut = new ByteArrayOutputStream();
        System.setOut(new PrintStream(capturedOut));
    }

    @AfterEach
    void restoreStdout() {
        System.setOut(originalOut);
    }

    @Test
    void demoPrintsTheFullNarrative() {
        ProductImageDemo.main(new String[0]);

        String output = capturedOut.toString();
        assertTrue(output.contains("Images loaded eagerly, before rendering anything: 3"));
        assertTrue(output.contains("Images loaded so far (real subject not yet touched): 0"));
        assertTrue(output.contains("Images loaded after first render: 1"));
        assertTrue(output.contains("Images loaded after second render (unchanged -- cached): 1"));
        assertTrue(output.contains("Catalog admin can render: Rendering SKU-2087 hero image (1920x1080)"));
        assertTrue(output.contains("Shopper denied: Only catalog admins may view SKU-2087"));
        assertTrue(output.contains("Total images loaded so far: 2 -- SKU-9001 is not among them yet, still lazy"));
        assertTrue(output.contains("Admin render through both proxies: Rendering SKU-9001 hero image (1920x1080)"));
        assertTrue(output.contains("Total images loaded after admin render: 3"));
        assertTrue(output.contains("Naive viewer denied: Only catalog admins may view SKU-9001"));
    }
}
