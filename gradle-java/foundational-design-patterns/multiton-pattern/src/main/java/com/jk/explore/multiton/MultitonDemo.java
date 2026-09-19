package com.jk.explore.multiton;

import java.util.concurrent.CyclicBarrier;

public class MultitonDemo {

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A new one each time.");
        Warehouse.resetAll();
        Warehouse a = Warehouse.unshared("UK");
        Warehouse b = Warehouse.unshared("UK");
        a.reserve(10);
        System.out.println("  two callers each made a UK warehouse. same object: " + (a == b) + ". A has stock " + a.stock() + ", B has " + b.stock() + ".");
        System.out.println("  the shop now believes two different things about one warehouse.");
    }

    private static void two() {
        System.out.println("TWO. One per region.");
        Warehouse.resetAll();
        Warehouse a = Warehouse.of("UK");
        Warehouse b = Warehouse.of("UK");
        Warehouse eu = Warehouse.of("EU");
        System.out.println("  asked for UK twice: same object: " + (a == b) + ". asked for EU: same as UK: " + (a == eu) + ". created so far: " + Warehouse.created() + ".");
    }

    private static void three() {
        System.out.println("THREE. Shared, so they agree.");
        Warehouse.resetAll();
        Warehouse.of("UK").reserve(10);
        System.out.println("  one part of the shop reserved 10 in the UK. another part, asking for UK, sees stock " + Warehouse.of("UK").stock() + ". the EU warehouse has " + Warehouse.of("EU").stock() + ".");
    }

    private static void four() {
        System.out.println("FOUR. A fixed set of keys.");
        Warehouse.resetAll();
        Warehouse.of("UK");
        Warehouse.of("EU");
        Warehouse.of("US");
        try {
            Warehouse.of("MARS");
        } catch (IllegalArgumentException e) {
            System.out.println("  asked for MARS: refused, \"" + e.getMessage() + "\". instances held: " + Warehouse.held() + ".");
        }
    }

    private static void five() throws Exception {
        System.out.println("FIVE. Two threads, one region.");
        CyclicBarrier both = new CyclicBarrier(2);
        NaiveWarehouses naive = new NaiveWarehouses(() -> {
            try {
                both.await();
            } catch (Exception e) {
                throw new IllegalStateException(e);
            }
        });
        Warehouse.resetAll();
        Warehouse[] got = new Warehouse[2];
        Thread t1 = new Thread(() -> got[0] = naive.of("UK"));
        Thread t2 = new Thread(() -> got[1] = naive.of("UK"));
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("  look first, create second, no lock: both threads looked before either created. same object: " + (got[0] == got[1]) + ". created: " + Warehouse.created() + ".");
        Warehouse.resetAll();
        Thread[] safe = new Thread[8];
        Warehouse[] many = new Warehouse[8];
        CyclicBarrier start = new CyclicBarrier(8);
        for (int i = 0; i < 8; i++) {
            int n = i;
            safe[i] = new Thread(() -> {
                try {
                    start.await();
                } catch (Exception e) {
                    throw new IllegalStateException(e);
                }
                many[n] = Warehouse.of("UK");
            });
            safe[i].start();
        }
        for (Thread t : safe) {
            t.join();
        }
        boolean same = true;
        for (Warehouse w : many) {
            same &= w == many[0];
        }
        System.out.println("  with an atomic create-if-absent: 8 threads at once, same object: " + same + ". created: " + Warehouse.created() + ".");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Warehouse.resetAll();
        Warehouse.of("UK").reserve(30);
        System.out.println("  one test reserved 30. the next test starts, and asks for UK: stock " + Warehouse.of("UK").stock() + ", not 100. state leaks from one test to the next.");
        System.out.println("  the instances live as long as the program does: held " + Warehouse.held() + ", and nothing ever lets one go.");
        System.out.println("  and any code can reach any warehouse from anywhere, so who changed the stock is hard to say.");
    }
}
