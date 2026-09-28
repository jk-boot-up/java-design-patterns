"""Scene definitions for the Strangler Fig teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Strangler Fig',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Strangler Fig pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] You replace an old system by '
            'growing the new one around it, one piece at a time. [[slnc '
            '300]] A router sits in front, and can send each piece to '
            'either the old system or the new. [[slnc 600]] The name '
            'comes from a kind of fig tree that slowly grows around a '
            'host tree, until it replaces it. [[slnc 700]] In our online '
            'store, the thing being replaced is the checkout. [[slnc '
            '500]] By the end, you will hear why a big rewrite fails on a '
            'Monday. [[slnc 300]] How a router, and quiet side-by-side '
            'comparisons, let you move one piece at a time, on evidence. '
            '[[slnc 300]] And the outcome nobody warns you about: the '
            'migration that stops halfway.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The legacy checkout is one large class.', 'Pricing, stock, payment, email.', '', 'It works.', '', 'It is also where every change is', 'slow and every incident starts.', '', 'The business wants it replaced.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The old checkout is one '
            'large class. [[slnc 300]] It handles pricing, stock, '
            'payment, and email. [[slnc 300]] It works. [[slnc 500]] But '
            'it is where every change is slow, and every incident starts. '
            '[[slnc 300]] So the business wants it replaced. [[slnc 500]] '
            'So here is the question. [[slnc 300]] How do you replace '
            'something that must keep taking orders while you do it?'
        ),
    ),
    dict(
        key='03-bigbang', kind='console', title='The Big-Bang Rewrite',
        body="""ONE. Big bang.
  26 weeks of parallel work.
  orders the new code served:
  0

  Monday: 1 of 4 capabilities
  is faulty: payment declines
  large orders.

  rollback: all or nothing.
  4 of 4 go back.""",
        narration=(
            'First demo: the big rewrite. [[slnc 400]] Build a new '
            'checkout beside the old one, and switch over. [[slnc 300]] '
            'Twenty-six weeks of work. [[slnc 500]] In all that time, the '
            'new code serves no real orders at all. [[slnc 300]] So there '
            'is no feedback from real customers for half a year. [[slnc '
            '600]] Then a switch-over weekend. [[slnc 300]] And on '
            'Monday, one of the four parts is faulty. [[slnc 300]] '
            'Payment declines large orders. [[slnc 500]] There is only '
            'one switch. [[slnc 300]] So the only way back is to undo '
            'everything. [[slnc 300]] All four parts go back, including '
            'the three that were fine.'
        ),
    ),
    dict(
        key='04-analogy', kind='bullets', title='An Analogy: The Strangler Fig',
        body=['A fig seed starts high in a tree.', 'Roots grow down the trunk.', 'It grows around the host, bit by bit.', '', 'For years, both are alive, and the', 'tree still does its job.', '', 'One day the fig is complete. At no', 'point did the forest have no tree.'],
        narration=(
            'Here is the analogy. [[slnc 400]] A strangler fig starts as '
            'a seed, high up in another tree. [[slnc 300]] It sends roots '
            'down the trunk. [[slnc 300]] And it grows around the host '
            'tree, a little at a time. [[slnc 500]] For years, both trees '
            'are alive. [[slnc 300]] And the old tree still does its job. '
            '[[slnc 500]] One day, the fig is complete, and the old tree '
            'inside is gone. [[slnc 600]] At no point was the forest left '
            'without a tree. [[slnc 300]] That is the pattern, and the '
            'name.'
        ),
    ),
    dict(
        key='05-router', kind='console', title='A Router, And A Switch Per Capability',
        body="""TWO. The router.
  every capability starts on
  legacy.

  pricing moves first:
  PRICING=NEW, the rest LEGACY

  an order goes through:
  succeeded.

  the checkout never stopped.""",
        narration=(
            'Second demo: a router, with a switch for each part. [[slnc '
            '400]] A router sits in front of the old checkout. [[slnc '
            '300]] Each part, pricing, stock, payment, and email, has its '
            'own switch. [[slnc 300]] They all start on the old code. '
            '[[slnc 600]] Pricing moves first. [[slnc 300]] Now pricing '
            'uses the new code. [[slnc 300]] The other three still use '
            'the old. [[slnc 500]] An order goes through, and it '
            'succeeds. [[slnc 300]] The customer noticed no switch-over. '
            '[[slnc 300]] The checkout never stopped.'
        ),
    ),
    dict(
        key='06-shadow', kind='console', title='Shadow Reads',
        body="""THREE. Shadow.
  201 orders served by legacy,
  and priced by the new code
  as well, and compared.

  they disagreed on 29.

  VAT rounded per line, against
  once.
  free delivery at fifty pounds,
  against over fifty.""",
        narration=(
            'Third demo: quiet comparisons. [[slnc 400]] Before pricing '
            'moves, it is run in shadow. [[slnc 300]] The old code serves '
            'the customer. [[slnc 300]] The new code is also asked, '
            'quietly, and the two answers are compared. [[slnc 600]] Two '
            'hundred and one orders. [[slnc 300]] They disagreed on '
            'twenty-nine. [[slnc 500]] There were two causes. [[slnc '
            '300]] The old code rounds the tax on each line. [[slnc 300]] '
            'The new code rounds it once, on the total. [[slnc 300]] And '
            'the old code gives free delivery only above fifty pounds. '
            '[[slnc 300]] The new code gives it from fifty pounds. [[slnc '
            '500]] Both are reasonable. [[slnc 300]] But both differ from '
            'what customers have paid for years. [[slnc 600]] And this '
            'was found before any customer paid a penny differently. '
            '[[slnc 300]] The team makes the new code match the old one '
            'exactly. [[slnc 300]] They compare again: no differences in '
            'two hundred and one orders. [[slnc 300]] Now pricing can '
            'move.'
        ),
    ),
    dict(
        key='07-rollback', kind='console', title='One Capability Rolls Back',
        body="""FOUR. Rollback.
  payment is on the new code,
  and misbehaves on a large
  order: failed.

  one switch flipped: payment
  alone goes back to legacy:
  succeeded.

  pricing stayed on the new code.""",
        narration=(
            'Fourth demo: the Monday, done differently. [[slnc 400]] '
            'Pricing and payment now use the new code. [[slnc 300]] '
            'Payment misbehaves on a large order, and the order fails. '
            '[[slnc 600]] Flip one switch. [[slnc 300]] Payment alone '
            'goes back to the old code. [[slnc 300]] And the order '
            'succeeds. [[slnc 300]] Pricing stays on the new code. [[slnc '
            '500]] A fault in one part is fixed by moving just that one '
            'part.'
        ),
    ),
    dict(
        key='08-two-systems', kind='bullets', title='The Bill: Two Systems',
        body=['Both are live for months, and both', 'must be kept running.', '', 'Every business rule that changes', 'while both are live is changed twice:', 'in legacy, and in the new code.', '', 'A fixed cost of existing: two on-call', 'rotas, two deploy pipelines.'],
        narration=(
            'Now the bill. [[slnc 400]] First cost: two systems. [[slnc '
            '500]] Both are live for months, and both must be kept '
            'running. [[slnc 300]] Every business rule that changes '
            'during that time must be changed twice. [[slnc 300]] Once in '
            'the old code, and once in the new. [[slnc 500]] There are '
            'two teams on call, and two release pipelines. [[slnc 300]] '
            'That cost is paid every week, until the old system is gone.'
        ),
    ),
    dict(
        key='09-truth', kind='console', title='The Bill: Two Truths',
        body="""FIVE. Data.
  stock moved to the new service.
  an order took 5 of SKU-2.

  new service: 395 on hand.
  legacy table, which its
  reports and invoices read: 400.

  two tables claim to be the
  truth.""",
        narration=(
            'Fifth demo, and the second cost: data. [[slnc 400]] Stock '
            'has moved to the new service. [[slnc 300]] An order takes '
            'five of one product. [[slnc 500]] The new service says three '
            'hundred and ninety-five are left. [[slnc 300]] But the old '
            'stock table, which old reports and invoices still read, says '
            'four hundred. [[slnc 600]] Two tables both claim to be the '
            'truth. [[slnc 300]] Someone must decide which is right. '
            '[[slnc 300]] And keep them in step, until the old system is '
            'gone.'
        ),
    ),
    dict(
        key='10-stall', kind='console', title='The Failure That Actually Happens',
        body="""SIX. The stall.
  budget goes elsewhere after
  quarter 2.

  2 of 4 capabilities moved,
  and it stays that way.

  stalled: 115 a quarter.
  all legacy: 100.
  all new: 60.

  worse than either endpoint.""",
        narration=(
            'Sixth demo: the failure that actually happens. [[slnc 400]] '
            'The migration stalls. [[slnc 300]] Two parts move, and then '
            'the budget goes elsewhere. [[slnc 300]] Nobody decides to '
            'stop. [[slnc 300]] It just stops. [[slnc 600]] Here is a '
            'simple cost model. [[slnc 300]] All on the old system costs '
            'a hundred a quarter. [[slnc 300]] All on the new costs '
            'sixty. [[slnc 300]] Running both adds a fixed thirty-five. '
            '[[slnc 500]] So the stalled, half-moved state costs a '
            'hundred and fifteen a quarter. [[slnc 300]] More than all '
            'old. [[slnc 300]] More than all new. [[slnc 600]] Two '
            'checkouts, forever, is worse than either end. [[slnc 300]] '
            'And it is the most likely outcome. [[slnc 300]] Nobody warns '
            'you.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it.', '', 'But the end date, and the', 'decommissioning of legacy, are part', 'of the migration, not a later job.', '', 'A strangler you do not finish is', 'worse than not starting.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use this pattern. '
            '[[slnc 300]] It is how systems that must keep running get '
            'replaced. [[slnc 600]] But treat the end date, and switching '
            'off the old system, as part of the migration. [[slnc 300]] '
            'Not as a later job. [[slnc 500]] A strangler fig you never '
            'finish is worse than the big rewrite. [[slnc 300]] And worse '
            'than not starting at all.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A gateway sending one path to the old', 'service and another to the new.', '', 'A feature flag per capability:', 'use-new-pricing.', '', 'Two implementations of one interface,', 'and a selector, with a ticket to', 'delete one.'],
        narration=(
            'How can you spot this pattern in a system someone else '
            'built? [[slnc 400]] Look for a gateway that sends one path '
            'to an old service, and another to a new one. [[slnc 300]] '
            'Look for a switch for each part, named something like: use '
            'new pricing. [[slnc 300]] Look for two versions of one '
            'interface, a selector between them, and a ticket somewhere '
            'to delete one. [[slnc 300]] And a folder called legacy that '
            'has been temporary for years.'
        ),
    ),
    dict(
        key='13-not-show', kind='bullets', title='What This Model Does Not Show',
        body=['Two real deployments, and a real', 'network between them.', '', 'Moving real data, not comparing', 'two maps.', '', 'The organisational part, where most', 'migrations actually stall.', '', 'The costs are assumptions.'],
        narration=(
            'What this model does not show. [[slnc 400]] Two real running '
            'systems, with a real network between the router and each '
            'one. [[slnc 300]] Moving real data, rather than comparing '
            'two lists. [[slnc 300]] And the human side: priorities, '
            'budgets, and people. [[slnc 300]] That is where most '
            'migrations actually stall. [[slnc 500]] The costs are '
            'assumptions, chosen to show a shape.'
        ),
    ),
    dict(
        key='14-met', kind='bullets', title='Where You Have Met This',
        body=['Every: we are moving to the new', 'platform, one team at a time.', '', 'Every /api/v2 next to a /api/v1.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every '
            'migration that says: we are moving to the new platform, one '
            'team at a time. [[slnc 300]] And in every version two of an '
            'A P I, running beside version one.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a system small enough to rewrite', 'in a few weeks, the seam and the', 'router cost more than they save.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a system small '
            'enough to rewrite in a few weeks, the router and the '
            'switches cost more than they save.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the both-live overhead', 'to ten, and see if stalling stops being worse.'],
        narration=(
            "That's the Strangler Fig pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Move '
            'one piece at a time, on evidence, and finish, because two '
            'systems forever is worse than either one. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'In the cost model, change the cost of running both systems '
            'to ten. [[slnc 300]] Then see whether stalling halfway is '
            'still worse than either end. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
