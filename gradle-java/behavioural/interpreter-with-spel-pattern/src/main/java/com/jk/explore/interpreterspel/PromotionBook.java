package com.jk.explore.interpreterspel;

import org.springframework.expression.EvaluationContext;
import org.springframework.expression.Expression;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.SimpleEvaluationContext;
import org.springframework.expression.spel.support.StandardEvaluationContext;

import java.util.ArrayList;
import java.util.List;

/**
 * Promotions written as text, one per line: {@code CODE | percent | rule}. Spring's expression
 * language is the interpreter: each rule is parsed once, when the book is built, into a tree that
 * can be evaluated against any number of orders.
 */
public class PromotionBook {

    private record Promotion(String code, int percent, String text, Expression rule) {
    }

    private final SpelExpressionParser parser = new SpelExpressionParser();
    private final List<Promotion> promotions = new ArrayList<>();
    private final boolean trusted;

    /** @param trusted true for the full evaluation context, false for the read-only one */
    public PromotionBook(boolean trusted, String... lines) {
        this.trusted = trusted;
        for (String line : lines) {
            String[] parts = line.split("\\|", 3);
            String text = parts[2].trim();
            promotions.add(new Promotion(parts[0].trim(), Integer.parseInt(parts[1].trim()), text, parser.parseExpression(text)));
        }
    }

    public List<String> applicableTo(Order order) {
        EvaluationContext context = trusted
                ? new StandardEvaluationContext(order)
                : SimpleEvaluationContext.forReadOnlyDataBinding().withRootObject(order).build();
        List<String> codes = new ArrayList<>();
        for (Promotion promotion : promotions) {
            if (Boolean.TRUE.equals(promotion.rule().getValue(context, Boolean.class))) {
                codes.add(promotion.code() + " (" + promotion.percent() + "% off)");
            }
        }
        return codes;
    }
}
