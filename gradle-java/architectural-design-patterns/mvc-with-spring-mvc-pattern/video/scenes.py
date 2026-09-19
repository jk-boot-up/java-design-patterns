"""Scene definitions for the MVC with Spring MVC teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='MVC with Spring MVC',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the MVC pattern with '
            'Spring MVC, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] It is the framework version '
            'of the MVC video. That one split an order summary into a '
            'model that works out the total, views that only show it, and '
            'a controller that connects them, and showed a second view '
            'added without touching the model. This one shows the same '
            'idea inside Spring MVC. [[slnc 350]] The plain definition, '
            'in short: in Spring MVC, a controller method returns a view '
            'name and a model, and the framework does the rendering. '
            '[[slnc 300]] By the end you will see an order summary served '
            'as a web page and as JSON from one model, then see what goes '
            'wrong when a template does its own sums.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['MVC, the hand-built video, splits an', 'order summary into a model, views', 'and a controller.', '', 'It adds a second view without', 'touching the model.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the MVC video. If you have not seen it, '
            'start there. It splits an order summary into a model that '
            'works out the total, views that only show it, and a '
            'controller that connects them, and adds a second view '
            'without touching the model. [[slnc 300]] This one uses the '
            'same example. It does not teach the pattern again. It shows '
            'what Spring MVC does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'Spring MVC, and Thymeleaf,', 'a template engine.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring MVC is. Spring '
            'MVC is the web layer of Spring. A controller method returns '
            'a view name and a model, and Thymeleaf turns a template and '
            'the model into a page. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-view', kind='console', title='The Controller Names A View',
        body="""ONE. A view.
  a browser gets HTML.
  Total: £292.50.
  Discount: £32.50.""",
        narration=(
            'First, a browser asks for the order. The controller names a '
            'view, and the model supplies the numbers. The page says: '
            'total, two hundred and ninety two pounds fifty. Discount, '
            'thirty two pounds fifty.'
        ),
    ),
    dict(
        key='05-json', kind='console', title='The Same Model, A Second View',
        body="""TWO. A second view.
  a program gets JSON.
  totalPence: 29250.

  the model did not change.""",
        narration=(
            'Second, another view. A program that asks for JSON gets the '
            'same model as data. Total, twenty nine thousand two hundred '
            'and fifty pence. We added a controller method, and the model '
            'did not change.'
        ),
    ),
    dict(
        key='06-once', kind='console', title='Computed Once',
        body="""THREE. Once.
  summaries computed per page
  view: 1.

  the model, with no server:
  £292.50.""",
        narration=(
            'Third, once. One page view computes the summary once. And '
            'the model needs no server to run. Called on its own, it '
            'gives the same total. That is what makes it easy to test.'
        ),
    ),
    dict(
        key='07-sum', kind='console', title='A Sum In The View',
        body="""FOUR. A sum in the view.
  the shortcut view: 32500.
  the model: 29250.

  the view never heard of the
  discount.""",
        narration=(
            'Fourth, the shortcut. A template adds up the lines itself. '
            'It shows thirty two thousand five hundred. The model says '
            'twenty nine thousand two hundred and fifty. The template '
            'never heard of the discount. [[slnc 300]] Two places now '
            'compute a total, and they disagree.'
        ),
    ),
    dict(
        key='08-shape', kind='console', title='The Same View, Another Order',
        body="""FIVE. Another order.
  a one-line order.
  the shortcut view: 500.
  the real view: 200,
  £12.50.""",
        narration=(
            'Fifth, another order. A one-line order is placed. The '
            'template that adds up two named lines fails with a five '
            'hundred. The real view, which only shows what the model '
            'gives it, works. A sum in a template is written for one '
            'shape of data.'
        ),
    ),
    dict(
        key='09-prg', kind='console', title='Post, Redirect, Get',
        body="""SIX. Redirect.
  the form post answered with
  a redirect.

  a refresh repeats the GET,
  not the order.""",
        narration=(
            'Last, post, redirect, get. The form post answers with a '
            "redirect to the new order's page. If the customer refreshes, "
            'the browser repeats the get, not the post. The order cannot '
            'be placed twice by accident.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Compute in the model, once.', '', 'Templates only display.', '', 'A thin controller.', '', 'Redirect after a post.'],
        narration=(
            'My verdict, plainly. Compute in the model, once. Keep '
            'templates to display. Keep the controller thin. And use a '
            'redirect after a form post.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Controller methods returning', 'a view name.', '', 'Templates under resources.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Controller methods that return a view name and take a model. '
            'And templates in a resources folder.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every server-rendered Spring', 'web page.'],
        narration=(
            'You have met this in every server rendered Spring web page.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1 and', 'Thymeleaf.', '', 'A real web server on a free port.'],
        narration=(
            'For the record. Spring Boot four point one point one and '
            'Thymeleaf. A real web server, on a free port.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real web server,', 'real HTTP and real templates.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real web server, real HTTP and real '
            'templates.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For an API with no pages, a controller', 'that returns data is enough.'],
        narration=(
            'So when is it too much? For an API with no pages, a '
            'controller that returns data is enough, and there is no view '
            'to separate.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a plain text view', 'and keep the model unchanged.'],
        narration=(
            "That's MVC with Spring MVC. [[slnc 250]] If you take one "
            'sentence away, take this one: Spring MVC renders for you, '
            'and the pattern holds only while templates just show. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository. [[slnc '
            '300]] If you try one exercise, add a plain text view, and '
            'keep the model unchanged. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
