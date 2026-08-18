package com.jk.explore.abstractfactory;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.util.List;
import java.util.stream.Stream;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

@DisplayName("MarketFactory — each factory hands back one matching family")
class MarketFactoryTest {

    static List<MarketFactory> allFactories() {
        return List.of(new UkMarketFactory(), new UsMarketFactory(), new IndiaMarketFactory());
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> families() {
        return Stream.of(
                arguments(new UkMarketFactory(), "United Kingdom",
                        UkVatCalculator.class, PoundFormatter.class, UkPostcodeValidator.class),
                arguments(new UsMarketFactory(), "United States",
                        UsSalesTaxCalculator.class, DollarFormatter.class, UsZipValidator.class),
                arguments(new IndiaMarketFactory(), "India",
                        IndiaGstCalculator.class, RupeeFormatter.class, IndiaPinValidator.class));
    }

    @ParameterizedTest(name = "{1} factory builds its own three products")
    @MethodSource("families")
    void factoryBuildsItsOwnFamily(MarketFactory factory, String market,
                                   Class<?> tax, Class<?> money, Class<?> address) {
        assertAll(
                () -> assertEquals(market, factory.market()),
                () -> assertInstanceOf(tax, factory.createTaxCalculator()),
                () -> assertInstanceOf(money, factory.createCurrencyFormatter()),
                () -> assertInstanceOf(address, factory.createAddressValidator()));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> markets() {
        return Stream.of(
                arguments(new UkMarketFactory(), "VAT", "GBP", "postcode", "EH1 1YZ", "10001"),
                arguments(new UsMarketFactory(), "Sales Tax", "USD", "ZIP code", "10001", "560001"),
                arguments(new IndiaMarketFactory(), "GST", "INR", "PIN code", "560001", "EH1 1YZ"));
    }

    @ParameterizedTest(name = "{1} / {2} / {3} travel together")
    @MethodSource("markets")
    void theThreeProductsAgreeWithEachOther(MarketFactory factory, String taxLabel,
                                            String currency, String postcodeLabel,
                                            String good, String foreign) {
        assertAll(
                () -> assertEquals(taxLabel, factory.createTaxCalculator().label()),
                () -> assertEquals(currency, factory.createCurrencyFormatter().currencyCode()),
                () -> assertEquals(postcodeLabel, factory.createAddressValidator().postcodeLabel()),
                () -> assertTrue(factory.createAddressValidator().isValid(good),
                        good + " should be valid in this market"),
                () -> assertFalse(factory.createAddressValidator().isValid(foreign),
                        foreign + " belongs to another market"));
    }

    @Test
    @DisplayName("every call returns a fresh product, never a shared one")
    void eachCallReturnsANewInstance() {
        for (MarketFactory factory : allFactories()) {
            assertAll(
                    () -> assertNotSame(factory.createTaxCalculator(), factory.createTaxCalculator()),
                    () -> assertNotSame(factory.createCurrencyFormatter(),
                            factory.createCurrencyFormatter()),
                    () -> assertNotSame(factory.createAddressValidator(),
                            factory.createAddressValidator()));
        }
    }

    @Test
    @DisplayName("the same subtotal is taxed differently in each market")
    void taxRatesDifferPerMarket() {
        assertAll(
                () -> assertEquals(24.00, new UkMarketFactory().createTaxCalculator().taxOn(120.00)),
                () -> assertEquals(10.65, new UsMarketFactory().createTaxCalculator().taxOn(120.00)),
                () -> assertEquals(21.60,
                        new IndiaMarketFactory().createTaxCalculator().taxOn(120.00)));
    }

    @Test
    @DisplayName("each market formats the same amount in its own currency")
    void currencyFormattingDiffersPerMarket() {
        assertAll(
                () -> assertEquals("£1,250.50",
                        new UkMarketFactory().createCurrencyFormatter().format(1250.50)),
                () -> assertEquals("$1,250.50",
                        new UsMarketFactory().createCurrencyFormatter().format(1250.50)),
                () -> assertEquals("₹1,250.50",
                        new IndiaMarketFactory().createCurrencyFormatter().format(1250.50)));
    }

    @Test
    @DisplayName("a brand new market needs no change to any existing class")
    void newMarketNeedsNoExistingChange() {
        // Germany, invented entirely here. Nothing above this line was edited.
        MarketFactory germany = new MarketFactory() {
            @Override
            public String market() {
                return "Germany";
            }

            @Override
            public TaxCalculator createTaxCalculator() {
                return new TaxCalculator() {
                    @Override
                    public String label() {
                        return "MwSt";
                    }

                    @Override
                    public double taxOn(double subtotal) {
                        return Math.round(subtotal * 0.19 * 100.0) / 100.0;
                    }
                };
            }

            @Override
            public CurrencyFormatter createCurrencyFormatter() {
                return new CurrencyFormatter() {
                    @Override
                    public String currencyCode() {
                        return "EUR";
                    }

                    @Override
                    public String format(double amount) {
                        return String.format("€%,.2f", amount);
                    }
                };
            }

            @Override
            public AddressValidator createAddressValidator() {
                return new AddressValidator() {
                    @Override
                    public String postcodeLabel() {
                        return "PLZ";
                    }

                    @Override
                    public boolean isValid(String postcode) {
                        return postcode != null && postcode.matches("\\d{5}");
                    }
                };
            }
        };

        // The unchanged client happily works with it.
        Quote quote = new CheckoutService(germany)
                .quote(new Order("ORD-9001", "CUST-DE", 200.00, "10115"));

        assertAll(
                () -> assertEquals("Germany", quote.market()),
                () -> assertEquals("MwSt", quote.taxLabel()),
                () -> assertEquals("€38.00", quote.tax()),
                () -> assertEquals("€238.00", quote.total()));
    }
}
