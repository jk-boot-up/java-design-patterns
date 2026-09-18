package com.jk.explore.tracing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The problem, made mechanical.
 *
 * <p>It is easy to assert that logs are inadequate. These tests instead check the
 * specific property that makes them inadequate: the merged log contains two of
 * every line, correctly timestamped, with nothing on any line that says which
 * customer it belongs to. That is why no subtraction you perform on it is valid.
 */
class InterleavedLogTest {

    private static final List<InterleavedLog.Line> MERGED =
            InterleavedLog.twoConcurrentPageLoads();

    @Test
    @DisplayName("two customers produce two of every line")
    void containsBothRequests() {
        assertEquals(20, MERGED.size());
        assertEquals(2, MERGED.stream()
                .filter(line -> "quote started".equals(line.message())).count());
        assertEquals(2, MERGED.stream()
                .filter(line -> "quote complete".equals(line.message())).count());
    }

    @Test
    @DisplayName("the aggregator sorts by time, and only by time")
    void isSortedByTime() {
        long previous = Long.MIN_VALUE;
        for (InterleavedLog.Line line : MERGED) {
            assertTrue(line.atMillis() >= previous, "the merged log must be in time order");
            previous = line.atMillis();
        }
    }

    @Test
    @DisplayName("the two requests really do overlap")
    void requestsAreInterleaved() {
        // Ben's page load starts before Ada's has finished, so his opening line
        // lands in the middle of hers. If the two were sequential the log would
        // be readable and there would be no problem to solve.
        int firstGatewayOpen = indexOf("GET /product/A-2231", 0);
        int secondGatewayOpen = indexOf("GET /product/A-2231", firstGatewayOpen + 1);
        int firstResponse = indexOf("200 OK", 0);

        assertTrue(secondGatewayOpen < firstResponse,
                "the second request must begin before the first one finishes");
    }

    @Test
    @DisplayName("no line carries anything that identifies the customer")
    void nothingTellsTheRequestsApart() {
        // The whole argument in one assertion. Two pricing lines, identical in
        // every field except the timestamp, and a timestamp cannot tell you
        // which request a line belongs to.
        List<String> pricingLines = MERGED.stream()
                .filter(line -> "pricing".equals(line.service()))
                .map(InterleavedLog.Line::message)
                .toList();

        assertEquals(List.of("quote complete", "quote complete",
                "quote started", "quote started"),
                pricingLines.stream().sorted().toList());
    }

    @Test
    @DisplayName("a rendered line shows a time, a service and a message")
    void rendersLikeAnAggregator() {
        InterleavedLog.Line line =
                new InterleavedLog.Line(120, "pricing", "quote started");

        assertEquals("14:32:07.120  pricing          quote started", line.rendered());
    }

    @Test
    @DisplayName("times past a second roll over into the seconds column")
    void rendersSecondsCorrectly() {
        InterleavedLog.Line line =
                new InterleavedLog.Line(1_390, "gateway", "200 OK");

        assertEquals("14:32:08.390  gateway          200 OK", line.rendered());
    }

    @Test
    @DisplayName("the whole log renders with one line per entry")
    void rendersEveryLine() {
        String rendered = InterleavedLog.render(MERGED);

        assertEquals(MERGED.size(), rendered.lines().count());
    }

    private static int indexOf(String message, int from) {
        for (int i = from; i < MERGED.size(); i++) {
            if (MERGED.get(i).message().equals(message)) {
                return i;
            }
        }
        throw new AssertionError("no line said " + message);
    }
}
