"""Scene definitions for the Strangler Fig teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Strangler Fig',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Strangler Fig '
            'pattern, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'replace a system by growing the new one around the old, one '
            'piece at a time, behind a router that can send each piece to '
            'either. [[slnc 350]] This is the last project in the '
            'platform category, whose subject is the shape of a system as '
            'it changes over time. In our online store, the thing being '
            'replaced is the checkout. [[slnc 300]] By the end you will '
            'see why the big rewrite fails on a Monday, how a router and '
            'shadow reads let you move a piece at a time on evidence, and '
            'the outcome that nobody warns you about: the migration that '
            'stalls half finished.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The legacy checkout is one large class.', 'Pricing, stock, payment, email.', '', 'It works.', '', 'It is also where every change is', 'slow and every incident starts.', '', 'The business wants it replaced.'],
        narration=(
            'Here is the scenario. The legacy checkout is one large '
            'class. It does pricing, stock, payment, and email. It works. '
            '[[slnc 300]] It is also where every change is slow, and '
            'every incident starts. So the business wants it replaced. '
            'The question: how do you replace something that must keep '
            'taking orders while you do it?'
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
            'The obvious answer is a rewrite. Build the new checkout '
            'beside the old one, and switch over. Twenty-six weeks of '
            'work, in parallel with production. In that time, the new '
            'code serves no real orders at all, so there is no feedback '
            'from real traffic for half a year. [[slnc 300]] Then a '
            'cutover weekend. And on Monday, one of the four capabilities '
            'is faulty: payment declines large orders. [[slnc 300]] There '
            'is one switch, so the only rollback is all of it. All four '
            'capabilities go back, including the three that were fine.'
        ),
    ),
    dict(
        key='04-analogy', kind='bullets', title='An Analogy: The Strangler Fig',
        body=['A fig seed starts high in a tree.', 'Roots grow down the trunk.', 'It grows around the host, bit by bit.', '', 'For years, both are alive, and the', 'tree still does its job.', '', 'One day the fig is complete. At no', 'point did the forest have no tree.'],
        narration=(
            'An analogy. A strangler fig begins as a seed, high in a '
            'tree. It sends roots down the trunk, and grows around the '
            'host, a little at a time. For years, both are alive, and the '
            'old tree is still doing its job. One day the fig is '
            'complete, and the tree inside it is gone. [[slnc 300]] At no '
            'point in all that time did the forest have no tree. That is '
            'the pattern, and the name.'
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
            'The pattern. Put a router in front of the legacy checkout. '
            'Every capability, pricing, stock, payment, email, has its '
            'own switch. They all start on legacy. [[slnc 300]] Move '
            'pricing first. Now pricing is served by the new code, and '
            'the other three still by legacy. An order goes through, and '
            'it succeeds. The customer saw no cutover. The checkout never '
            'stopped.'
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
            'Before pricing moves, shadow it. Legacy serves the customer. '
            'The new code is called as well, and the two answers are '
            'compared. Two hundred and one orders. They disagreed on '
            'twenty-nine. [[slnc 300]] Two causes. Legacy rounds the V A '
            'T on each line. The new code rounds it once, on the total. '
            'And legacy gives free delivery only when the goods cost more '
            'than fifty pounds. The new code gives it from fifty pounds. '
            'Both are reasonable. Both differ from what customers have '
            'paid for years. [[slnc 300]] Found before any customer paid '
            'a penny differently. The team decides to reproduce legacy '
            'exactly, and shadows again: zero differences in two hundred '
            'and one. Now pricing can move.'
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
            'Now the Monday, done differently. Pricing and payment are on '
            'the new code. Payment misbehaves on a large order, and the '
            'order fails. [[slnc 300]] Flip one switch. Payment alone '
            'goes back to legacy, and the order succeeds. Pricing never '
            'moved back. A fault in one capability is answered by moving '
            'one capability.'
        ),
    ),
    dict(
        key='08-two-systems', kind='bullets', title='The Bill: Two Systems',
        body=['Both are live for months, and both', 'must be kept running.', '', 'Every business rule that changes', 'while both are live is changed twice:', 'in legacy, and in the new code.', '', 'A fixed cost of existing: two on-call', 'rotas, two deploy pipelines.'],
        narration=(
            'Now the bill. First, two systems are live for months, and '
            'both must be maintained. Every business rule that changes '
            'while both are live is changed twice: in legacy, and in the '
            'new code. There are two on-call rotas, two deployment '
            'pipelines. That is a cost, and it is paid every week until '
            'legacy is gone.'
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
            'Second cost. Data. Stock has moved to the new service, and '
            'an order takes five of one product. The new service says '
            'three hundred and ninety-five on hand. The legacy table, '
            'which its reports and its invoices still read, says four '
            'hundred. [[slnc 300]] Two tables claim to be the truth. '
            'Someone must decide which, and keep them in step until '
            'legacy is gone.'
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
            'And the failure that actually happens in the field. The '
            'migration stalls. Two capabilities move, and then the budget '
            'goes elsewhere. Nobody decides to stop. It just stops. '
            '[[slnc 300]] Here is a cost model, and it is a model, stated '
            'as one. All legacy costs a hundred a quarter. All new costs '
            'sixty. While both are live, there is a fixed extra '
            'thirty-five for running two. The stalled state costs a '
            'hundred and fifteen a quarter. More than all legacy. More '
            'than all new. [[slnc 300]] Two checkouts, forever, is worse '
            'than either endpoint. And it is the most likely outcome, and '
            'nobody warns you.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it.', '', 'But the end date, and the', 'decommissioning of legacy, are part', 'of the migration, not a later job.', '', 'A strangler you do not finish is', 'worse than not starting.'],
        narration=(
            'My verdict, plainly. Use it. It is how systems that must '
            'keep running get replaced. But treat the end date, and the '
            'decommissioning of legacy, as part of the migration, not a '
            'later job. A strangler you do not finish is worse than the '
            'big bang you should have avoided, and worse than not '
            'starting at all.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A gateway sending one path to the old', 'service and another to the new.', '', 'A feature flag per capability:', 'use-new-pricing.', '', 'Two implementations of one interface,', 'and a selector, with a ticket to', 'delete one.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'gateway with routes, sending one path to an old service, and '
            'another to a new one. A feature flag for each capability, '
            'with a name like use new pricing. Two implementations of one '
            'interface, a selector between them, and a ticket, somewhere, '
            'to delete one. And a package called legacy that has been '
            'temporary for years.'
        ),
    ),
    dict(
        key='13-not-show', kind='bullets', title='What This Model Does Not Show',
        body=['Two real deployments, and a real', 'network between them.', '', 'Moving real data, not comparing', 'two maps.', '', 'The organisational part, where most', 'migrations actually stall.', '', 'The costs are assumptions.'],
        narration=(
            'What this model does not show. Two real deployments, and a '
            'real network between the router and the systems. Moving real '
            'data, rather than comparing two maps. And the organisational '
            'part, priorities, budgets, and people, which is where most '
            'of these migrations actually stall. The costs are '
            'assumptions, chosen to show a shape.'
        ),
    ),
    dict(
        key='14-met', kind='bullets', title='Where You Have Met This',
        body=['Every: we are moving to the new', 'platform, one team at a time.', '', 'Every /api/v2 next to a /api/v1.'],
        narration=(
            'You have met this in every migration that says we are moving '
            'to the new platform, one team at a time. And in every slash '
            'A P I slash v two, running next to a slash v one.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a system small enough to rewrite', 'in a few weeks, the seam and the', 'router cost more than they save.'],
        narration=(
            'So when is it too much? For a system small enough to rewrite '
            'in a few weeks, the seam and the router cost more than they '
            'save.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the both-live overhead', 'to ten, and see if stalling stops being worse.'],
        narration=(
            "That's the Strangler Fig. [[slnc 250]] If you take one "
            'sentence away, take this one: move one piece at a time, on '
            'evidence, and finish, because two systems forever is worse '
            'than either. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'change the both-live overhead in the cost model to ten, and '
            'see whether stalling stops being worse than the endpoints. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
