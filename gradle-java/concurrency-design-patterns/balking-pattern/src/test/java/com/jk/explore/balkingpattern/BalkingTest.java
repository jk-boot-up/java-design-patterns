package com.jk.explore.balkingpattern;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class BalkingTest {

    @Test
    void anAlwaysSavingDraftWritesOnEveryCall() {
        Storage s = new Storage();
        AlwaysSavingDraft d = new AlwaysSavingDraft(s);
        d.edit("x");
        for (int i = 0; i < 5; i++) d.save();
        assertEquals(5, s.written().size());
    }

    @Test
    void aBalkingDraftSavesOnceAndThenSaysThereIsNothingToSave() {
        Storage s = new Storage();
        BalkingDraft d = new BalkingDraft(s);
        d.edit("x");
        assertEquals(SaveResult.SAVED, d.save());
        assertEquals(SaveResult.NOTHING_TO_SAVE, d.save());
        assertEquals(1, s.written().size());
    }

    @Test
    void aNeverEditedDraftNeverWrites() {
        Storage s = new Storage();
        assertEquals(SaveResult.NOTHING_TO_SAVE, new BalkingDraft(s).save());
        assertTrue(s.written().isEmpty());
    }

    @RepeatedTest(5)
    void aSecondSaveWhileOneIsRunningBalksAtOnce() throws Exception {
        Storage s = new Storage();
        BalkingDraft d = new BalkingDraft(s);
        d.edit("x");
        Gate g = new Gate();
        Thread t = BalkingDemo.startHeldSave(s, g, d::save);
        assertEquals(SaveResult.ALREADY_SAVING, d.save());
        g.open();
        t.join();
        assertEquals(1, s.written().size());
    }

    @RepeatedTest(5)
    void anEditDuringASaveIsNotLostWithAVersionCounter() throws Exception {
        Storage s = new Storage();
        BalkingDraft d = new BalkingDraft(s);
        d.edit("2");
        Gate g = new Gate();
        Thread t = BalkingDemo.startHeldSave(s, g, d::save);
        d.edit("3");
        g.open();
        t.join();
        s.holdWritesAt(null, () -> { });
        assertTrue(d.isDirty());
        assertEquals(SaveResult.SAVED, d.save());
        assertEquals(List.of("2", "3"), s.written());
        assertFalse(d.isDirty());
    }

    @RepeatedTest(5)
    void theCarelessVersionLosesAnEditMadeDuringASave() throws Exception {
        Storage s = new Storage();
        CarelessBalkingDraft d = new CarelessBalkingDraft(s);
        d.edit("2");
        Gate g = new Gate();
        Thread t = BalkingDemo.startHeldSave(s, g, d::save);
        d.edit("3");
        g.open();
        t.join();
        assertFalse(d.isDirty());
        assertEquals(SaveResult.NOTHING_TO_SAVE, d.save());
        assertEquals(List.of("2"), s.written());
    }

    @Test
    void aBalkedRequestIsNotQueuedForLater() throws Exception {
        Storage s = new Storage();
        BalkingDraft d = new BalkingDraft(s);
        d.edit("2");
        Gate g = new Gate();
        Thread t = BalkingDemo.startHeldSave(s, g, d::save);
        assertEquals(SaveResult.ALREADY_SAVING, d.save());
        g.open();
        t.join();
        assertEquals(1, s.written().size());
    }
}
