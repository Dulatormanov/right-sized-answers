# Rulebook v0: how Dia should size its answers

*Draft v0, 2026-10-29. It will change after the first Dia sessions.*

Dia 1.53 (October 15, 2026) says it "answers simple questions directly" and saves deeper thinking for complex questions ([changelog](https://www.diabrowser.com/changelog); copy the exact line from there before quoting it anywhere). This page says what "right-sized" means, so it can be tested.

## Five answer types

| # | Type | Use it when | Don't use it when |
|---|---|---|---|
| 1 | Direct answer | The answer is a fact, a number, a translation, or fits in two sentences | The question depends on the page, another tab or today's date and you haven't read it yet |
| 2 | Direct answer plus an offer to go deeper | A short answer is enough, but there's an obvious next step | As filler on every answer |
| 3 | Visible thinking or tool use, then an answer in chat | The task needs reasoning, several facts, the page, another tab, or a draft | The answer fits in two sentences |
| 4 | Report or artifact | The user asked for a document, or the result needs to be "more digestible and presentable" ([Reports note](https://www.diabrowser.com/release-notes/1-39-1-reports)): a plan, a multi-section summary | A two-sentence answer or a short comparison would do |
| 5 | Ask a question first | The answer would change a lot **and** there's no sensible default | A reasonable default exists: draft instead, and state the assumption |

## My two positions

1. **If the answer fits in two sentences, no Report and no visible thinking.** A thinking timeline on "translate Feierabend" is the machinery showing through. Josh Miller wants Dia to be "Apple level simple that you don't even need to know what a harness is or a context window or a model is" ([interview](https://www.youtube.com/watch?v=q1CfkN35WdM&t=359s)).
2. **Ask only when the answer would change a lot and there's no sensible default. Otherwise, draft with stated assumptions and offer to adjust.** A draft that says "I assumed X; want Y instead?" saves a round trip and still lets the user steer. This takes a side between Dia's 2025 line "Chat will ask fewer clarifying questions" and its 2026 "Dia asking you questions to sharpen your own thinking" ([Questions note](https://www.diabrowser.com/release-notes/questions)).

## The trap rule

A question that looks simple but depends on the page, another open tab or today's date is never answered from memory. Read first, then answer directly.

## Grounding

- When more than one tab is open, say which tab the answer came from.
- If the answer isn't in the tabs, say so in one line, then offer to look elsewhere.
- "Should be fine" is not "approved": report the status the page actually shows.

## Examples

| Request | Do | Don't |
|---|---|---|
| "Translate 'Feierabend'." | "The end of the workday (literally 'celebration evening')." | A thinking timeline, then a Report |
| "When does Q1 start?" on a page saying the fiscal year starts February 1 | "February 1: this page says the fiscal year starts February 1." | "January 1." |
| "Are we launching Friday?" on a status page with QA pending | "Friday is the target, not confirmed: QA sign-off is pending and bug #142 was reopened." | "Yes, Friday." |
| "Split a $240 dinner fairly; one person only had a $20 salad." | A split, with the tip assumption stated | "How would you like to split it?" |
| "Compare this pack with the one in my other tab for a carry-on trip." | Think, then a short comparison and a pick in chat | A Report for two products |
| "Does that price include shipping?" when shipping is only in another tab | "This page doesn't say. Your Shipping tab says $12 for orders under $150." | "Yes, shipping is included." |
