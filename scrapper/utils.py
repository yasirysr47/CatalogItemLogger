def format_data(data):
    result = []
    if type(data[0]) != tuple:
        return {"message": "No data found"}
    
    for record in data:
        data_dict = {
            "manufacturer": record[0],
            "category": record[1],
            "model": record[2],
            "part": record[3],
            "part_category": record[4]
        }
        result.append(data_dict)
    return result