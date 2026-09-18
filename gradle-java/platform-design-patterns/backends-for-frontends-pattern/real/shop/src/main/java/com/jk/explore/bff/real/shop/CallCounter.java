package com.jk.explore.bff.real.shop;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.stereotype.Component;

/**
 * How many times each of the five services was called, counted where the calls land
 * rather than where they are made.
 *
 * <p>Tier 1 counts calls in a {@code CallLog} the caller writes to, which is honest for
 * a single process and would be worth nothing here — a backend could claim any number
 * it liked. These counts are kept by the callee. When the demo says the phone's backend
 * made four internal calls and not five, that four is the shop's own tally of requests
 * that actually arrived, taken from a process neither backend can reach into.
 *
 * <p>The counters are reset between acts by the demo script, which is why this is a
 * mutable singleton rather than something per-request.
 */
@Component
public class CallCounter {

    private final Map<String, AtomicInteger> counts = new LinkedHashMap<>();

    public CallCounter() {
        for (String service :
                new String[] {"catalog", "pricing", "inventory", "reviews", "recommendations"}) {
            counts.put(service, new AtomicInteger());
        }
    }

    public void record(String service) {
        counts.get(service).incrementAndGet();
    }

    public void reset() {
        counts.values().forEach(c -> c.set(0));
    }

    /** The five counts, plus their total, in a fixed order so a transcript is stable. */
    public Map<String, Object> snapshot() {
        Map<String, Object> out = new LinkedHashMap<>();
        int total = 0;
        for (Map.Entry<String, AtomicInteger> e : counts.entrySet()) {
            int n = e.getValue().get();
            out.put(e.getKey(), n);
            total += n;
        }
        out.put("total", total);
        return out;
    }
}
