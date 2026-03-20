# GitLab Reference

Use this reference when the portable workflow needs to be executed through GitLab-specific mechanics.

## Core GitLab objects

- Issues
- Labels
- Milestones
- Merge requests
- Issue boards
- Comments, mentions, and cross-references

GitLab issue boards can visualize work, but the issue and its labels remain the canonical workflow record.

## Preferred mechanics

Use the safest available GitLab interface in the current environment, such as authenticated CLI, API, MCP, or browser tooling.

Common operations include:

- viewing an issue and discussion
- editing title/body
- adding or removing labels
- assigning users
- linking MRs through references in MR descriptions or issue comments

## Portable status mutation on GitLab

When changing issue state:

1. inspect existing labels first
2. remove the old `status:*` label
3. add the new `status:*` label
4. update issue body fields if blocker or linkage data changed
5. verify the final label set on the issue

Do not assume moving a card in an issue board is enough. If boards are used, they should reflect canonical labels.

## MR linkage on GitLab

Preferred references in MR descriptions:

- `Closes #123`
- `Related to #123`

Use a closing relationship only when merging the MR should complete the issue.

## Blocker representation on GitLab

Keep blockers portable even if GitLab offers richer issue relationship UX.

Preferred pattern:

```md
## Blocked by
#123
```

Pair that with:

- `status:blocked`
- removal of the prior active status label

This avoids coupling the core workflow to paid-tier or provider-specific dependency features.

## Pitfalls to avoid

- Treating issue board columns as canonical state
- Depending on Premium planning features for the base workflow contract
- Encoding workflow state only in discussion threads
- Allowing one MR to blur the primary issue relationship
