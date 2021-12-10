import yaml
import os

'''toolsClass
'''
class Util(object):

    def __init__(self):
        pass

    def operateYaml(self, filename):
        try:
            # 当前文件路径
            CUR_PATH = os.path.realpath(__file__)
            print(CUR_PATH)
            # 项目根目录
            ROOT_PATH = os.path.dirname(os.path.dirname(CUR_PATH))
            print(ROOT_PATH)
            yaml_path = os.path.join(ROOT_PATH, "data", filename)
            file = open(yaml_path, "r",encoding='utf-8')
            data = yaml.load(file,Loader=yaml.FullLoader)
            file.close()
        except Exception as msg:
            raise IOError("读yaml文件报错")
        return data


if __name__ == "__main__":

    d = Util().operateYaml("proposal_sbr.yaml")
    print(d['assert'])




