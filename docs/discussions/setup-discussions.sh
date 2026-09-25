#!/usr/bin/env bash
# Sets up the labels and "how to use this category" posts for course Discussions.
#
# Usage:  ./setup-discussions.sh OWNER/REPO            # labels + welcome posts
#         ./setup-discussions.sh OWNER/REPO --labels-only
#
# Needs the GitHub CLI (gh auth login) with admin/maintain access to OWNER/REPO.
# Categories must already exist (GitHub has no API for creating them) — see SETUP.md.
# Safe to re-run: labels are updated in place and existing welcome posts are skipped.
set -euo pipefail

REPO="${1:?usage: $0 OWNER/REPO [--labels-only]}"
MODE="${2:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OWNER="${REPO%%/*}"; NAME="${REPO##*/}"

echo "==> Labels"
while IFS='|' read -r label color desc; do
  [[ -z "$label" || "$label" == \#* ]] && continue
  gh label create "$label" --repo "$REPO" --color "$color" --description "$desc" --force >/dev/null
  echo "    ✓ $label"
done < "$HERE/labels.txt"
[[ "$MODE" == "--labels-only" ]] && exit 0

BRANCH="$(gh api "repos/$REPO" --jq .default_branch)"
GUIDE_URL="https://github.com/$REPO/blob/$BRANCH/docs/discussions/GUIDE.md"
IMG="https://github.com/$REPO/raw/$BRANCH/docs/discussions/images"

echo "==> Categories"
REPO_ID="$(gh api graphql -f query='query($o:String!,$n:String!){repository(owner:$o,name:$n){id}}' \
  -f o="$OWNER" -f n="$NAME" --jq .data.repository.id)"
CATS="$(gh api graphql -f query='query($o:String!,$n:String!){repository(owner:$o,name:$n){
  discussionCategories(first:25){nodes{id slug name}}}}' -f o="$OWNER" -f n="$NAME" \
  --jq '.data.repository.discussionCategories.nodes[] | "\(.slug)|\(.id)|\(.name)"')"
echo "$CATS" | sed 's/^/    /'

missing=0
for form in "$HERE"/../../.github/DISCUSSION_TEMPLATE/*.yml; do
  slug="$(basename "$form" .yml)"
  echo "$CATS" | awk -F'|' -v s="$slug" '$1==s{f=1} END{exit !f}' \
    || { echo "!!  Form $slug.yml matches no category slug — rename the file to the slug listed above."; missing=1; }
done
for f in "$HERE"/welcome-posts/*.md; do
  slug="$(basename "$f" .md)"
  cat_id="$(echo "$CATS" | awk -F'|' -v s="$slug" '$1==s{print $2}')"
  if [[ -z "$cat_id" ]]; then
    echo "!!  No category with slug '$slug' — create/rename it (SETUP.md step 1) and re-run."
    missing=1; continue
  fi
  title="$(head -n1 "$f" | sed 's/^# //')"
  if [[ "$slug" == "polls" ]]; then
    echo "--  $slug: polls can only be created in the browser. Paste docs/discussions/welcome-posts/polls.md manually (SETUP.md step 4)."
    continue
  fi
  exists="$(gh api graphql -f query='query($o:String!,$n:String!,$c:ID!){repository(owner:$o,name:$n){
    discussions(first:50,categoryId:$c){nodes{title url}}}}' -f o="$OWNER" -f n="$NAME" -f c="$cat_id" \
    --jq ".data.repository.discussions.nodes[] | select(.title==\"$title\") | .url")"
  if [[ -n "$exists" ]]; then echo "    = $slug: already posted → $exists"; continue; fi
  body="$(tail -n +2 "$f" | sed -e "s#{{GUIDE_URL}}#$GUIDE_URL#g" -e "s#{{IMG}}#$IMG#g")"
  url="$(gh api graphql -f query='mutation($r:ID!,$c:ID!,$t:String!,$b:String!){
    createDiscussion(input:{repositoryId:$r,categoryId:$c,title:$t,body:$b}){discussion{url}}}' \
    -f r="$REPO_ID" -f c="$cat_id" -f t="$title" -f b="$body" --jq .data.createDiscussion.discussion.url)"
  echo "    ✓ $slug → $url"
done

cat <<MSG

==> Left to do in the browser (GitHub has no API for these) — see SETUP.md steps 4–5:
    • Create the Polls welcome post as a poll
    • Open each welcome post → right sidebar → "Pin discussion to <category>"
    • Open the Announcements post → right sidebar → "Pin discussion" (pins it to the top of all Discussions)
MSG
exit $missing
