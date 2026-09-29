package com.jk.explore.privateclassdata;

/**
 * The pattern's data class: the invoice's figures, set once, with no way to change them afterwards.
 */
public record InvoiceData(String number, String customer, long netPence) {
}
