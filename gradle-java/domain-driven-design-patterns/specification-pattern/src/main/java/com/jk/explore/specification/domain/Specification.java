package com.jk.explore.specification.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * A business rule as an object: something that can say whether a candidate satisfies it, say what
 * it means in words, and say which parts of it a candidate fails. Rules combine with {@code and},
 * {@code or} and {@code not} into new rules, so a named rule is written once and used everywhere.
 */
public interface Specification<T> {

    boolean isSatisfiedBy(T candidate);

    String describe();

    /** The plain-language parts of this rule that the candidate fails, empty when it satisfies the rule. */
    List<String> unmet(T candidate);

    default Specification<T> and(Specification<T> other) {
        return new And<>(this, other);
    }

    default Specification<T> or(Specification<T> other) {
        return new Or<>(this, other);
    }

    default Specification<T> not() {
        return new Not<>(this);
    }

    /** One indivisible rule, with its description. */
    static <T> Specification<T> of(String description, java.util.function.Predicate<T> test) {
        return new Specification<>() {
            public boolean isSatisfiedBy(T candidate) {
                return test.test(candidate);
            }

            public String describe() {
                return description;
            }

            public List<String> unmet(T candidate) {
                return test.test(candidate) ? List.of() : List.of(description);
            }
        };
    }

    record And<T>(Specification<T> left, Specification<T> right) implements Specification<T> {
        public boolean isSatisfiedBy(T c) {
            return left.isSatisfiedBy(c) && right.isSatisfiedBy(c);
        }

        public String describe() {
            return "(" + left.describe() + " and " + right.describe() + ")";
        }

        public List<String> unmet(T c) {
            List<String> all = new ArrayList<>(left.unmet(c));
            all.addAll(right.unmet(c));
            return all;
        }
    }

    record Or<T>(Specification<T> left, Specification<T> right) implements Specification<T> {
        public boolean isSatisfiedBy(T c) {
            return left.isSatisfiedBy(c) || right.isSatisfiedBy(c);
        }

        public String describe() {
            return "(" + left.describe() + " or " + right.describe() + ")";
        }

        public List<String> unmet(T c) {
            if (isSatisfiedBy(c)) {
                return List.of();
            }
            List<String> all = new ArrayList<>(left.unmet(c));
            all.addAll(right.unmet(c));
            return all;
        }
    }

    record Not<T>(Specification<T> inner) implements Specification<T> {
        public boolean isSatisfiedBy(T c) {
            return !inner.isSatisfiedBy(c);
        }

        public String describe() {
            return "not " + inner.describe();
        }

        public List<String> unmet(T c) {
            return inner.isSatisfiedBy(c) ? List.of(describe()) : List.of();
        }
    }
}
