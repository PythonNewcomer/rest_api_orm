from json import dumps


class DataTransformer(object):

    def transform_dataset_into_json(self, result):
        list = []
        for row in result:
            dic = {}
            dic['id'] = row[0]
            dic['country'] = row[1]
            dic['continent'] = row[2]
            list.append(dic)
        return dumps(list)


    def transform_row_into_json(self, result):
        dic = {}
        try:
            row = result[0]  # result returns list even if it consists of one tuple only
            dic['id'] = row[0]
            dic['country'] = row[1]
            dic['continent'] = row[2]
        except IndexError:
            dic['message'] = "Country Not Found"
        return dumps(dic)
