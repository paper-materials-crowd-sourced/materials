from django.db import models

# Create your models here.
from panel.models import Code


CHECK_STATUS = (
    (0, "has not checked"),
    (1, "checked by our algorithm"),
    (2, "checked by random algorithm"),
    (3, "checked by both"),
)


class KeywordMeterStatus:
    has_not_checked = CHECK_STATUS[0][0]
    checked_by_our_algorithm = CHECK_STATUS[1][0]
    checked_by_random_algorithm = CHECK_STATUS[2][0]
    checked_by_both = CHECK_STATUS[3][0]


class GHResultKeywordMeter(models.Model):
    # Required
    answer_id = models.IntegerField()
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    ghUrl = models.CharField(max_length=1000)
    repo_name = models.CharField(max_length=300)

    # Optional
    is_vulnerable_our_algorithm = models.BooleanField(default=False, verbose_name="Own Vulnerable ?")
    is_vulnerable_random_algorithm = models.BooleanField(default=False, verbose_name="Random Vulnerable ?")
    is_error   = models.BooleanField(default=False, verbose_name="ERROR ?")
    status   = models.CharField(choices=CHECK_STATUS, default=0, max_length=50, verbose_name="Check Status")
    report = models.CharField(max_length=1000, default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Github Results - Meter"
        unique_together = [
            'answer_id',
            'ghUrl',
            'code'
        ]

    def __str__(self):
        return "{}".format(self.answer_id)
