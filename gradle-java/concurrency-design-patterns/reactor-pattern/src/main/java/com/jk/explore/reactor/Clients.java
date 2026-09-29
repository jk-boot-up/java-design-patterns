package com.jk.explore.reactor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

/**
 * Many shop tills connected at once, each able to ask one question and read the answer.
 */
public final class Clients implements AutoCloseable {

    private final List<Socket> sockets = new ArrayList<>();
    private final List<BufferedReader> readers = new ArrayList<>();
    private final List<PrintWriter> writers = new ArrayList<>();

    public Clients(int port, int count) throws IOException {
        for (int i = 0; i < count; i++) {
            Socket s = new Socket(InetAddress.getLoopbackAddress(), port);
            sockets.add(s);
            readers.add(new BufferedReader(new InputStreamReader(s.getInputStream())));
            writers.add(new PrintWriter(s.getOutputStream(), true));
        }
    }

    public void send(int i, String line) {
        writers.get(i).println(line);
    }

    public String read(int i) throws IOException {
        return readers.get(i).readLine();
    }

    public String ask(int i, String line) throws IOException {
        send(i, line);
        return read(i);
    }

    @Override
    public void close() throws IOException {
        for (Socket s : sockets) {
            s.close();
        }
    }
}
