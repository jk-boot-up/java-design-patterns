package com.jk.explore.proactor;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Without the pattern: ask each supplier in turn, and wait for each answer before asking the next.
 */
public final class BlockingQuotes {

    public static Map<Integer, Integer> ask(List<Integer> ports) throws IOException {
        Map<Integer, Integer> prices = new LinkedHashMap<>();
        for (int port : ports) {
            try (Socket s = new Socket(InetAddress.getLoopbackAddress(), port);
                 PrintWriter out = new PrintWriter(s.getOutputStream(), true);
                 BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()))) {
                out.println("price KETTLE-1");
                prices.put(port, Integer.parseInt(in.readLine().trim()));
            }
        }
        return prices;
    }

    private BlockingQuotes() {
    }
}
