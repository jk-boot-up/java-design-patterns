"""Scene definitions for the MVC with Spring MVC teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='MVC with Spring MVC',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the M V '
            'C pattern, in Java, using Spring M V C. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] M V C splits a '
            'screen into three roles. [[slnc 300]] A model that works out '
            'the numbers. [[slnc 200]] Views that only display them. '
            '[[slnc 200]] And a controller that connects the two. [[slnc '
            '500]] In Spring M V C, a controller method returns the name '
            'of a view, together with a model. [[slnc 300]] The framework '
            'then does the displaying for you. [[slnc 600]] Think of a '
            'restaurant menu. [[slnc 300]] The kitchen sets the prices '
            'once. [[slnc 300]] The printed menu and the menu on the '
            'website just show them. [[slnc 700]] This is the framework '
            'version of the M V C video, with the same online store. '
            '[[slnc 400]] We will serve one order summary as a web page, '
            'and as data for other programs, from one model. [[slnc 300]] '
            'Then we will hear what goes wrong when a template does its '
            'own sums.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['MVC, the hand-built video, splits an', 'order summary into a model, views', 'and a controller.', '', 'It adds a second view without', 'touching the model.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built M V C video. [[slnc 400]] That one '
            'splits an order summary into a model that works out the '
            'total, views that only show it, and a controller that '
            'connects them. [[slnc 300]] It also adds a second view, '
            'without touching the model. [[slnc 500]] If you are new to '
            'the pattern, watch that one first. [[slnc 400]] Here, we '
            'keep the same example, and ask what Spring M V C does with '
            'it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'Spring MVC, and Thymeleaf,', 'a template engine.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] Spring '
            'Boot. [[slnc 200]] Spring M V C, which is the web part of '
            'Spring. [[slnc 200]] And Thymeleaf, a template engine. '
            '[[slnc 500]] Here is how they fit together. [[slnc 300]] A '
            'controller method returns a view name and a model. [[slnc '
            '300]] Thymeleaf takes the matching template, fills in the '
            "model's values, and produces the web page. [[slnc 500]] And "
            'one promise. [[slnc 300]] If you skip this video, you lose '
            'none of the pattern. [[slnc 300]] This one is about the '
            'tool.'
        ),
    ),
    dict(
        key='04-view', kind='console', title='The Controller Names A View',
        body="""ONE. A view.
  a browser gets HTML.
  Total: £292.50.
  Discount: £32.50.""",
        narration=(
            'First demo: the controller names a view. [[slnc 400]] A web '
            'browser asks for the order. [[slnc 300]] The controller '
            'chooses a view, and the model supplies the numbers. [[slnc '
            '500]] The page shows a total of two hundred and ninety-two '
            'pounds fifty. [[slnc 300]] And a discount of thirty-two '
            'pounds fifty.'
        ),
    ),
    dict(
        key='05-json', kind='console', title='The Same Model, A Second View',
        body="""TWO. A second view.
  a program gets JSON.
  totalPence: 29250.

  the model did not change.""",
        narration=(
            'Second demo: the same model, a second view. [[slnc 400]] '
            'This time, another program asks for the order as data, in a '
            'format called JSON. [[slnc 400]] It gets the same model, as '
            'data. [[slnc 300]] The total is twenty-nine thousand two '
            'hundred and fifty pence, which is the same two hundred and '
            'ninety-two pounds fifty. [[slnc 500]] We added one '
            'controller method. [[slnc 300]] The model did not change at '
            'all.'
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
            'Third demo: the total is computed once. [[slnc 400]] Each '
            'time the page is viewed, the summary is computed exactly '
            'once. [[slnc 500]] And the model does not need a web server '
            'to run. [[slnc 300]] Call it on its own, and it gives the '
            'same total. [[slnc 300]] That is what makes it so easy to '
            'test.'
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
            'Fourth demo: the shortcut. [[slnc 400]] Someone writes a '
            'template that adds up the order lines by itself. [[slnc '
            '500]] It shows three hundred and twenty-five pounds. [[slnc '
            '300]] But the model says two hundred and ninety-two pounds '
            'fifty. [[slnc 500]] Why? [[slnc 300]] The template never '
            'heard about the discount. [[slnc 400]] Now two places '
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
            'Fifth demo: the same template, with a different order. '
            '[[slnc 400]] Someone places an order with just one line. '
            '[[slnc 500]] The shortcut template was written to add up two '
            'named lines. [[slnc 300]] So it fails, with a server error, '
            'five hundred. [[slnc 500]] The real view, which only shows '
            'what the model gives it, works fine. [[slnc 300]] It shows '
            'twelve pounds fifty. [[slnc 500]] A sum written inside a '
            'template only works for one shape of data.'
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
            'Last demo: post, redirect, get. [[slnc 400]] When the '
            'customer submits the order form, that is called a post. '
            '[[slnc 300]] The server answers with a redirect, to the new '
            "order's page. [[slnc 500]] Now, if the customer presses "
            'refresh, the browser repeats only the page request. [[slnc '
            '300]] Not the order. [[slnc 400]] So the order cannot be '
            'placed twice by accident.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Compute in the model, once.', '', 'Templates only display.', '', 'A thin controller.', '', 'Redirect after a post.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Compute in the model, '
            'once. [[slnc 300]] Let templates only display. [[slnc 300]] '
            'Keep the controller thin. [[slnc 300]] And after a form '
            'post, answer with a redirect.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Controller methods returning', 'a view name.', '', 'Templates under resources.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for controller methods that take a model, and '
            'return the name of a view. [[slnc 300]] And look for '
            'templates stored in the resources folder.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every server-rendered Spring', 'web page.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every Spring '
            'web page that is built on the server.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1 and', 'Thymeleaf.', '', 'A real web server on a free port.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one, and Thymeleaf. [[slnc 300]] '
            'With a real web server, on a free port.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real web server,', 'real HTTP and real templates.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] A real web server, '
            'real web requests, and real templates.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For an API with no pages, a controller', 'that returns data is enough.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a service with '
            'no web pages at all, a controller that returns data is '
            'enough. [[slnc 300]] There is no view to separate.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a plain text view', 'and keep the model unchanged.'],
        narration=(
            "That's M V C with Spring M V C. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Spring M V C '
            'does the rendering for you, and the pattern only holds while '
            'templates just display. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a plain text view of the order. [[slnc '
            '300]] And keep the model exactly as it is. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
