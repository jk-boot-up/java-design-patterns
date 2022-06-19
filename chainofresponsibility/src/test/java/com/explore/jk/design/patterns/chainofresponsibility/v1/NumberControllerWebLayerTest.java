package com.explore.jk.design.patterns.chainofresponsibility.v1;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.result.ContentResultMatchers;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.doAnswer;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(SpringExtension.class)
@WebMvcTest(controllers = NumberController.class)
public class NumberControllerWebLayerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private NumberController numberController;

    @MockBean
    @Qualifier("negativeNumberHandler")
    private IHandler negativeNumberHandler;

    @Test
    public void responseFromNumberController() throws Exception {
        assertEquals(numberController.getHandler(), negativeNumberHandler);
        String responseString = String.format("Number is positive: %d", 10);
        doAnswer(invocation -> {
            // just placeholder for request
            Request request = (Request) invocation.getArgument(0);
            Response response = (Response) invocation.getArgument(1);
            response.setResponse(responseString);
            return null;
        }).when(negativeNumberHandler).handleRequest(Mockito.any(Request.class), Mockito.any(Response.class));
        ResultActions resultActions = this.mockMvc.perform(get("/design-patterns/chain-of-responsibility/v1/numbers/10"));
        resultActions.andDo(MockMvcResultHandlers.print());
        resultActions.andExpect(MockMvcResultMatchers.status().isOk());
        resultActions.andExpect(content().json("{\"response\":\"Number is positive: 10\"}"));
        resultActions.andExpect(content().contentType(MediaType.APPLICATION_JSON));
        MvcResult mvcResult = resultActions.andReturn();
        assertEquals(200, mvcResult.getResponse().getStatus());
    }

}
