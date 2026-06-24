from members.models import GymMember


def account_membership(request):
    if not request.user.is_authenticated:
        return {"account_member": None}

    member = (
        GymMember.objects.select_related("membership_plan")
        .filter(user=request.user)
        .first()
    )
    return {"account_member": member}
