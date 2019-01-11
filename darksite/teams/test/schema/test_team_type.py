from teams import schema


def test_resolve_members(team_member_factory):
    """
    The members field should resolve to an iterable of
    :class:`TeamMember` instances to maintain the extra information
    from the intermediate model in the many-to-many relationship.
    """
    member = team_member_factory()

    assert list(schema.TeamType.resolve_members(member.team)) == [member]
