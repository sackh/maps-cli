"""Common utilities across project."""


def yield_subcommands(obj):
    """
    Show list of all available sub commands.

    :param obj: ``Click`` command object.
    """
    for name, value in obj.commands.items():
        if name != "show":
            yield name
