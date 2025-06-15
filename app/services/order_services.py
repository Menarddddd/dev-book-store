from ..core.errors import HTTPError


discounted_members = {
    "Student": 8,
    "Senior-citizen": 9, 
    "Teacher": 3,
    "Police": 3,
    "Disabled": 8
}


def is_eligible(member_type: str):
    return member_type in discounted_members


def get_member_discount(member_type: str, orig_price):
    if not is_eligible(member_type):
        HTTPError.bad_request("We're sorry, you are not eligible for this discount")

    discounted_amount = discounted_members[member_type]
    discounted_price = orig_price - discounted_amount
    return {"discounted_amount": discounted_amount, "total_amount": discounted_price}
