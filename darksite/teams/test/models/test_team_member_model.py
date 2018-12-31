from teams import models


def test_repr(person_factory, team_factory):
    """
    The representation of a team member should contain the information
    required to reconstruct it.
    """
    member = models.TeamMember(
        number=42,
        person=person_factory(),
        role=models.TeamMember.PLAYER,
        team=team_factory(),
    )
    expected = (
        f"TeamMember(id={repr(member.id)}, number={repr(member.number)}, "
        f"person_slug={repr(member.person.slug)}, role={repr(member.role)}, "
        f"team_id={repr(member.team.id)})"
    )

    assert repr(member) == expected


def test_str(person_factory):
    """
    Converting a team member to a string should return a user readable
    string describing the instance.
    """
    member = models.TeamMember(
        person=person_factory(), role=models.TeamMember.COACH
    )

    assert str(member) == member.person.name


def test_str_with_number(person_factory):
    """
    If the team member has a number, it should be included in the string
    conversion.
    """
    member = models.TeamMember(
        number=42, person=person_factory(), role=models.TeamMember.PLAYER
    )

    assert str(member) == f"{member.person.name} (#{member.number})"
