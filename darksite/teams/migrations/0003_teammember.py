# Generated by Django 2.1.5 on 2019-01-10 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("teams", "0002_person")]

    operations = [
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The time that the team member was created at.",
                        verbose_name="creation time",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        help_text="The team member's number if they are a player.",
                        null=True,
                        verbose_name="number",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("C", "Coach"), ("P", "Player")],
                        help_text="The member's role on the team.",
                        max_length=1,
                        verbose_name="role",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The last time the team member was updated.",
                        verbose_name="last update time",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        help_text="The person who is a member of the team.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teams.Person",
                        verbose_name="person",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="The team the person is a member of.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teams.Team",
                        verbose_name="team",
                    ),
                ),
            ],
            options={
                "verbose_name": "team member",
                "verbose_name_plural": "team members",
                "ordering": ("-created",),
            },
        ),
        migrations.AddField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                blank=True,
                help_text="The members who make up the team.",
                related_name="teams",
                related_query_name="team",
                through="teams.TeamMember",
                to="teams.Person",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="teammember", unique_together={("person", "team")}
        ),
    ]