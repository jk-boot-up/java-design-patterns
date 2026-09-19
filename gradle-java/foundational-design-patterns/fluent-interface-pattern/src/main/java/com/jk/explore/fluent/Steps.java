package com.jk.explore.fluent;

import java.util.List;

/** A guided fluent query: each step only offers what may come next, so a wrong order does not compile. */
public final class Steps {

    public interface NeedsCategory {
        NeedsMax category(String category);
    }

    public interface NeedsMax {
        Ready under(int cents);
    }

    public interface Ready {
        Ready inStock();

        Ready cheapestFirst();

        List<String> run();
    }

    private Steps() {
    }

    public static NeedsCategory search() {
        return new Impl();
    }

    private static final class Impl implements NeedsCategory, NeedsMax, Ready {

        private Query q = Query.search();

        @Override
        public NeedsMax category(String category) {
            q = q.category(category);
            return this;
        }

        @Override
        public Ready under(int cents) {
            q = q.under(cents);
            return this;
        }

        @Override
        public Ready inStock() {
            q = q.inStock();
            return this;
        }

        @Override
        public Ready cheapestFirst() {
            q = q.cheapestFirst();
            return this;
        }

        @Override
        public List<String> run() {
            return q.run();
        }
    }
}
