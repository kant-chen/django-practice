import datetime

from django.db import models

from apps.core.models import Base
from apps.user.models import CustomUser


class Coupon(Base):
    TWD = "TWD"
    USER_RIGISTERD_COUPON = "USER_RIGISTERD_COUPON"
    COUPON_TYPE_COICES = (
        (1, USER_RIGISTERD_COUPON),
    )

    user = models.ForeignKey(
        CustomUser, related_name='coupons', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency_code = models.CharField(max_length=3, default=TWD)
    type = models.CharField(max_length=50, null=True,
                            choices=COUPON_TYPE_COICES)
    description = models.CharField(max_length=100, null=True)
    expired_date = models.DateField(null=True)

    @classmethod
    def create_user_registered_coupon(cls, user):
        """Create a coupon when a user just joins"""

        DESCRIPTION = "First Coupon for our valuable user"

        date_joined = user.created_at.date()
        thirty_days = datetime.timedelta(days=30)
        expired_date = date_joined + thirty_days
        coupon = cls.objects.create(
            user=user,
            amount=100,
            currency_code="TWD",
            type=cls.USER_RIGISTERD_COUPON,
            description=DESCRIPTION,
            expired_date=expired_date,
        )

        return coupon
