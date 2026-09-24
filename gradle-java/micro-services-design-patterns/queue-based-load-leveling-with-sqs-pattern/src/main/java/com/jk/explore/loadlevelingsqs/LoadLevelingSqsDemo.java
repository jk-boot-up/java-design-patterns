package com.jk.explore.loadlevelingsqs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import software.amazon.awssdk.awscore.exception.AwsServiceException;

/**
 * Six acts against the real Amazon SQS API, played by LocalStack in a container that this
 * program starts and stops.
 *
 * <p>A sale sends 100 orders to the shop at once. Checkout puts every order on a queue and
 * answers the customer straight away; the packing service takes them off at its own pace of
 * 10 a round. The acts show the depth the burst really builds, what SQS does with an order
 * that has been taken but not finished, and what that costs.
 */
public class LoadLevelingSqsDemo {

    /** The burst: a sale's first second. */
    static final int BURST = 100;

    /** How long the queues in acts three to five hide a taken order, in seconds. */
    static final int SHORT_TIMEOUT = 2;

    public static void main(String[] args) {
        if (!LocalStack.containerRuntimeAvailable()) {
            System.out.println(LocalStack.NO_RUNTIME_ADVICE);
            return;
        }
        try (LocalStack aws = new LocalStack()) {
            try {
                aws.start();
            } catch (RuntimeException e) {
                System.out.println(LocalStack.WOULD_NOT_START_ADVICE);
                return;
            }
            one(aws);
            two(aws);
            three(aws);
            four(aws);
            five(aws);
            six(aws);
        }
    }

    /** The burst goes onto the queue, 10 to a request, and nobody is refused. */
    private static void one(LocalStack aws) {
        System.out.println("ONE. A burst lands on the queue.");
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-burst");
        List<String> orders = Checkout.orders(1001, BURST);
        System.out.println("  " + BURST + " orders arrive at once. checkout puts each one on a queue on Amazon SQS, played by LocalStack.");
        System.out.println("  11 orders in one request: " + refusal(() -> queue.sendTogether(orders.subList(0, 11))));
        int requests = queue.sendAll(orders);
        Poll.until("the burst to be on the queue", () -> queue.waiting() == BURST);
        System.out.println("  so the burst goes as " + requests + " requests of 10. SQS reports " + queue.waiting() + " waiting and " + queue.inFlight() + " in flight.");
        System.out.println("  nobody was refused. SQS keeps an order nobody takes for " + queue.keepsUntakenSeconds() + " seconds, which is " + queue.keepsUntakenSeconds() / 86_400 + " days.");
    }

    /** The packer drains the burst at 10 a round, and SQS's depth falls by 10 each round. */
    private static void two(LocalStack aws) {
        System.out.println("TWO. The packer keeps its own pace.");
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-drain");
        queue.sendAll(Checkout.orders(1001, BURST));
        Poll.until("the burst to be on the queue", () -> queue.waiting() == BURST);
        System.out.println("  the packing service asks for 11 at once: " + refusal(() -> queue.take(11)));
        List<OrderQueue.Taken> first = queue.take(OrderQueue.MOST_PER_REQUEST);
        System.out.println("  it takes " + first.size() + ". SQS now reports " + queue.waiting() + " waiting and " + queue.inFlight() + " in flight: taken, not yet finished.");
        Warehouse warehouse = new Warehouse();
        first.forEach(o -> warehouse.pack(o.orderId()));
        queue.deleteTogether(first);
        Packer packer = new Packer(queue, warehouse);
        List<Integer> depths = new ArrayList<>();
        depths.add(queue.waiting());
        int rounds = 1;
        int most = first.size();
        while (warehouse.ordersPacked() < BURST) {
            most = Math.max(most, packer.round().size());
            rounds++;
            depths.add(queue.waiting());
        }
        System.out.println("  it packs and deletes them. waiting after each round: " + join(depths) + ".");
        System.out.println("  " + warehouse.ordersPacked() + " packed in " + rounds + " rounds, never more than " + most + " at once. the deepest the queue got: " + BURST + ".");
    }

    /** A taken order is hidden, not removed, and comes back when its time runs out. */
    private static void three(LocalStack aws) {
        System.out.println("THREE. Taken is not removed.");
        System.out.println("  SQS hides a taken order for a while, then hands it out again. it calls that time the visibility timeout. the default is "
                + OrderQueue.create(aws.sqs(), "orders-default").visibilityTimeoutSeconds() + " seconds.");
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-hidden", SHORT_TIMEOUT);
        queue.sendOne("ORD-2001");
        Poll.until("the order to be waiting", () -> queue.waiting() == 1);
        OrderQueue.Taken taken = queue.takeOne();
        long takenAt = System.nanoTime();
        System.out.println("  this queue's timeout is " + queue.visibilityTimeoutSeconds() + " seconds. a packer takes " + taken.orderId()
                + " and stops before it finishes. SQS reports " + queue.waiting() + " waiting and " + queue.inFlight() + " in flight.");
        System.out.println("  a second packer asks at once, and is given " + queue.take(OrderQueue.MOST_PER_REQUEST).size() + " orders.");
        OrderQueue.Taken again = queue.takeOne();
        long seconds = (System.nanoTime() - takenAt) / 1_000_000_000L;
        System.out.println("  it keeps asking. " + again.orderId() + " comes back once the " + SHORT_TIMEOUT + " seconds have passed, not before: "
                + (seconds >= SHORT_TIMEOUT) + ". SQS has now handed it out " + again.timesHandedOut() + " times.");
        queue.delete(again);
        System.out.println("  SQS never knew the first packer stopped. it only knew the time ran out.");
    }

    /** A packer slower than the timeout: the order is packed twice. Saying "still working" stops it. */
    private static void four(LocalStack aws) {
        System.out.println("FOUR. A slow packer.");
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-slow", SHORT_TIMEOUT);
        Warehouse warehouse = new Warehouse();
        queue.sendOne("ORD-3001");
        Poll.until("the order to be waiting", () -> queue.waiting() == 1);
        OrderQueue.Taken byA = queue.takeOne();
        OrderQueue.Taken byB = queue.takeOne();
        System.out.println("  packer A takes " + byA.orderId() + " and needs longer than " + SHORT_TIMEOUT + " seconds. the time runs out, and packer B is given " + byB.orderId() + " too.");
        warehouse.pack(byB.orderId());
        queue.delete(byB);
        warehouse.pack(byA.orderId());
        queue.delete(byA);
        System.out.println("  both pack it and both delete it. " + byA.orderId() + " was packed " + warehouse.parcelsFor(byA.orderId()) + " times: two parcels for one order.");

        queue.sendOne("ORD-3002");
        Poll.until("the order to be waiting", () -> queue.waiting() == 1);
        OrderQueue.Taken slow = queue.takeOne();
        queue.stillWorking(slow, 10);
        System.out.println("  next, packer A takes " + slow.orderId() + " and, before its time runs out, tells SQS it is still working: hide it 10 seconds more.");
        int given = queue.take(OrderQueue.MOST_PER_REQUEST, 3).size();
        System.out.println("  packer B asks SQS to hold its question open for 3 seconds, past the old timeout. it is given " + given + " orders.");
        warehouse.pack(slow.orderId());
        queue.delete(slow);
        System.out.println("  packer A finishes and deletes. " + slow.orderId() + " was packed " + warehouse.parcelsFor(slow.orderId()) + " time.");
    }

    /** The packer's process stops in the middle of a round. The queue outlives it. */
    private static void five(LocalStack aws) {
        System.out.println("FIVE. The packer stops half way through a round.");
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-crash", SHORT_TIMEOUT);
        queue.sendAll(Checkout.orders(4001, BURST));
        Poll.until("the burst to be on the queue", () -> queue.waiting() == BURST);
        Warehouse warehouse = new Warehouse();
        List<OrderQueue.Taken> round = queue.take(OrderQueue.MOST_PER_REQUEST);
        List<OrderQueue.Taken> finished = round.subList(0, 3);
        finished.forEach(o -> warehouse.pack(o.orderId()));
        queue.deleteTogether(finished);
        System.out.println("  " + BURST + " orders on a queue with a " + SHORT_TIMEOUT + "-second timeout. the packer takes " + round.size()
                + ", finishes " + finished.size() + ", and its process stops.");
        System.out.println("  SQS reports " + queue.waiting() + " waiting and " + queue.inFlight() + " in flight. nothing is lost; " + queue.inFlight() + " are only hidden.");
        int back = BURST - finished.size();
        Poll.until("the hidden orders to come back", () -> queue.waiting() == back);
        System.out.println("  when the timeout runs out they come back: " + queue.waiting() + " waiting. a new packer drains the queue.");
        Packer packer = new Packer(queue, warehouse);
        int handedOutTwice = 0;
        while (warehouse.ordersPacked() < BURST) {
            for (OrderQueue.Taken order : packer.round()) {
                if (order.timesHandedOut() > 1) {
                    handedOutTwice++;
                }
            }
        }
        System.out.println("  packed: " + warehouse.ordersPacked() + ", lost: " + (BURST - warehouse.ordersPacked()) + ", packed twice: " + warehouse.packedTwiceOrMore()
                + ". orders SQS handed out a second time: " + handedOutTwice + ".");
        System.out.println("  the queue outlived the process reading it.");
    }

    /** No depth limit to set, a backlog nobody refuses, and what the requests add up to. */
    private static void six(LocalStack aws) {
        System.out.println("SIX. The bill.");
        System.out.println("  asked for a queue that holds at most 50 orders, SQS answers: "
                + refusal(() -> OrderQueue.create(aws.sqs(), "orders-limited", Map.of("MaximumDepth", "50"))));
        OrderQueue queue = OrderQueue.create(aws.sqs(), "orders-overload");
        Packer packer = new Packer(queue, new Warehouse());
        int rounds = 20;
        for (int r = 0; r < rounds; r++) {
            queue.sendAll(Checkout.orders(5001 + r * 15, 15));
            packer.round();
        }
        Poll.until("the backlog to settle", () -> queue.inFlight() == 0);
        System.out.println("  orders arrive at 15 a round and the packer does 10, for " + rounds + " rounds. SQS refused none. waiting: " + queue.waiting() + ", and growing.");
        System.out.println("  nothing warns you. the depth is a number you ask SQS for, and act on: more packers, or a limit of your own.");

        OrderQueue batched = OrderQueue.create(aws.sqs(), "orders-bill-batched");
        OrderQueue single = OrderQueue.create(aws.sqs(), "orders-bill-single");
        aws.resetCount();
        batched.sendAll(Checkout.orders(6001, BURST));
        Warehouse warehouse = new Warehouse();
        Packer batchPacker = new Packer(batched, warehouse);
        while (warehouse.ordersPacked() < BURST) {
            batchPacker.round();
        }
        String tens = aws.requestTotal() + " requests " + names(aws.requests());
        aws.resetCount();
        Checkout.orders(6001, BURST).forEach(single::sendOne);
        for (int i = 0; i < BURST; i++) {
            single.delete(single.takeOne());
        }
        int ones = aws.requestTotal();
        System.out.println("  " + BURST + " orders, 10 to a request: " + tens + ". one at a time: " + ones + ".");
        System.out.println("  a taken order can come back, so packing one twice must do no harm. this demo needed 1 container for 1 queue service.");
    }

    private static String join(List<Integer> numbers) {
        StringBuilder out = new StringBuilder();
        for (int n : numbers) {
            out.append(out.length() > 0 ? ", " : "").append(n);
        }
        return out.toString();
    }

    private static String names(Map<String, Integer> requests) {
        StringBuilder out = new StringBuilder("(");
        requests.forEach((name, count) -> out.append(out.length() > 1 ? ", " : "").append(name).append(count > 1 ? " x" + count : ""));
        return out.append(")").toString();
    }

    /** Runs a request and returns the service's own reason for refusing it, or "accepted". */
    static String refusal(Runnable request) {
        try {
            request.run();
            return "accepted";
        } catch (AwsServiceException e) {
            return e.awsErrorDetails().errorMessage();
        }
    }
}
