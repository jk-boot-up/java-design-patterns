# MVC with Spring MVC Pattern — Video Narration Script

## 1. MVC with Spring MVC

Hello, and welcome. This video explains the MVC pattern with Spring MVC, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the MVC video. That one split an order summary into a model that works out the total, views that only show it, and a controller that connects them, and showed a second view added without touching the model. This one shows the same idea inside Spring MVC. The plain definition, in short: in Spring MVC, a controller method returns a view name and a model, and the framework does the rendering. By the end you will see an order summary served as a web page and as JSON from one model, then see what goes wrong when a template does its own sums.

## 2. The Partner Project

This video assumes the MVC video. If you have not seen it, start there. It splits an order summary into a model that works out the total, views that only show it, and a controller that connects them, and adds a second view without touching the model. This one uses the same example. It does not teach the pattern again. It shows what Spring MVC does with it.

## 3. Before The First Line

Before the first line of code, what Spring MVC is. Spring MVC is the web layer of Spring. A controller method returns a view name and a model, and Thymeleaf turns a template and the model into a page. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. The Controller Names A View

First, a browser asks for the order. The controller names a view, and the model supplies the numbers. The page says: total, two hundred and ninety two pounds fifty. Discount, thirty two pounds fifty.

## 5. The Same Model, A Second View

Second, another view. A program that asks for JSON gets the same model as data. Total, twenty nine thousand two hundred and fifty pence. We added a controller method, and the model did not change.

## 6. Computed Once

Third, once. One page view computes the summary once. And the model needs no server to run. Called on its own, it gives the same total. That is what makes it easy to test.

## 7. A Sum In The View

Fourth, the shortcut. A template adds up the lines itself. It shows thirty two thousand five hundred. The model says twenty nine thousand two hundred and fifty. The template never heard of the discount. Two places now compute a total, and they disagree.

## 8. The Same View, Another Order

Fifth, another order. A one-line order is placed. The template that adds up two named lines fails with a five hundred. The real view, which only shows what the model gives it, works. A sum in a template is written for one shape of data.

## 9. Post, Redirect, Get

Last, post, redirect, get. The form post answers with a redirect to the new order's page. If the customer refreshes, the browser repeats the get, not the post. The order cannot be placed twice by accident.

## 10. The Verdict

My verdict, plainly. Compute in the model, once. Keep templates to display. Keep the controller thin. And use a redirect after a form post.

## 11. How To Recognise It

How do you recognise this in code you did not write? Controller methods that return a view name and take a model. And templates in a resources folder.

## 12. Where You Have Met This

You have met this in every server rendered Spring web page.

## 13. What Was Used

For the record. Spring Boot four point one point one and Thymeleaf. A real web server, on a free port.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real web server, real HTTP and real templates.

## 15. When This Is Too Much

So when is it too much? For an API with no pages, a controller that returns data is enough, and there is no view to separate.

## 16. Thanks for Watching

That's MVC with Spring MVC. If you take one sentence away, take this one: Spring MVC renders for you, and the pattern holds only while templates just show. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a plain text view, and keep the model unchanged. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
