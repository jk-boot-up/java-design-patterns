package com.jk.explore.nullobject.pattern;

import com.jk.explore.nullobject.domain.Discount;
import com.jk.explore.nullobject.domain.DiscountDirectory;

import java.util.Optional;

/**
 * <strong>The fair alternative: make absence explicit in the type.</strong>
 * "No discount" is {@code Optional.empty()}. "The service is down" is still an
 * exception. The two can no longer be confused, and every caller must decide
 * what absence means to it.
 */
public class OptionalDirectory {

    private final DiscountDirectory directory;

    public OptionalDirectory(DiscountDirectory directory) {
        this.directory = directory;
    }

    public Optional<Discount> find(int customerId) {
        return Optional.ofNullable(directory.find(customerId));
    }
}
