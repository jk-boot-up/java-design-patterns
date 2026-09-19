package com.jk.explore.balkingpattern;

import java.util.concurrent.CountDownLatch;

public class BalkingDemo {

    /** Starts a save on another thread, holds it inside the write, and returns the thread with the gate to release it. */
    static Thread startHeldSave(Storage storage, Gate gate, Runnable save) throws InterruptedException {
        CountDownLatch inside = new CountDownLatch(1);
        storage.holdWritesAt(gate, inside::countDown);
        Thread t = new Thread(save);
        t.start();
        inside.await();
        return t;
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Save every time it is asked.");
        Storage storage = new Storage();
        AlwaysSavingDraft draft = new AlwaysSavingDraft(storage);
        draft.edit("2 x MUG-BLUE");
        for (int i = 0; i < 5; i++) {
            draft.save();
        }
        System.out.println("  one edit, and the autosave timer fires 5 times: " + storage.written().size() + " writes.");
        System.out.println("  four of them wrote exactly what was already there.");
    }

    private static void two() {
        System.out.println("TWO. Balk when there is nothing to save.");
        Storage storage = new Storage();
        BalkingDraft draft = new BalkingDraft(storage);
        draft.edit("2 x MUG-BLUE");
        StringBuilder results = new StringBuilder();
        for (int i = 0; i < 5; i++) {
            results.append(draft.save()).append(i < 4 ? ", " : "");
        }
        System.out.println("  the same five calls: " + results + ".");
        System.out.println("  writes: " + storage.written().size() + ".");
    }

    private static void three() throws Exception {
        System.out.println("THREE. Balk when a save is already running.");
        Storage storage = new Storage();
        BalkingDraft draft = new BalkingDraft(storage);
        draft.edit("2 x MUG-BLUE");
        Gate gate = new Gate();
        Thread first = startHeldSave(storage, gate, draft::save);
        System.out.println("  a save is in progress. a second call arrives: " + draft.save() + ", straight away, without waiting.");
        gate.open();
        first.join();
        System.out.println("  the first save finishes. writes: " + storage.written().size() + ". the second caller did not queue behind it.");
    }

    private static void four() throws Exception {
        System.out.println("FOUR. An edit during a save.");
        Storage storage = new Storage();
        CarelessBalkingDraft careless = new CarelessBalkingDraft(storage);
        careless.edit("2 x MUG-BLUE");
        Gate g1 = new Gate();
        Thread t1 = startHeldSave(storage, g1, careless::save);
        careless.edit("3 x MUG-BLUE");
        g1.open();
        t1.join();
        System.out.println("  the customer changes 2 to 3 while the save runs. a draft that marks itself clean when the save ends: dirty " + careless.isDirty() + ", next save says " + careless.save() + ". saved: " + storage.written() + ".");
        Storage storage2 = new Storage();
        BalkingDraft draft = new BalkingDraft(storage2);
        draft.edit("2 x MUG-BLUE");
        Gate g2 = new Gate();
        Thread t2 = startHeldSave(storage2, g2, draft::save);
        draft.edit("3 x MUG-BLUE");
        g2.open();
        t2.join();
        storage2.holdWritesAt(null, () -> { });
        System.out.println("  with a version counter: dirty " + draft.isDirty() + ", next save says " + draft.save() + ". saved: " + storage2.written() + ".");
    }

    private static void five() {
        System.out.println("FIVE. The caller is told.");
        Storage storage = new Storage();
        BalkingDraft draft = new BalkingDraft(storage);
        System.out.println("  nothing edited: " + draft.save() + ".");
        draft.edit("x");
        System.out.println("  edited: " + draft.save() + ".");
        System.out.println("  a balk is an answer, not an error. the caller can retry, ignore it, or tell the user, and the enum says which happened.");
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill.");
        Storage storage = new Storage();
        BalkingDraft draft = new BalkingDraft(storage);
        draft.edit("2 x MUG-BLUE");
        Gate gate = new Gate();
        Thread first = startHeldSave(storage, gate, draft::save);
        draft.edit("3 x MUG-BLUE");
        SaveResult second = draft.save();
        System.out.println("  the customer clicks Save while the autosave is running: " + second + ". their click did nothing.");
        gate.open();
        first.join();
        System.out.println("  the draft is still dirty: " + draft.isDirty() + ". saved so far: " + storage.written() + ". the change waits for the next save.");
        System.out.println("  balking suits work that can be skipped and done later. it is wrong where every request must be honoured, because a balked request is simply not done.");
    }
}
