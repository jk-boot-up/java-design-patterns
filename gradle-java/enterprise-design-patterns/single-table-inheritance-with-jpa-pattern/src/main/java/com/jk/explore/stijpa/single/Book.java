package com.jk.explore.stijpa.single;

import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

/**
 * A product row whose type column says BOOK.
 */
@Entity
@DiscriminatorValue("BOOK")
public class Book extends Product {

    /** Every book must have an ISBN, but the column is shared with every other type: it cannot be NOT NULL. */
    private String isbn;

    protected Book() {
    }

    public Book(String sku, String name, int pence, String isbn) {
        super(sku, name, pence);
        this.isbn = isbn;
    }

    @Override
    public String detail() {
        return "ISBN " + isbn;
    }
}
