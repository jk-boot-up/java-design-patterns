package com.jk.explore.prototypespring;

import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * A product listing, as in the hand-built prototype project, but now a prototype-scoped
 * bean: every request to the container builds a new one from the definition below.
 */
@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class Listing {

    static final AtomicInteger BUILT = new AtomicInteger();
    static final AtomicInteger DESTROYED = new AtomicInteger();

    private String title = "Untitled";
    private final List<String> images = new ArrayList<>(List.of("placeholder.png"));

    public Listing() {
        BUILT.incrementAndGet();
    }

    public String title() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public List<String> images() {
        return images;
    }

    /** Spring gives no way to copy a bean that has been edited, so the class still needs this. */
    public Listing copy() {
        Listing copy = new Listing();
        copy.title = title;
        copy.images.clear();
        copy.images.addAll(images);
        return copy;
    }

    @PreDestroy
    void close() {
        DESTROYED.incrementAndGet();
    }
}
