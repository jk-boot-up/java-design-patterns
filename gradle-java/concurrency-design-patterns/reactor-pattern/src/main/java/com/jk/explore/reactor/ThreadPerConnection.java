package com.jk.explore.reactor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Without the pattern: a new thread for every connection, which mostly sits waiting for the client to say something.
 */
public final class ThreadPerConnection implements AutoCloseable {

    private final ServerSocket server;
    private final AtomicInteger threads = new AtomicInteger();

    public ThreadPerConnection() throws IOException {
        server = new ServerSocket(0, 200, InetAddress.getLoopbackAddress());
        Thread acceptor = new Thread(this::acceptLoop, "acceptor");
        acceptor.setDaemon(true);
        acceptor.start();
    }

    private void acceptLoop() {
        while (!server.isClosed()) {
            try {
                Socket s = server.accept();
                threads.incrementAndGet();
                Thread t = new Thread(() -> serve(s));
                t.setDaemon(true);
                t.start();
            } catch (IOException e) {
                return;
            }
        }
    }

    private void serve(Socket s) {
        try (s; BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
             PrintWriter out = new PrintWriter(s.getOutputStream(), true)) {
            String line;
            while ((line = in.readLine()) != null) {
                out.println(StockCommands.answer(line));
            }
        } catch (IOException e) {
            // client went away
        }
    }

    public int port() {
        return server.getLocalPort();
    }

    public int threadsStarted() {
        return threads.get();
    }

    @Override
    public void close() throws IOException {
        server.close();
    }
}
