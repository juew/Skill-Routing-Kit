# Launch Checklist

## Before Posting

- [ ] GitHub repo has topics.
- [ ] README first screen explains the problem in under 30 seconds.
- [ ] CI badge is visible and passing.
- [ ] `v0.1.0` GitHub Release is published.
- [ ] Demo GIF is recorded or at least terminal output is ready.
- [ ] GitHub Discussion is open for missed-routing cases.
- [ ] `docs/demo.md` and `docs/promotion-kit.md` are linked from README.

## Day 1

- [ ] Publish GitHub Release.
- [ ] Post on V2EX.
- [ ] Post on Juejin.
- [ ] Share X thread.
- [ ] Ask 3-5 relevant builders for feedback, not stars.

## Day 2

- [ ] Post Show HN.
- [ ] Post to r/opensource.
- [ ] Reply to comments with examples, not defensiveness.
- [ ] Add good questions to README or FAQ.

## Day 3-5

- [ ] Post to r/ChatGPTCoding or another coding-agent community.
- [ ] Open GitHub issues for real feedback themes.
- [ ] Add one or two routing regression tests from community examples.
- [ ] Prepare demo GIF if not already done.

## After First Feedback

- [ ] Cut `v0.1.1` if installation or docs need fixes.
- [ ] Add a FAQ section if the same question appears twice.
- [ ] Improve README with one real user scenario.
- [ ] Consider Product Hunt only after GIF/screenshot assets exist.

## Metrics To Watch

- GitHub stars.
- Clone count.
- Release downloads if any.
- Discussions opened.
- Issues with real missed-routing examples.
- Comments asking "does this work with my setup?"

## Reply Template For Feedback

```text
Thanks, this is exactly the kind of missed-routing case I am looking for.

I will map it as:

- request:
- expected primary capability:
- tempting wrong capability:
- missing routing signal:
- possible negative example:

If it is stable enough, I will turn it into a regression test.
```
