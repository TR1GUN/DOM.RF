import pydantic


class AnswerBillingCadastre(pydantic.BaseModel):
    """
    Billing answer model
    """
    calculated: bool
