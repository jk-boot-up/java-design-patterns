package com.jk.explore.balkingpattern;

/** A draft whose save always writes, changed or not, busy or not. */
public class AlwaysSavingDraft {

    private final Storage storage;
    private String text = "";

    public AlwaysSavingDraft(Storage storage) {
        this.storage = storage;
    }

    public synchronized void edit(String text) {
        this.text = text;
    }

    public void save() {
        String snapshot;
        synchronized (this) {
            snapshot = text;
        }
        storage.write(snapshot);
    }
}
