# GitLab Reference

Use this reference when the repository workflow runs on GitLab or when the task requires GitLab-specific mechanics. Keep the portable semantics from `../SKILL.md` as the source of truth.

## Canonical mapping

| Portable concern | GitLab mechanic |
|---|---|
| Issue record | GitLab Issue |
| Status | Labels such as `status:ready`, `status:blocked` |
| Priority | Labels such as `priority:high` |
| Release grouping | Milestones |
| Delivery artifact | Merge Request |
| Visualization | Issue boards |

## Labels

Use labels as the canonical machine-readable workflow state. Keep exactly one active status label at a time.

Relevant docs:
- https://docs.gitlab.com/ee/user/project/labels.html
- https://docs.gitlab.com/ee/user/project/issues/

Operational guidance:
- prefer status and priority labels over board-only state
- remove contradictory status labels instead of stacking new ones
- treat label changes as the canonical state mutation

## Milestones

Use milestones for release or iteration grouping only. Do not overload milestones with status semantics.

Relevant doc:
- https://docs.gitlab.com/ee/user/project/milestones.html

## Issue and MR templates

Use issue templates, description templates, or MR templates when the repository supports them so records consistently capture goal, acceptance criteria, blockers, and related delivery artifacts.

Relevant docs:
- https://docs.gitlab.com/ee/user/project/issue_templates.html
- https://docs.gitlab.com/ee/user/project/description_templates.html
- https://docs.gitlab.com/ee/user/project/merge_requests/merge_request_templates.html

Recommended portable fields:
- Goal
- Acceptance Criteria
- Blocked by
- Primary MR

## Issue and MR linkage

GitLab supports linking merge requests to issues and automatically closing issues from merge requests. Use that for delivery linkage, but keep the issue body and labels authoritative for workflow state.

Relevant docs:
- https://docs.gitlab.com/ee/user/project/merge_requests/using_merge_requests.html#closing-issues-with-merge-requests
- https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically-from-merge-requests
- https://docs.gitlab.com/ee/user/project/issue_links.html

Operational guidance:
- one MR should name one primary issue
- use closing or related references in the MR description
- if the MR is open, make sure the issue can point back to it when useful
- do not let workflow coordination live only in MR comments

## Boards

GitLab issue boards are useful views, not the canonical task record.

Relevant docs:
- https://docs.gitlab.com/ee/user/project/boards.html
- https://docs.gitlab.com/ee/user/project/issue_board.html

Operational guidance:
- if a board column disagrees with labels, fix labels first
- do not assume moving a card means the issue record is now correct

## Automation surfaces

GitLab provides APIs and repository automation surfaces for issue and MR mutation. Use them to apply portable workflow rules more consistently, not to invent a second hidden state machine.

Relevant docs:
- https://docs.gitlab.com/ee/api/issues.html
- https://docs.gitlab.com/ee/api/merge_requests.html

## Blockers on GitLab

GitLab offers richer issue relationship features than some other providers, but this skill should still keep blockers portable. Represent blockers explicitly in the issue body or comments using portable text such as:

```md
## Blocked by
#123
```

Then align labels accordingly:
- add `status:blocked`
- remove the previous active status label
- restore the correct active status when the blocker clears

This keeps the workflow portable even if the repository later moves away from GitLab-specific issue relationships.

## Preferred operating order

1. Read the issue body, labels, milestone, recent comments, and MR state.
2. Normalize labels so there is one active status.
3. Apply the smallest correct mutation through issue labels or body updates.
4. Keep MR linkage explicit.
5. Re-check the issue after mutation rather than trusting the UI.

## Things not to rely on

- board columns as source of truth
- premium-only planning features as the base workflow model
- hidden blocker state that exists only in comments without label updates
- GitLab-only workflow semantics that cannot be mirrored in the issue record
