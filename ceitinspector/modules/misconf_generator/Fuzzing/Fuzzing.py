import hashlib
import time


class Fuzzing( object ):
    def __init__(self, option):
        """
        :param option: {u'key': u'Listen', u'value': u'80', u'constraint': u'PORT'}
                    {
                      "key": "directive",
                      "value" : "123 456 unit"
                      "value1": "123",
                      "value2" : "456",
                      "value3" : "unit",
                      "constraint": "INT[,]|INT[,]|ENUM",
                      "dependency_constraint" : {"2":"www.baidu.com"}
                    }
        """
        self.option_values = []
        self.option_value = option["value"]
        self.option_num = option["constraint"].count("|")+1
        if self.option_num == 1:
            self.option_values.append(option["value"])
        else:
            for i in range(self.option_num):
                id = str(i+1)
                self.option_values.append(option["value"+id])


        self.misconfs = []
        for i in range(self.option_num):
            misconf = [{
                "name": "randomstring",
                "key": None,
                "operator": None,
                "value": self.create_md5()
            }]
            misconf = self.add_other_values(misconf, i)
            self.misconfs.extend(misconf)

    def create_md5(self):
        m = hashlib.md5()
        m.update( bytes( str( time.time() ) ) )
        return m.hexdigest()

    def get_misconfs(self):
        return self.misconfs

    def add_other_values(self, misconf_list, i):
        """

        :param misconf_list:  [{"name": "str_misconf",
                 "key": None,
                 "operator": None,
                 "value": "wrongvalue"}]
        :param i: the index of the misconf_value
        :return:
        """
        if self.option_num == 1:
            return misconf_list
        else:
            for misconf in misconf_list:
                misconf_value = misconf["value"]
                temp_list = []
                for j in range(self.option_num):
                    if j == i:
                        temp_list.append(misconf_value)
                    else:
                        temp_list.append(self.option_values[j])

                target_value = " ".join(temp_list)
                misconf["value"] = target_value
                misconf["name"] = "option_" + str(i) + "_" + misconf["name"]
            return misconf_list
