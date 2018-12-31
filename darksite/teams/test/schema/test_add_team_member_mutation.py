import pytest
from graphql import GraphQLError

from teams import schema, models


class Info:
    def __init__(self, context):
        self.context = context


def test_mutate_coach(rf, team_factory, person_factory, user_factory):
    """
    Staff users should be able to add a coach to the team.
    """
    mutation = schema.AddTeamMember()
    team = team_factory()
    person = person_factory()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    result = mutation.mutate(
        Info(request),
        person_slug=person.slug,
        role=models.TeamMember.COACH,
        team_year=team.year,
    )

    assert models.TeamMember.objects.exists()
    assert result.team_member.person == person
    assert result.team_member.role == models.TeamMember.COACH
    assert result.team_member.team == team


def test_mutate_duplicate(rf, team_member_factory, user_factory):
    """
    Attempting to add a duplicate team member should raise an error.
    """
    mutation = schema.AddTeamMember()
    member = team_member_factory()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    with pytest.raises(GraphQLError):
        mutation.mutate(
            Info(request),
            person_slug=member.person.slug,
            role=models.TeamMember.COACH,
            team_year=member.team.year,
        )


def test_mutate_invalid_person(rf, team_factory, user_factory):
    """
    If an invalid person slug is provided, an error should be raised.
    """
    mutation = schema.AddTeamMember()
    team = team_factory()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    with pytest.raises(GraphQLError):
        mutation.mutate(
            Info(request),
            person_slug="invalid-slug",
            role=models.TeamMember.COACH,
            team_year=team.year,
        )


def test_mutate_invalid_team(person_factory, rf, user_factory):
    """
    If there is no team for the provided year, an error should be
    raised.
    """
    mutation = schema.AddTeamMember()
    person = person_factory()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    with pytest.raises(GraphQLError):
        mutation.mutate(
            Info(request),
            person_slug=person.slug,
            role=models.TeamMember.COACH,
            team_year=2018,
        )


def test_mutate_non_staff(person_factory, rf, team_factory, user_factory):
    """
    If a non-staff user attempts to add a team member, an exception
    should be raised.
    """
    mutation = schema.AddTeamMember()
    team = team_factory()
    person = person_factory()

    user = user_factory()
    request = rf.post("/")
    request.user = user

    with pytest.raises(GraphQLError):
        mutation.mutate(
            Info(request),
            person_slug=person.slug,
            role=models.TeamMember.COACH,
            team_year=team.year,
        )

    assert models.TeamMember.objects.count() == 0


def test_mutate_player(person_factory, rf, team_factory, user_factory):
    """
    Staff users should be able to add a player to the team.
    """
    mutation = schema.AddTeamMember()
    team = team_factory()
    person = person_factory()

    user = user_factory(is_staff=True)
    request = rf.post("/")
    request.user = user

    result = mutation.mutate(
        Info(request),
        number=42,
        person_slug=person.slug,
        role=models.TeamMember.PLAYER,
        team_year=team.year,
    )

    assert models.TeamMember.objects.exists()
    assert result.team_member.number == 42
    assert result.team_member.person == person
    assert result.team_member.role == models.TeamMember.PLAYER
    assert result.team_member.team == team
