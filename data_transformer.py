from json import dumps


class DataTransformer(object):

    def transform_dataset_into_json(self, result):
        list = []
        for row in result:
            dic = {}
            dic['id'] = row[0]
            dic['title'] = row[1]
            dic['year'] = row[2]
            dic['country_id'] = row[3]
            list.append(dic)
        return dumps(list)


    def transform_row_into_json(self, result):
        dic = {}
        try:
            row = result[0]  # result returns list even if it consists of one tuple only
            dic['id'] = row[0]
            dic['title'] = row[1]
            dic['year'] = row[2]
            dic['country_id'] = row[3]
        except IndexError:
            dic['message'] = "Movie Not Found"
        return dumps(dic)