from django.db import models


# Create your models here.
class Code(models.Model):
    filename = models.CharField(max_length=255, name="filename", verbose_name="Filename", null=False)
    group_id = models.IntegerField(name="group_id", verbose_name="Group ID", null=False)
    snipped_code = models.TextField(name="snipped_code", verbose_name="Snipped Code", null=False)
    reviewed = models.BooleanField(name="reviewed", default=False, verbose_name="Is Reviewed ?")
    description = models.TextField(name="description", verbose_name="Description", null=True, blank=True, default="")
    is_vulnerable = models.BooleanField(name="is_vulnerable", verbose_name="Is Vulnerable ?", default=False)
    # answer_id = models.IntegerField(default=0,name="answer_id",verbose_name="Answer ID")


class sourl(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    url = models.URLField(name="url", verbose_name="URL")

    def __str__(self):
        return self.url


class Code_Answer(models.Model):
    answer_id = models.IntegerField()
    question_id = models.IntegerField(null=True, blank=True)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False, verbose_name="Done ?")

    def __str__(self):
        return "{} - {}".format(self.answer_id, self.code.filename)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class CodeTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            'tag',
            'code'
        ]

    def __str__(self):
        return "{} ({})".format(
            self.code.filename,
            self.tag.name,
        )


class GHResult(models.Model):
    answer_id = models.IntegerField()
    code = models.ForeignKey(Code, on_delete=models.CASCADE,default=None)
    ghUrl = models.CharField(max_length=1000)
    is_vulnerable = models.BooleanField(default=False, verbose_name="Vulnerable ?")
    is_checked = models.BooleanField(default=False, verbose_name="Checked ?")
    is_error   = models.BooleanField(default=False, verbose_name="ERROR ?")
    report = models.CharField(max_length=1000, default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Github Results"
        unique_together = [
            'answer_id',
            'ghUrl',
            'code'
        ]

    def __str__(self):
        return "{}".format(self.answer_id)


class GHResult_LastVersions(models.Model):
    answer_id = models.IntegerField()
    code = models.ForeignKey(Code, on_delete=models.CASCADE, default=None)
    ghUrl = models.CharField(max_length=1000)
    repo_name = models.CharField(blank=True, default="", max_length=300)
    is_vulnerable = models.BooleanField(default=False, verbose_name="Vulnerable ?")
    is_checked = models.BooleanField(default=False, verbose_name="Checked ?")
    is_error   = models.BooleanField(default=False, verbose_name="ERROR ?")
    report = models.CharField(max_length=1000, default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Github Results - Last Versions"
        unique_together = [
            'answer_id',
            'ghUrl',
            'code'
        ]

    def __str__(self):
        return "{}".format(self.answer_id)


class GHResult_KeywordMeter(models.Model):
    answer_id = models.IntegerField()
    code = models.ForeignKey(Code, on_delete=models.CASCADE, default=None)
    ghUrl = models.CharField(max_length=1000)
    repo_name = models.CharField(blank=True, default="", max_length=300)
    is_vulnerable = models.BooleanField(default=False, verbose_name="Vulnerable ?")
    is_checked = models.BooleanField(default=False, verbose_name="Checked ?")
    is_error   = models.BooleanField(default=False, verbose_name="ERROR ?")
    report = models.CharField(max_length=1000, default="", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Github Results - Keyword Meter"
        unique_together = [
            'answer_id',
            'ghUrl',
            'code'
        ]

    def __str__(self):
        return "{}".format(self.answer_id)