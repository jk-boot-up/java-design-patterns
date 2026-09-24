package com.jk.explore.competingconsumersrabbitmq;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.DeliverCallback;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Predicate;

/**
 * One competing consumer: a warehouse picker, with its own connection to the broker, taking
 * pick orders from the shared queue.
 *
 * <p>A picker has two parts, because the broker has two moments. The first moment is the
 * broker <em>handing</em> an order over: it arrives down the network connection and waits in
 * the picker's tray. The second is the picker <em>picking</em> it: taking it from the tray,
 * reserving the stock, and then saying done. How many orders may sit in the tray at once is
 * the broker's prefetch setting. Keeping the two moments apart is what lets the demo count
 * orders a picker is holding but has not started.
 *
 * <p>The pickers never talk to each other. Each one only talks to the broker.
 */
public class Picker implements AutoCloseable {

    /** Prefetch 0 is RabbitMQ's way of saying no limit at all. It is also what you get by default. */
    public static final int NO_LIMIT = 0;

    private record Handed(PickOrder order, long receipt, boolean seenBefore) {
    }

    private final String name;
    private final String queue;
    private final int prefetch;
    private final boolean saysDone;
    private final Stock stock;
    private final Connection connection;
    private final Channel amqp;

    private final LinkedBlockingQueue<Handed> tray = new LinkedBlockingQueue<>();
    private final AtomicInteger handedOver = new AtomicInteger();
    private final AtomicInteger seenBefore = new AtomicInteger();
    private final List<String> handedOrders = new ArrayList<>();
    private final List<String> picked = new ArrayList<>();
    private final CountDownLatch released = new CountDownLatch(1);
    private final Thread worker;

    private volatile Predicate<PickOrder> stallOn = order -> false;
    private volatile String inHand;
    private volatile boolean crashed;
    private volatile boolean stopping;

    private Picker(String name, Broker broker, String queue, int prefetch, boolean saysDone, Stock stock) {
        this.name = name;
        this.queue = queue;
        this.prefetch = prefetch;
        this.saysDone = saysDone;
        this.stock = stock;
        this.connection = broker.connect();
        try {
            this.amqp = connection.createChannel();
        } catch (IOException e) {
            throw new IllegalStateException("could not open a conversation with the broker", e);
        }
        this.worker = new Thread(this::work, "picker-" + name);
        this.worker.setDaemon(true);
    }

    /** A picker that may hold one order at a time: it is handed the next only after saying done. */
    public static Picker oneAtATime(String name, Broker broker, String queue, Stock stock) {
        return new Picker(name, broker, queue, 1, true, stock);
    }

    /** A picker that may hold up to this many orders it has not yet said done for. */
    public static Picker holdingUpTo(int orders, String name, Broker broker, String queue, Stock stock) {
        return new Picker(name, broker, queue, orders, true, stock);
    }

    /** A picker with no limit on what it may hold. This is what RabbitMQ does when nobody sets one. */
    public static Picker withNoLimit(String name, Broker broker, String queue, Stock stock) {
        return new Picker(name, broker, queue, NO_LIMIT, true, stock);
    }

    /**
     * A picker that never says done, because it told the broker to count every order as done the
     * moment it is handed over. RabbitMQ calls this automatic acknowledgement.
     */
    public static Picker forgettingOnHandover(String name, Broker broker, String queue, Stock stock) {
        return new Picker(name, broker, queue, NO_LIMIT, false, stock);
    }

    /**
     * Makes the picker get stuck on any order that matches: it reserves the stock and then waits,
     * until {@link #release()} or until it crashes. This stands in for a slow shelf, a jammed
     * printer, or a picker who is simply slow.
     */
    public Picker stallingOn(Predicate<PickOrder> which) {
        this.stallOn = which;
        return this;
    }

    /** Stuck on the very first order it is handed. */
    public Picker stallingOnTheFirst() {
        return stallingOn(order -> true);
    }

    /** Tells the broker how much this picker may hold, and starts listening. */
    public Picker start() {
        try {
            amqp.basicQos(prefetch);
            DeliverCallback onHandedOver = (tag, delivery) -> {
                PickOrder order = PickOrder.read(new String(delivery.getBody(), StandardCharsets.UTF_8));
                boolean again = delivery.getEnvelope().isRedeliver();
                synchronized (handedOrders) {
                    handedOrders.add(order.orderId());
                }
                if (again) {
                    seenBefore.incrementAndGet();
                }
                handedOver.incrementAndGet();
                tray.add(new Handed(order, delivery.getEnvelope().getDeliveryTag(), again));
            };
            amqp.basicConsume(queue, !saysDone, onHandedOver, tag -> {
            });
        } catch (IOException e) {
            throw new IllegalStateException("could not listen on " + queue, e);
        }
        worker.start();
        return this;
    }

    private void work() {
        while (!stopping && !crashed) {
            Handed next;
            try {
                next = tray.poll(50, TimeUnit.MILLISECONDS);
            } catch (InterruptedException e) {
                return;
            }
            if (next == null || crashed) {
                continue;
            }
            inHand = next.order().orderId();
            // The first half of picking: the stock is set aside for this order.
            stock.reserve(next.order());
            if (stallOn.test(next.order())) {
                waitForRelease();
            }
            if (crashed || stopping) {
                // Died, or went home, mid-work: the stock is reserved and the broker was never
                // told done, so the order is still the broker's.
                return;
            }
            synchronized (picked) {
                picked.add(next.order().orderId());
            }
            inHand = null;
            if (saysDone) {
                sayDone(next);
            }
        }
    }

    private void waitForRelease() {
        try {
            while (!crashed && !released.await(50, TimeUnit.MILLISECONDS)) {
                // keep waiting; a crash also ends the wait
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void sayDone(Handed handed) {
        try {
            amqp.basicAck(handed.receipt(), false);
        } catch (Exception e) {
            // The connection has gone; the broker will hand this order to somebody else.
        }
    }

    /** Lets a stalled picker carry on, and stops it stalling again. */
    public void release() {
        released.countDown();
    }

    public String name() {
        return name;
    }

    /** How many orders the broker has handed to this picker, counting a repeat as another. */
    public int handedOver() {
        return handedOver.get();
    }

    /** The orders handed over, in the order they arrived. */
    public List<String> handedOrders() {
        synchronized (handedOrders) {
            return List.copyOf(handedOrders);
        }
    }

    /** How many of the handed-over orders came marked by the broker as seen before. */
    public int markedSeenBefore() {
        return seenBefore.get();
    }

    /** The orders this picker finished, in the order it finished them. */
    public List<String> picked() {
        synchronized (picked) {
            return List.copyOf(picked);
        }
    }

    /** Handed over but not finished: the order being picked, plus everything in the tray. */
    public int holding() {
        return handedOver() - picked().size();
    }

    /** The order being picked right now, or null when the picker is between orders. */
    public String inHand() {
        return inHand;
    }

    public boolean busy() {
        return inHand != null;
    }

    /**
     * Ends the connection the way a crash does: no goodbye to the broker. Whatever the picker was
     * handed and had not said done for is the broker's problem now.
     */
    public void crash() {
        crashed = true;
        try {
            connection.abort(0);
        } catch (Exception e) {
            // A crash has no error path.
        }
        joinWorker();
    }

    /** Stops politely, the way a picker going home at the end of a shift would. */
    @Override
    public void close() {
        stopping = true;
        released.countDown();
        joinWorker();
        try {
            connection.close();
        } catch (Exception e) {
            // Closing a connection twice, or one that already crashed, is not a failure.
        }
    }

    private void joinWorker() {
        try {
            if (worker.isAlive()) {
                worker.join(5_000);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
