"""This module defines exceptions."""
import click


class ApiKeyNotFoundError(click.UsageError):
    """Exception raised when API KEY for provider is not provided as option and it is not
    present in respected environment variable.
    """
