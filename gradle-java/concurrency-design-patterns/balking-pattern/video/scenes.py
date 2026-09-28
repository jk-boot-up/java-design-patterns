"""Scene definitions for the Balking teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Balking',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Balking pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Balking means an action only '
            'happens if the object is in the right state. [[slnc 300]] If '
            'it is not, the call returns at once. [[slnc 300]] It does '
            'not wait, and it does not fail. [[slnc 600]] Think of a lift '
            'button. [[slnc 300]] If the lift is already on its way, '
            'pressing the button again does nothing new. [[slnc 700]] In '
            "our online store, a customer's basket draft saves itself "
            'automatically. [[slnc 500]] In this video, one edit will '
            'cause five saves. [[slnc 300]] Then the draft will balk when '
            'nothing changed, and when a save is already running. [[slnc '
            '300]] We will hear an edit lost by a careless version, and '
            'kept by a careful one. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["A customer's basket draft is", 'saved by a timer, and by a Save', 'button.', '', 'Sometimes nothing has changed.', 'Sometimes a save is running.', '', 'What should save do?'],
        narration=(
            "Here is the scenario. [[slnc 400]] A customer's basket draft "
            'is saved in two ways. [[slnc 300]] By a timer, every few '
            'seconds. [[slnc 300]] And by a Save button. [[slnc 500]] '
            'Sometimes nothing has changed since the last save. [[slnc '
            '300]] Sometimes a save is already running. [[slnc 500]] So '
            'here is the question. [[slnc 300]] What should save do then?'
        ),
    ),
    dict(
        key='03-always', kind='console', title='Save Every Time',
        body="""ONE. Every time.
  one edit.
  the timer fires 5 times.
  writes: 5.

  four wrote what was there.""",
        narration=(
            'First, the simple way: save every time you are asked. [[slnc '
            '400]] The customer makes one edit. [[slnc 300]] The autosave '
            'timer fires five times. [[slnc 500]] That is five writes. '
            '[[slnc 300]] And four of them wrote exactly what was already '
            'there.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Check the state at the door.', '', 'If the action is not needed, or', 'not possible now, return at once.', '', 'Do not wait, and do not fail.', '', 'Tell the caller which it was.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Check the state at the door. '
            '[[slnc 300]] If the action is not needed, or not possible '
            'right now, return at once. [[slnc 400]] Do not wait, and do '
            'not fail. [[slnc 300]] And tell the caller which of those it '
            'was.'
        ),
    ),
    dict(
        key='05-clean', kind='console', title='Balk When There Is Nothing To Save',
        body="""TWO. Nothing to save.
  the same 5 calls:
  SAVED, then NOTHING_TO_SAVE
  four times.
  writes: 1.""",
        narration=(
            'Second demo: balk when there is nothing to save. [[slnc '
            '400]] The same five calls. [[slnc 300]] The first saves. '
            '[[slnc 300]] The other four are told: nothing to save. '
            '[[slnc 500]] Just one write. [[slnc 300]] The four that '
            'balked returned at once, and did no work.'
        ),
    ),
    dict(
        key='06-busy', kind='console', title='Balk When A Save Is Already Running',
        body="""THREE. Busy.
  a save is running.
  a second call: ALREADY_SAVING,
  at once, without waiting.

  writes: 1.""",
        narration=(
            'Third demo: balk when a save is already running. [[slnc '
            '400]] A save is in progress, and held in the middle of '
            'writing. [[slnc 300]] A second call arrives. [[slnc 300]] It '
            'is told: already saving, straight away, without waiting. '
            '[[slnc 500]] When the first save finishes, there has been '
            'only one write. [[slnc 300]] The second caller did not queue '
            'behind it.'
        ),
    ),
    dict(
        key='07-edit', kind='console', title='An Edit During A Save',
        body="""FOUR. An edit mid-save.
  2 becomes 3 during a save.
  careless: clean after the
  save, 3 is never saved.

  version counter: still dirty,
  next save writes 3.""",
        narration=(
            'Fourth demo: an edit during a save. [[slnc 400]] While a '
            'save is running, the customer changes a quantity from two to '
            'three. [[slnc 500]] The careless version marks the draft as '
            'clean when the save finishes. [[slnc 300]] So the change is '
            'lost. [[slnc 300]] The draft no longer thinks it has '
            'changes. [[slnc 300]] And the next save says: nothing to '
            'save. [[slnc 500]] The careful version uses a version '
            'counter. [[slnc 300]] It knows a newer change arrived during '
            'the save, so it stays dirty. [[slnc 300]] And the next save '
            'writes the three. [[slnc 500]] Balking is easy to get almost '
            'right.'
        ),
    ),
    dict(
        key='08-told', kind='console', title='The Caller Is Told',
        body="""FIVE. Told.
  nothing edited: NOTHING_TO_SAVE.
  edited: SAVED.

  a balk is an answer, not an
  error. the caller decides.""",
        narration=(
            'Fifth demo: the caller is told what happened. [[slnc 400]] '
            'When nothing was edited, the answer is: nothing to save. '
            '[[slnc 300]] When something was edited, the answer is: '
            'saved. [[slnc 500]] A balk is an answer, not an error. '
            '[[slnc 300]] The caller can retry, ignore it, or tell the '
            'user. [[slnc 300]] And the result says exactly which case '
            'happened.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the customer clicks Save while
  the autosave runs:
  ALREADY_SAVING.
  their click did nothing.

  balking is wrong where every
  request must be honoured.""",
        narration=(
            'Finally, the cost. [[slnc 400]] The customer clicks Save '
            'while the autosave is running. [[slnc 300]] They are told: '
            'already saving. [[slnc 400]] So their click did nothing. '
            '[[slnc 300]] Their latest change is still unsaved, and must '
            'wait for the next save. [[slnc 500]] Balking suits work that '
            'can safely be skipped, and done later. [[slnc 300]] It is '
            'wrong wherever every request must be carried out. [[slnc '
            '300]] Because a request that balks is simply not done.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An early return at the top of a', 'method that checks a state flag.', '', 'isSaving, isRunning or', 'alreadyStarted fields.', '', 'AtomicBoolean.compareAndSet(false,', 'true) guarding a task.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for an early return at the top of a method, '
            'checking a state flag. [[slnc 300]] Look for fields named is '
            'saving, is running, or already started. [[slnc 300]] Look '
            "for an Atomic Boolean's compare-and-set, guarding a task. "
            '[[slnc 300]] And look for scheduled tasks that skip a run if '
            'the last one is still going.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use balking for work that is', 'idempotent or repeatable, where', 'skipping a call is harmless', 'because a later call will catch', 'up: autosave, refresh, a periodic', 'sync. Return a result that says', 'what happened. Track what was', 'saved with a version, not a flag.', 'Do not use it where every request'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use balking for work '
            'that can be repeated safely, where skipping one call is '
            'harmless because a later call will catch up. [[slnc 300]] '
            'Autosave, a screen refresh, or a regular sync. [[slnc 500]] '
            'Return a result that says what happened. [[slnc 300]] Track '
            'what was saved with a version number, not a simple flag. '
            '[[slnc 400]] And do not use it where every request must be '
            'carried out. [[slnc 300]] There, wait, or queue the request '
            'instead.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Where the caller needs the action', 'done, balking silently drops it.', 'Where the state is checked and', 'changed in separate steps without', 'a lock, balking is a race in', 'disguise.'],
        narration=(
            'So, when is this wrong? [[slnc 400]] Where the caller needs '
            'the action done, balking silently drops it. [[slnc 400]] And '
            'where the state is checked and changed in separate steps, '
            'without a lock, balking is a race condition in disguise.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Balking pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Balking returns at '
            'once when the state is wrong, and the price is that the '
            'request it turns away is not done. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Make the Save button wait '
            'for a running save, instead of balking. [[slnc 300]] Then '
            'listen to what changes. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
