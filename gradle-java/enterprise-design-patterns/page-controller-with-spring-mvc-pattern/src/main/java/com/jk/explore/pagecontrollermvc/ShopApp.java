package com.jk.explore.pagecontrollermvc;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * The shop's web application. With shop.login-interceptor=true, the login check is registered once
 * for every page that needs it.
 */
@SpringBootApplication
public class ShopApp implements WebMvcConfigurer {

    @Value("${shop.login-interceptor:false}")
    private boolean loginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        if (loginInterceptor) {
            registry.addInterceptor(new LoginInterceptor()).addPathPatterns("/basket", "/checkout");
        }
    }
}
