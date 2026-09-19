package com.jk.explore.objectpool;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() throws InterruptedException {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PaymentDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("10 connections opened"), out);
        assertTrue(out.contains("2 connections opened"), out);
        assertTrue(out.contains("was: Ada Lovelace"), out);
        assertTrue(out.contains("nothing (rescued by a timeout)"), out);
        assertTrue(out.contains("50 connections opened, and 46 sit idle"), out);
    }
}
