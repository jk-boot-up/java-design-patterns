package com.jk.explore.reactor;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * The pattern: one thread waits for events on every connection at once, and hands each event to its handler.
 *
 * <p>The Selector is the event demultiplexer: it blocks until some connection
 * is ready (a new client, or bytes to read), then says which. The loop
 * dispatches: a new client gets registered for reading; a ready read is
 * answered. Handlers must be quick, because while one runs, nobody else is
 * served.
 */
public final class Reactor implements AutoCloseable {

    private final Selector selector;
    private final ServerSocketChannel server;
    private final Thread loop;
    private final Set<String> threadNames = ConcurrentHashMap.newKeySet();
    private volatile boolean running = true;

    public Reactor() throws IOException {
        selector = Selector.open();
        server = ServerSocketChannel.open();
        server.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 200);
        server.configureBlocking(false);
        server.register(selector, SelectionKey.OP_ACCEPT);
        loop = new Thread(this::run, "reactor");
        loop.setDaemon(true);
        loop.start();
    }

    private void run() {
        while (running) {
            try {
                selector.select();
                Iterator<SelectionKey> it = selector.selectedKeys().iterator();
                while (it.hasNext()) {
                    SelectionKey key = it.next();
                    it.remove();
                    threadNames.add(Thread.currentThread().getName());
                    if (key.isAcceptable()) {
                        onAccept();
                    } else if (key.isReadable()) {
                        onRead(key);
                    }
                }
            } catch (IOException e) {
                return;
            }
        }
    }

    /** Handler for "a new client arrived": register it for reading. */
    private void onAccept() throws IOException {
        SocketChannel client = server.accept();
        if (client != null) {
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ, ByteBuffer.allocate(256));
        }
    }

    /** Handler for "a client sent bytes": answer each complete line. */
    private void onRead(SelectionKey key) throws IOException {
        SocketChannel client = (SocketChannel) key.channel();
        ByteBuffer buf = (ByteBuffer) key.attachment();
        if (client.read(buf) < 0) {
            key.cancel();
            client.close();
            return;
        }
        String text = new String(buf.array(), 0, buf.position(), StandardCharsets.UTF_8);
        int nl = text.indexOf('\n');
        if (nl >= 0) {
            buf.clear();
            String reply = StockCommands.answer(text.substring(0, nl)) + "\n";
            client.write(ByteBuffer.wrap(reply.getBytes(StandardCharsets.UTF_8)));
        }
    }

    public int port() {
        return server.socket().getLocalPort();
    }

    /** How many different threads ever ran a handler. */
    public int handlerThreads() {
        return threadNames.size();
    }

    @Override
    public void close() throws IOException {
        running = false;
        selector.wakeup();
        server.close();
    }
}
