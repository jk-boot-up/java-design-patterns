package com.jk.explore.reactornetty;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

/**
 * A shop till: an ordinary blocking TCP client that asks the server one line at a time.
 */
public final class Till implements AutoCloseable {

    private final Socket socket;
    private final BufferedReader in;
    private final OutputStream out;

    public Till(int port) throws Exception {
        socket = new Socket("127.0.0.1", port);
        in = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
        out = socket.getOutputStream();
    }

    public String ask(String question) throws Exception {
        send(question + "\n");
        return in.readLine();
    }

    /** Sends raw text, possibly part of a line, and flushes it as its own network write. */
    public void send(String text) throws Exception {
        out.write(text.getBytes(StandardCharsets.UTF_8));
        out.flush();
    }

    public String readLine() throws Exception {
        return in.readLine();
    }

    @Override
    public void close() throws Exception {
        socket.close();
    }
}
