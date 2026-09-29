package com.jk.explore.translatorcamel;

import java.util.LinkedHashMap;
import java.util.Map;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.dataformat.JsonLibrary;

/**
 * The routes. The inbox route is the normalizer: it recognises the format from the text and sends
 * the order to direct:translate-&lt;format&gt;. Each translator route ends at the warehouse.
 */
public final class ShopRoutes extends RouteBuilder {

    private final Warehouse warehouse;

    public ShopRoutes(Warehouse warehouse) {
        this.warehouse = warehouse;
    }

    @Override
    public void configure() {
        // The normalizer: recognise the format, then hand over to that format's translator.
        from("direct:inbox").routeId("normalizer")
                .setHeader("format", method(ShopRoutes.class, "formatOf"))
                .toD("direct:translate-${header.format}");

        from("direct:translate-web").routeId("translate-web")
                .process(e -> e.getMessage().setBody(Translators.fromWebForm(form(e.getMessage().getBody(String.class)))))
                .to("direct:warehouse");

        from("direct:translate-csv").routeId("translate-csv")
                .unmarshal().csv()
                .bean(Translators.class, "fromCsv")
                .to("direct:warehouse");

        from("direct:translate-json").routeId("translate-json")
                .unmarshal().json(JsonLibrary.Jackson, Map.class)
                .bean(Translators.class, "fromJson")
                .to("direct:warehouse");

        // The warehouse takes only the canonical order.
        from("direct:warehouse").routeId("warehouse")
                .convertBodyTo(OrderMessage.class)
                .bean(warehouse, "pick");
    }

    /** Marketplace C, added later as one more route: XML read with XPath. */
    public static RouteBuilder xmlTranslator() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from("direct:translate-xml").routeId("translate-xml")
                        .setHeader("id", xpath("/order/@id", String.class))
                        .setHeader("sku", xpath("/order/line/@sku", String.class))
                        .setHeader("qty", xpath("/order/line/@qty", Integer.class))
                        .setHeader("price", xpath("/order/line/@price", Double.class))
                        .process(e -> e.getMessage().setBody(new OrderMessage(e.getMessage().getHeader("id", String.class),
                                e.getMessage().getHeader("sku", String.class), e.getMessage().getHeader("qty", Integer.class),
                                e.getMessage().getHeader("price", Double.class))))
                        .to("direct:warehouse");
            }
        };
    }

    /** Recognises a format from the first character of the text. */
    public static String formatOf(String body) {
        String t = body.strip();
        if (t.startsWith("{")) {
            return "json";
        }
        if (t.startsWith("<")) {
            return "xml";
        }
        return t.contains("=") ? "web" : "csv";
    }

    private static Map<String, String> form(String text) {
        Map<String, String> out = new LinkedHashMap<>();
        for (String pair : text.split("&")) {
            String[] kv = pair.split("=", 2);
            out.put(kv[0], kv[1]);
        }
        return out;
    }
}
