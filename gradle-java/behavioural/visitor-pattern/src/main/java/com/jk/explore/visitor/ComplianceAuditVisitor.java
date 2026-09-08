package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * Report four: which items in the catalog cannot simply be put in a box.
 *
 * <p>The report the bundle exists for. A product is restricted or it is
 * not — one field, one line. A bundle has no restriction of its own and is
 * restricted by <em>what is inside it</em>: a phone kit with a spare
 * lithium cell in the box needs the same air-freight declaration the cell
 * needs on its own, and nothing on the bundle says so.
 *
 * <p>Those are two genuinely different rules, and here they are two
 * methods. In {@link NaiveBundle} they are one method that was copied from
 * the other one, which is how the shop came to file a shipment with an
 * undeclared cell in it.
 */
public final class ComplianceAuditVisitor extends CategoryPathVisitor {

    private final List<String> findings = new ArrayList<>();
    private final Set<Restriction> obligations = new LinkedHashSet<>();
    private int itemsChecked;

    @Override
    public void visit(Product product) {
        itemsChecked++;
        if (product.restriction().isRestricted()) {
            record(pathTo(product.name()), product.sku(), product.restriction(), "");
        }
    }

    @Override
    public void visit(Bundle bundle) {
        itemsChecked++;
        // A bundle inherits every restriction in the box. This loop is the
        // rule; there is nowhere else it could go, because the bundle
        // itself carries no restriction field to read.
        for (Product content : bundle.contents()) {
            if (content.restriction().isRestricted()) {
                record(pathTo(bundle.name()), bundle.sku(), content.restriction(),
                        " (from " + content.name() + " in the box)");
            }
        }
    }

    private void record(String where, String sku, Restriction restriction, String note) {
        obligations.add(restriction);
        findings.add(String.format("%-34s %-8s %-14s %s%s",
                where, sku, restriction.label(), restriction.obligation(), note));
    }

    /** One line per obligation found, in tree order. */
    public List<String> findings() {
        return List.copyOf(findings);
    }

    /** The distinct restrictions in play — what the paperwork has to cover. */
    public Set<Restriction> obligations() {
        return new LinkedHashSet<>(obligations);
    }

    /** Sellable lines examined, whether or not they were restricted. */
    public int itemsChecked() {
        return itemsChecked;
    }

    /** Whether the shipment can go by air without a declaration. */
    public boolean clearForAir() {
        return !obligations.contains(Restriction.LITHIUM_BATTERY)
                && !obligations.contains(Restriction.FLAMMABLE);
    }
}
