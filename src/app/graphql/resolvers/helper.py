from strawberry import Info


def is_field_requested(info: Info, field_name: str) -> bool:
    for field_node in info.field_nodes:
        if field_node.selection_set:
            for selection in field_node.selection_set.selections:
                if selection.name.value == field_name:
                    return True
    return False

