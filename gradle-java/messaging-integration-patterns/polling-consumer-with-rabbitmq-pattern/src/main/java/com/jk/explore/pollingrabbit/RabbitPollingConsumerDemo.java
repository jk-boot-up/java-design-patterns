package com.jk.explore.pollingrabbit;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against a real RabbitMQ broker started and stopped by this program.
 */
public final class RabbitPollingConsumerDemo {

    public static void main(String[] args) throws Exception {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                out.add(Broker.WOULD_NOT_START_ADVICE);
                return out;
            }

            out.add("ONE. RabbitMQ pushes orders at the printer, with no limit.");
            Orders.send(broker, 50);
            try (LabelPrinter printer = new LabelPrinter(broker)) {
                printer.subscribe(0);
                Poll.until("all 50 pushed", () -> printer.inHand() == 50);
                out.add("  a burst of 50 orders: the broker pushed " + printer.inHand()
                        + " at once into the printer's memory; the printer's buffer holds 10");
                out.add("  if the printer crashes now, all 50 go back to the queue and arrive again");
            }
            Poll.until("the 50 to be back", () -> broker.waiting(Orders.QUEUE) == 50);
            out.add("  after the crash: back on the queue " + broker.waiting(Orders.QUEUE));

            out.add("");
            out.add("TWO. A polling consumer: basicGet, up to 5 each tick.");
            try (LabelPrinter printer = new LabelPrinter(broker)) {
                int ticks = 0;
                while (printer.printed() < 50) {
                    printer.poll(5);
                    ticks++;
                }
                out.add("  printed " + printer.printed() + " of 50 in " + ticks + " ticks; never more than 5 in hand");
            }

            out.add("");
            out.add("THREE. Pausing is simply not polling.");
            Orders.send(broker, 20);
            try (LabelPrinter printer = new LabelPrinter(broker)) {
                printer.poll(5);
                Poll.until("the queue count to settle", () -> broker.waiting(Orders.QUEUE) == 15);
                out.add("  paper runs out after one tick: printed " + printer.printed()
                        + "; safely waiting on the queue: " + broker.waiting(Orders.QUEUE));
                while (printer.printed() < 20) {
                    printer.poll(5);
                }
                out.add("  paper loaded, polling resumes: printed " + printer.printed() + " of 20, none lost");

                out.add("");
                out.add("FOUR. When nothing is happening.");
                for (int i = 0; i < 600; i++) {
                    printer.poll(1);
                }
                out.add("  a quiet minute, polling every tenth of a second: " + printer.emptyPolls()
                        + " requests to the broker, all empty");
            }
            Orders.send(broker, 20);
            try (LabelPrinter printer = new LabelPrinter(broker)) {
                printer.subscribe(5);
                Poll.until("5 pushed", () -> printer.inHand() == 5);
                out.add("  RabbitMQ's middle way, push with prefetch 5: 20 orders waiting, the printer holds "
                        + printer.inHand() + ", and the broker waits for acknowledgements before sending more");
                out.add("  a quiet queue then costs no requests at all");
                while (printer.printed() < 20) {
                    printer.printInHand();
                    Poll.until("more pushed or all printed", () -> printer.inHand() > 0 || printer.printed() == 20);
                }
            }

            out.add("");
            out.add("FIVE. The bill.");
            out.add("  with polling, an order arriving just after a poll waits a whole interval");
            out.add("  and every empty poll is a request to the broker; RabbitMQ's own advice is to consume with a prefetch limit");
        }
        return out;
    }

    private RabbitPollingConsumerDemo() {
    }
}
