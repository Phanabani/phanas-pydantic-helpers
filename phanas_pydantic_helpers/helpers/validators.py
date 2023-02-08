__all__ = ["maybe_relative_path", "only_one_of"]

from pathlib import Path
from typing import Any, Dict, List, Union

from pydantic import ConfigError, root_validator, validator

from phanas_pydantic_helpers.common.typing import T_MaybeList, ensure_list


def maybe_relative_path(fields: T_MaybeList[str], root_path: Path):
    fields = ensure_list(fields)

    def validate_fn(path: Union[Path, str]):
        if not isinstance(path, Path):
            path = Path(path)
        if not path.is_absolute():
            return root_path / path
        return path

    return validator(*fields, allow_reuse=True)(validate_fn)


def only_one_of(
    *groups_of_fields: T_MaybeList[str], need_all: Union[bool, List[bool]] = True
):
    """
    A Pydantic root validator that ensures one and only one of the groups of
    fields exists in the model.

    :param groups_of_fields: the groups of fields that you want one and only
        one of. Each group may be either a list of field names or a single
        field name.
    :param need_all: whether the groups need all fields or just one to succeed.
        If this arg is a bool, apply to all fields. If it's a list of bools,
        each item will be matched up with the corresponding field group from
        `groups_of_fields` (the list lengths must match).
    """
    if isinstance(need_all, list) and len(need_all) != len(groups_of_fields):
        raise ConfigError(
            "`need_all` must either be a bool or a list of bools of the same "
            "length as `groups_of_fields`"
        )

    groups_of_fields = list(groups_of_fields)
    for idx, group in enumerate(groups_of_fields):
        groups_of_fields[idx] = ensure_list(group)

    def validate_fn(cls, values: Dict[str, Any]):
        a_group_succeeded = False

        for idx, group in enumerate(groups_of_fields):
            required: bool = need_all[idx] if isinstance(need_all, list) else need_all
            existing_fields = [name in values for name in group]

            # Ignore if no fields exist
            if not any(existing_fields):
                continue

            # Two groups coexist, not allowed!
            if a_group_succeeded:
                raise ValueError(
                    f"Only one of the following groups of fields is allowed: "
                    f"{', '.join(map(str, groups_of_fields))}"
                )

            # Check that all fields exist if that was requested
            if required and not all(existing_fields):
                found = [name for name in group if name in values]
                missing = [name for name in group if name not in values]
                raise ValueError(
                    f"The fields {found} exist, but the following are also "
                    f"required and missing: {missing}"
                )

            # If we've made it here, this group has succeeded
            a_group_succeeded = True

        if not a_group_succeeded:
            raise ValueError(
                f"One and only one of the following groups must exist: "
                f"{', '.join(map(str, groups_of_fields))}"
            )

        return values

    return root_validator(pre=True, allow_reuse=True)(validate_fn)
