package com.jk.explore.mvc;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The demo is what the video shows and what the README quotes, so its output
 * is pinned here.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PlaceAnOrderDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    @DisplayName("the demo runs end to end and prints all five acts plus the acceptance block")
    void allFiveActsRun() {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. No model, no view, no controller."), output);
        assertTrue(output.contains("TWO. A model, a controller, and one view."), output);
        assertTrue(output.contains("THREE. A second view, the shortcut way."), output);
        assertTrue(output.contains("FOUR. The rule, written down"), output);
        assertTrue(output.contains("FIVE. Add the real second view."), output);
        assertTrue(output.contains("ACCEPTANCE"), output);
    }

    @Test
    @DisplayName("the numbers the README and narration quote are the numbers the demo prints")
    void theQuotedNumbersAreReal() {
        String output = runTheDemo();

        assertTrue(output.contains("the screen says £382.50. the email says £383.00."), output);
        assertTrue(output.contains("NOTHING IN THE BUILD OBJECTED."), output);
        assertTrue(output.contains("both views: £382.50."), output);
        assertTrue(output.contains("files added     : 1   view/EmailConfirmationView.java"), output);
        assertTrue(output.contains("classes across model + controller + views : 21"), output);
        assertTrue(output.contains("of those, never opened                    : 20"), output);
        assertTrue(output.contains("order ord-1001 for cust-8801: PLACED, 3 lines, £382.50"), output);
        assertTrue(output.contains("stock ESP-001 3, GRD-014 1, BNS-220 38"), output);
        assertTrue(output.contains("charged cust-8801 £382.50 once"), output);
        assertTrue(output.contains(
                "refused: not enough stock, unknown product, payment declined"), output);
    }

    @Test
    @DisplayName("the demo is deterministic: two runs produce byte-identical output")
    void theDemoIsDeterministic() {
        assertEquals(runTheDemo(), runTheDemo());
    }
}
