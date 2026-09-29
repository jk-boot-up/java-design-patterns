package com.jk.explore.stijpa.perclass;

import jakarta.persistence.Entity;

/**
 * Its own table, with its own copy of the shared columns.
 */
@Entity
public class BookItem extends CatalogItem {

    private String isbn;

    protected BookItem() {
    }

    public BookItem(String sku, String name, int pence, String isbn) {
        super(sku, name, pence);
        this.isbn = isbn;
    }
}
