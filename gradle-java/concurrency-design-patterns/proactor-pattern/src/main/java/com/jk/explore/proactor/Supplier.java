package com.jk.explore.proactor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * A supplier's price server on this machine: answers "price KETTLE-1" with its price in pence, after 200 ms.
 */
public final class Supplier implements AutoCloseable {

    public static final int MS_TO_ANSWER = 200;

    private final ServerSocket server;
    private final int pricePence;

    public Supplier(int pricePence) throws IOException {
        this.pricePence = pricePence;
        server = new ServerSocket(0, 50, InetAddress.getLoopbackAddress());
        Thread t = new Thread(this::acceptLoop, "supplier");
        t.setDaemon(true);
        t.start();
    }

    private void acceptLoop() {
        while (!server.isClosed()) {
            try {
                Socket s = server.accept();
                Thread t = new Thread(() -> answer(s));
                t.setDaemon(true);
                t.start();
            } catch (IOException e) {
                return;
            }
        }
    }

    private void answer(Socket s) {
        try (s; BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
             PrintWriter out = new PrintWriter(s.getOutputStream(), true)) {
            in.readLine();
            Thread.sleep(MS_TO_ANSWER);
            out.println(pricePence);
        } catch (IOException | InterruptedException e) {
            // caller went away
        }
    }

    public int port() {
        return server.getLocalPort();
    }

    /** A port where nothing is listening, for a supplier that is down. */
    public static int deadPort() throws IOException {
        try (ServerSocket s = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            return s.getLocalPort();
        }
    }

    @Override
    public void close() throws IOException {
        server.close();
    }
}
