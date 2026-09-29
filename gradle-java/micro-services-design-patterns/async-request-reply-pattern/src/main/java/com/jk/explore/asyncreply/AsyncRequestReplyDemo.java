package com.jk.explore.asyncreply;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: waiting and timing out, accepted at once, checking back, asking twice, and the bill.
 */
public final class AsyncRequestReplyDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The seller waits for a 6 second report.");
        Clock c1 = new Clock();
        ReportBuilder b1 = new ReportBuilder();
        SyncReportApi sync = new SyncReportApi(c1, b1);
        out.add("  first try: " + sync.getReport() + " (the gateway gives up after 3 s)");
        out.add("  second try: " + sync.getReport());
        out.add("  the report was built " + b1.runs() + " times; the seller received it 0 times");

        out.add("");
        out.add("TWO. Accepted at once, with a link to check.");
        Clock c2 = new Clock();
        ReportBuilder b2 = new ReportBuilder();
        AsyncReportApi api = new AsyncReportApi(c2, b2);
        out.add("  POST /reports: " + api.submit("seller-7-september"));
        out.add("  answered in 0 s; the report is built in the background");

        out.add("");
        out.add("THREE. Check back when told, then fetch the result.");
        PollingClient client = new PollingClient(c2, api);
        client.getReport("seller-7-september", 0);
        client.trace().stream().skip(1).forEach(t -> out.add("  " + t));

        out.add("");
        out.add("FOUR. The seller clicks twice.");
        out.add("  POST again with the same key: " + api.submit("seller-7-september"));
        out.add("  the report was built " + b2.runs() + " time");

        out.add("");
        out.add("FIVE. The bill: more requests, and a client that must wait well.");
        Clock c4 = new Clock();
        AsyncReportApi polite = new AsyncReportApi(c4, new ReportBuilder());
        new PollingClient(c4, polite).getReport("seller-7-september", 0);
        out.add("  one report, checking every 2 s as told: " + polite.requests() + " requests instead of 1");
        Clock c3 = new Clock();
        AsyncReportApi eager = new AsyncReportApi(c3, new ReportBuilder());
        new PollingClient(c3, eager).getReport("seller-7-september", 100);
        out.add("  an impatient client checking every 0.1 s: " + eager.requests() + " requests");
        out.add("  and the server must keep every job's state until the result is collected");
        return out;
    }

    private AsyncRequestReplyDemo() {
    }
}
