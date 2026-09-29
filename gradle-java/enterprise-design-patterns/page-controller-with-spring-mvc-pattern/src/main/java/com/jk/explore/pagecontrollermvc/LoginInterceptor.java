package com.jk.explore.pagecontrollermvc;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.HandlerInterceptor;

/**
 * A check that runs before the controllers it is registered for, so no page's author can forget it.
 */
public class LoginInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (request.getHeader("X-Customer") == null) {
            response.setStatus(401);
            response.getWriter().write("please log in");
            return false;
        }
        return true;
    }
}
