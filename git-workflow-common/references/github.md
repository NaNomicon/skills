# GitHub Reference

Use this reference when the repository workflow runs on GitHub or when the task requires GitHub-specific mechanics. Keep the portable semantics from `../SKILL.md` as the source of truth.

## Canonical mapping

| Portable concern | GitHub mechanic |
|---|---|
| Issue record | GitHub Issue |
| Status | Labels such as `status:ready`, `status:blocked` |
| Priority | Labels such as `priority:high` |
| Release grouping | Milestones |
| Delivery artifact | Pull Request |
| Visualization | Projects / project boards |

## Labels

Use labels as the canonical machine-readable workflow state. Keep exactly one active status label at a time.

Relevant docs:
- https://docs.github.com/en/issues/tracking-your-work-with-labels/about-labels
- https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels

Operational guidance:
- prefer status and priority labels over board-only state
- remove contradictory status labels instead of adding a new one on top
- treat label changes as the canonical state mutation

## Milestones

Use milestones for release or iteration grouping only. Do not overload milestones with status semantics.

Relevant doc:
- https://docs.github.com/en/issues/tracking-your-work-with-issues/about-milestones

## Issue templates and forms

Use templates or issue forms when the repository supports them so issues consistently capture goal, acceptance criteria, blockers, and related delivery artifacts.

Relevant docs:
- https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issue-forms
- https://docs.github.com/en/issues/tracking-your-work-with-issues/about-templates-for-issues-and-pull-requests

Recommended portable fields:
- Goal
- Acceptance Criteria
- Blocked by
- Primary PR

## Pull request linkage

GitHub supports linking pull requests to issues and automatically closing issues on merge. Use that for delivery linkage, but keep the issue body and labels authoritative for workflow state.

Relevant doc:
- https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue

Operational guidance:
- one PR should name one primary issue
- use closing or related references in the PR body
- if the PR is open, make sure the issue can point back to it when useful
- do not let workflow coordination live only in PR comments

## Projects and boards

GitHub Projects and project boards are useful views, not the canonical task record.

Relevant docs:
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
- https://docs.github.com/en/issues/planning-and-tracking-with-kanban/managing-project-boards/about-project-boards

Operational guidance:
- if a project column disagrees with labels, fix labels first
- do not assume moving a card means the task record is now correct

## Automation surfaces

GitHub provides two common automation paths for workflow mutation:
- `gh` CLI for direct issue and PR operations
- GitHub Actions for event-driven workflow updates

Relevant docs:
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-the-github-cli
- https://docs.github.com/en/actions/using-workflows/about-workflows

Use automation to apply the same portable rules more consistently, not to invent a second hidden state machine.

## Blockers on GitHub

GitHub does not provide a portable, first-class blocker model you should depend on for this skill. Represent blockers explicitly in the issue body or comments using portable text such as:

```md
## Blocked by
#123
```

Then align labels accordingly:
- add `status:blocked`
- remove the previous active status label
- restore the correct active status when the blocker clears

## Preferred operating order

1. Read the issue body, labels, milestone, recent comments, and PR state.
2. Normalize labels so there is one active status.
3. Apply the smallest correct mutation through issue labels or body updates.
4. Keep PR linkage explicit.
5. Re-check the issue after mutation rather than trusting the UI.

## Things not to rely on

- project columns as source of truth
- hidden blocker state that exists only in comments without label updates
- GitHub-only conventions that cannot be mirrored in the issue record
