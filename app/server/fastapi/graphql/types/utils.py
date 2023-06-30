def group_by(data):
    ids_map = {}
    for grouper_obj, *data_objects in data:
        if grouper_obj.id not in ids_map:
            ids_map[grouper_obj.id] = (grouper_obj, [])
        _, data_array = ids_map[grouper_obj.id]
        data_array.append(data_objects)
    return list(ids_map.values())