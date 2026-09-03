from content.models import Post

from .models import ModerationDecision


PROVIDER_OUTCOME_MAP = {
    "approved": ModerationDecision.Outcome.APPROVED,
    "blocked": ModerationDecision.Outcome.REJECTED,
    "review": ModerationDecision.Outcome.REVIEW,
}


def apply_provider_decision(post, provider_result):
    outcome = PROVIDER_OUTCOME_MAP.get(
        provider_result, ModerationDecision.Outcome.REJECTED
    )
    decision = ModerationDecision.objects.create(
        post=post, provider_result=provider_result, outcome=outcome
    )
    if outcome == ModerationDecision.Outcome.APPROVED:
        post.status = Post.Status.APPROVED
    elif outcome == ModerationDecision.Outcome.REJECTED:
        post.status = Post.Status.REJECTED
    post.save(update_fields=["status"])
    return decision
