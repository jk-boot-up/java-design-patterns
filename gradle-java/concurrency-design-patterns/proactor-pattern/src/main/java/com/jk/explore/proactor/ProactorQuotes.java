package com.jk.explore.proactor;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * The pattern: start every operation at once, and let the system call a completion handler when each one finishes.
 *
 * <p>The caller only starts work: connect, and say what to do when that
 * completes. Java's asynchronous channels do the waiting, and call
 * {@link CompletionHandler#completed} or {@link CompletionHandler#failed} on
 * their own threads. Each request is a short chain: connected, then written,
 * then read.
 */
public final class ProactorQuotes {

    private final Map<Integer, String> results = new ConcurrentHashMap<>();
    private final CountDownLatch done;
    private long startedInMs;

    public ProactorQuotes(int count) {
        done = new CountDownLatch(count);
    }

    /** Starts every request and returns at once. */
    public void start(List<Integer> ports) throws IOException {
        long t0 = System.nanoTime();
        for (int port : ports) {
            AsynchronousSocketChannel ch = AsynchronousSocketChannel.open();
            ch.connect(new InetSocketAddress(InetAddress.getLoopbackAddress(), port), port, new Connected(ch));
        }
        startedInMs = (System.nanoTime() - t0) / 1_000_000;
    }

    public boolean await(long ms) throws InterruptedException {
        return done.await(ms, TimeUnit.MILLISECONDS);
    }

    public Map<Integer, String> results() {
        return results;
    }

    public long startedInMs() {
        return startedInMs;
    }

    /** Step one finished: connected. Now send the question. */
    private final class Connected implements CompletionHandler<Void, Integer> {
        private final AsynchronousSocketChannel ch;

        Connected(AsynchronousSocketChannel ch) {
            this.ch = ch;
        }

        public void completed(Void v, Integer port) {
            ByteBuffer question = ByteBuffer.wrap("price KETTLE-1\n".getBytes(StandardCharsets.UTF_8));
            ch.write(question, port, new Written(ch));
        }

        public void failed(Throwable e, Integer port) {
            finish(ch, port, "failed: " + (e.getMessage() == null ? e.getClass().getSimpleName() : e.getMessage()));
        }
    }

    /** Step two finished: the question was sent. Now read the answer. */
    private final class Written implements CompletionHandler<Integer, Integer> {
        private final AsynchronousSocketChannel ch;

        Written(AsynchronousSocketChannel ch) {
            this.ch = ch;
        }

        public void completed(Integer bytes, Integer port) {
            ByteBuffer answer = ByteBuffer.allocate(64);
            ch.read(answer, port, new Read(ch, answer));
        }

        public void failed(Throwable e, Integer port) {
            finish(ch, port, "failed: " + e.getMessage());
        }
    }

    /** Step three finished: the answer arrived. Record it. */
    private final class Read implements CompletionHandler<Integer, Integer> {
        private final AsynchronousSocketChannel ch;
        private final ByteBuffer answer;

        Read(AsynchronousSocketChannel ch, ByteBuffer answer) {
            this.ch = ch;
            this.answer = answer;
        }

        public void completed(Integer bytes, Integer port) {
            finish(ch, port, new String(answer.array(), 0, answer.position(), StandardCharsets.UTF_8).trim());
        }

        public void failed(Throwable e, Integer port) {
            finish(ch, port, "failed: " + e.getMessage());
        }
    }

    private void finish(AsynchronousSocketChannel ch, int port, String result) {
        results.put(port, result);
        try {
            ch.close();
        } catch (IOException e) {
            // already closed
        }
        done.countDown();
    }
}
