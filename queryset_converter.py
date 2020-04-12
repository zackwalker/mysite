def queryset_value_to_list(queryset_values,field_name):
    temp = []
    for values in queryset_values:
        temp.append(float(values[field_name]))
    return temp
