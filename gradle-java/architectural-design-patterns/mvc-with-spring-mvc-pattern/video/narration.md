# MVC with Spring MVC Pattern — Video Narration Script

## 1. MVC with Spring MVC

Hello, and welcome. This video explains the M V C pattern, in Java, using Spring M V C. This video is presented by Jayasekhar Konduru. First, a simple definition. M V C splits a screen into three roles. A model that works out the numbers. Views that only display them. And a controller that connects the two. In Spring M V C, a controller method returns the name of a view, together with a model. The framework then does the displaying for you. Think of a restaurant menu. The kitchen sets the prices once. The printed menu and the menu on the website just show them. This is the framework version of the M V C video, with the same online store. We will serve one order summary as a web page, and as data for other programs, from one model. Then we will hear what goes wrong when a template does its own sums.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built M V C video. That one splits an order summary into a model that works out the total, views that only show it, and a controller that connects them. It also adds a second view, without touching the model. If you are new to the pattern, watch that one first. Here, we keep the same example, and ask what Spring M V C does with it.

## 3. Before The First Line

Three things are new in this project. Spring Boot. Spring M V C, which is the web part of Spring. And Thymeleaf, a template engine. Here is how they fit together. A controller method returns a view name and a model. Thymeleaf takes the matching template, fills in the model's values, and produces the web page. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. The Controller Names A View

First demo: the controller names a view. A web browser asks for the order. The controller chooses a view, and the model supplies the numbers. The page shows a total of two hundred and ninety-two pounds fifty. And a discount of thirty-two pounds fifty.

## 5. The Same Model, A Second View

Second demo: the same model, a second view. This time, another program asks for the order as data, in a format called JSON. It gets the same model, as data. The total is twenty-nine thousand two hundred and fifty pence, which is the same two hundred and ninety-two pounds fifty. We added one controller method. The model did not change at all.

## 6. Computed Once

Third demo: the total is computed once. Each time the page is viewed, the summary is computed exactly once. And the model does not need a web server to run. Call it on its own, and it gives the same total. That is what makes it so easy to test.

## 7. A Sum In The View

Fourth demo: the shortcut. Someone writes a template that adds up the order lines by itself. It shows three hundred and twenty-five pounds. But the model says two hundred and ninety-two pounds fifty. Why? The template never heard about the discount. Now two places compute a total, and they disagree.

## 8. The Same View, Another Order

Fifth demo: the same template, with a different order. Someone places an order with just one line. The shortcut template was written to add up two named lines. So it fails, with a server error, five hundred. The real view, which only shows what the model gives it, works fine. It shows twelve pounds fifty. A sum written inside a template only works for one shape of data.

## 9. Post, Redirect, Get

Last demo: post, redirect, get. When the customer submits the order form, that is called a post. The server answers with a redirect, to the new order's page. Now, if the customer presses refresh, the browser repeats only the page request. Not the order. So the order cannot be placed twice by accident.

## 10. The Verdict

So, here is the verdict. Compute in the model, once. Let templates only display. Keep the controller thin. And after a form post, answer with a redirect.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for controller methods that take a model, and return the name of a view. And look for templates stored in the resources folder.

## 12. Where You Have Met This

Where have you met this before? In every Spring web page that is built on the server.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one, and Thymeleaf. With a real web server, on a free port.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. A real web server, real web requests, and real templates.

## 15. When This Is Too Much

So, when is this too much? For a service with no web pages at all, a controller that returns data is enough. There is no view to separate.

## 16. Thanks for Watching

That's M V C with Spring M V C. If you remember one sentence, make it this one. Spring M V C does the rendering for you, and the pattern only holds while templates just display. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a plain text view of the order. And keep the model exactly as it is. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
