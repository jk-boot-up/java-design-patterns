package com.jk.explore.loadlevelingsqs;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import software.amazon.awssdk.services.sqs.model.SqsException;

/**
 * What SQS does, asked of it directly.
 *
 * <p>One LocalStack container is started for the whole class, because starting it is the slow
 * part, and removed at the end. Every wait is a bounded poll on something SQS can be asked, or
 * SQS's own long poll; there is no sleep anywhere in this file.
 */
class RealSqsTest {

    private static LocalStack aws;

    @BeforeAll
    static void startLocalStack() {
        assumeTrue(LocalStack.containerRuntimeAvailable(), "needs a container runtime");
        aws = new LocalStack();
        aws.start();
    }

    @AfterAll
    static void stopLocalStack() {
        if (aws != null) {
            aws.close();
        }
    }

    @Test
    void sqsTakesTenOrdersInOneRequestAndRefusesEleven() {
        OrderQueue queue = OrderQueue.create(aws.sqs(), "ten-and-eleven");
        queue.sendTogether(Checkout.orders(1, 10));
        assertThrows(SqsException.class, () -> queue.sendTogether(Checkout.orders(11, 11)));
        assertThrows(SqsException.class, () -> queue.take(11));
        Poll.until("ten to be waiting", () -> queue.waiting() == 10);
    }

    @Test
    void aBurstBuildsItsFullDepthAndDrainsAtMostTenARound() {
        OrderQueue queue = OrderQueue.create(aws.sqs(), "burst");
        assertEquals(10, queue.sendAll(Checkout.orders(1001, 100)));
        Poll.until("the burst to be waiting", () -> queue.waiting() == 100);
        Warehouse warehouse = new Warehouse();
        Packer packer = new Packer(queue, warehouse);
        int rounds = 0;
        while (warehouse.ordersPacked() < 100) {
            int size = packer.round().size();
            // How many one receive hands out is SQS's choice, so only the ceiling is exact.
            assertTrue(size <= 10, "a round took " + size);
            rounds++;
            assertTrue(rounds < 100, "the queue never drained");
        }
        assertTrue(rounds >= 10);
        assertEquals(0, warehouse.packedTwiceOrMore());
        Poll.until("the queue to be empty", () -> queue.waiting() == 0 && queue.inFlight() == 0);
    }

    @Test
    void aTakenOrderIsHiddenThenHandedOutAgainWhenTheTimeoutRunsOut() {
        OrderQueue queue = OrderQueue.create(aws.sqs(), "hidden", 1);
        queue.sendOne("ORD-2001");
        OrderQueue.Taken first = queue.takeOne();
        assertEquals(1, first.timesHandedOut());
        assertEquals(1, queue.inFlight());
        assertEquals(0, queue.take(10).size(), "hidden from everybody else while in flight");
        OrderQueue.Taken again = queue.takeOne();
        assertEquals("ORD-2001", again.orderId());
        assertEquals(2, again.timesHandedOut());
        queue.delete(again);
        Poll.until("the queue to be empty", () -> queue.waiting() == 0 && queue.inFlight() == 0);
    }

    @Test
    void sayingStillWorkingKeepsTheOrderHiddenPastTheOldTimeout() {
        OrderQueue queue = OrderQueue.create(aws.sqs(), "still-working", 1);
        queue.sendOne("ORD-3002");
        OrderQueue.Taken taken = queue.takeOne();
        queue.stillWorking(taken, 10);
        assertEquals(0, queue.take(10, 2).size(), "a two-second long poll, past the one-second timeout, finds nothing");
        queue.delete(taken);
        Poll.until("the queue to be empty", () -> queue.waiting() == 0 && queue.inFlight() == 0);
    }

    @Test
    void ordersTakenByAPackerThatStopsComeBackAndNoneIsLost() {
        OrderQueue queue = OrderQueue.create(aws.sqs(), "crash", 1);
        queue.sendAll(Checkout.orders(4001, 20));
        Poll.until("twenty to be waiting", () -> queue.waiting() == 20);
        List<OrderQueue.Taken> round = queue.take(10);
        queue.deleteTogether(round.subList(0, 3));
        int hidden = round.size() - 3;
        Poll.until("the hidden orders to come back", () -> queue.waiting() == 20 - 3);
        Warehouse warehouse = new Warehouse();
        Packer packer = new Packer(queue, warehouse);
        int secondTime = 0;
        while (warehouse.ordersPacked() < 20 - 3) {
            secondTime += (int) packer.round().stream().filter(o -> o.timesHandedOut() > 1).count();
        }
        assertEquals(hidden, secondTime);
        assertEquals(0, queue.waiting());
    }

    @Test
    void sqsHasNoSettingForTheDeepestAQueueMayGet() {
        SqsException refused = assertThrows(SqsException.class,
                () -> OrderQueue.create(aws.sqs(), "limited", Map.of("MaximumDepth", "50")));
        assertTrue(refused.awsErrorDetails().errorMessage().contains("Unknown Attribute MaximumDepth"));
        assertEquals(345_600, OrderQueue.create(aws.sqs(), "defaults").keepsUntakenSeconds());
        assertEquals(30, OrderQueue.create(aws.sqs(), "defaults").visibilityTimeoutSeconds());
    }
}
