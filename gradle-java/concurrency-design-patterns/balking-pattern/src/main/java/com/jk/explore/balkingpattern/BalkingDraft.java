package com.jk.explore.balkingpattern;

/**
 * A draft that saves only when it needs to. It balks, returns straight away, when there is nothing new to save or a
 * save is already running. It counts edits with a version, so a save marks clean only what it actually saved.
 */
public class BalkingDraft {

    private final Storage storage;
    private String text = "";
    private long version;
    private long savedVersion;
    private boolean saving;

    public BalkingDraft(Storage storage) {
        this.storage = storage;
    }

    public synchronized void edit(String text) {
        this.text = text;
        version++;
    }

    public SaveResult save() {
        String snapshot;
        long snapshotVersion;
        synchronized (this) {
            if (saving) {
                return SaveResult.ALREADY_SAVING;
            }
            if (version == savedVersion) {
                return SaveResult.NOTHING_TO_SAVE;
            }
            saving = true;
            snapshot = text;
            snapshotVersion = version;
        }
        try {
            storage.write(snapshot);
        } finally {
            synchronized (this) {
                saving = false;
                savedVersion = snapshotVersion;
            }
        }
        return SaveResult.SAVED;
    }

    public synchronized boolean isDirty() {
        return version != savedVersion;
    }
}
