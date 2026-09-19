package com.jk.explore.balkingpattern;

/**
 * Balks correctly when clean or busy, and then makes the classic mistake: it marks the draft clean when the save
 * finishes, even if it was edited while the save was running. That edit is now never saved.
 */
public class CarelessBalkingDraft {

    private final Storage storage;
    private String text = "";
    private boolean dirty;
    private boolean saving;

    public CarelessBalkingDraft(Storage storage) {
        this.storage = storage;
    }

    public synchronized void edit(String text) {
        this.text = text;
        this.dirty = true;
    }

    public SaveResult save() {
        String snapshot;
        synchronized (this) {
            if (saving) {
                return SaveResult.ALREADY_SAVING;
            }
            if (!dirty) {
                return SaveResult.NOTHING_TO_SAVE;
            }
            saving = true;
            snapshot = text;
        }
        storage.write(snapshot);
        synchronized (this) {
            saving = false;
            dirty = false;
        }
        return SaveResult.SAVED;
    }

    public synchronized boolean isDirty() {
        return dirty;
    }
}
