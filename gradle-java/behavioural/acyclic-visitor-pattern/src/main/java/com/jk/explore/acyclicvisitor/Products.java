package com.jk.explore.acyclicvisitor;

/**
 * The catalogue's product types. Each accepts a visitor only if that visitor says it handles this type.
 */
public final class Products {

    /** What every product offers. {@code accept} returns false when the visitor does not handle this type. */
    public interface Product {
        String sku();

        long pricePence();

        boolean accept(ProductVisitor v);

        void acceptClassic(ClassicVisitor v);
    }

    public record Book(String sku, long pricePence) implements Product {
        public boolean accept(ProductVisitor v) {
            if (v instanceof ProductVisitor.BookVisitor b) {
                b.visit(this);
                return true;
            }
            return false;
        }

        public void acceptClassic(ClassicVisitor v) {
            v.visitBook(this);
        }
    }

    public record Food(String sku, long pricePence) implements Product {
        public boolean accept(ProductVisitor v) {
            if (v instanceof ProductVisitor.FoodVisitor f) {
                f.visit(this);
                return true;
            }
            return false;
        }

        public void acceptClassic(ClassicVisitor v) {
            v.visitFood(this);
        }
    }

    public record Electronics(String sku, long pricePence, int grams) implements Product {
        public boolean accept(ProductVisitor v) {
            if (v instanceof ProductVisitor.ElectronicsVisitor e) {
                e.visit(this);
                return true;
            }
            return false;
        }

        public void acceptClassic(ClassicVisitor v) {
            v.visitElectronics(this);
        }
    }

    /** New in act three. The classic visitor has no method for it, so acceptClassic cannot be written honestly. */
    public record GiftCard(String sku, long pricePence) implements Product {
        public boolean accept(ProductVisitor v) {
            if (v instanceof ProductVisitor.GiftCardVisitor g) {
                g.visit(this);
                return true;
            }
            return false;
        }

        public void acceptClassic(ClassicVisitor v) {
            throw new UnsupportedOperationException("ClassicVisitor has no visitGiftCard: change it and every visitor");
        }
    }

    private Products() {
    }
}
