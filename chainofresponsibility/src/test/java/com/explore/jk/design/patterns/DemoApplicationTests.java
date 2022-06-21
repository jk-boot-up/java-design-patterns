package com.explore.jk.design.patterns;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.core.env.Environment;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = DemoApplication.class,
webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class DemoApplicationTests {

	@Autowired
	private Environment environment;

	@LocalServerPort
	private int port;

	@Autowired
	private TestRestTemplate testRestTemplate;


	@Test
	void contextLoads() {
		ResponseEntity<String> entity =
				testRestTemplate.getForEntity(
				"http://localhost:" + this.port + "/design-patterns/chain-of-responsibility/v1/numbers/43", String.class);
		Assertions.assertEquals(entity.getStatusCode(), HttpStatus.OK);

	}

}
