# -*- coding:utf-8 -*-
import json

FAIL = ['243', '249', '239', '246', '207', '216', '240', '16', '146', '245', '244', '250', '241', '237', '251', '238', '248', '247', '242', '236']
NOTESTS = ['123', '144', '136', '158', '128', '127', '190', '38', '11', '125', '122', '219', '155', '222', '184', '120', '131', '121', '124', '135', '45', '40', '103', '174', '51', '170', '58', '130', '52', '169', '175', '177', '48', '126', '129', '233', '78', '88', '87', '86', '118', '34', '73', '61']

PASS = ['1', '2', '188', '123', '137', '144', '106', '22', '53', '64', '41', '103', '98', '18', '76', '14', '128', '77', '43', '139', '151', '186', '62', '72', '8', '127', '182', '19', '172', '59', '82', '134', '80', '38', '11', '29', '125', '171', '110', '21', '122', '114', '109', '111', '159', '94', '107', '31', '105', '35', '91', '165', '71', '184', '84', '120', '104', '131', '102', '49', '121', '81', '124', '185', '42', '135', '150', '44', '40', '68', '176', '112', '174', '97', '163', '133', '26', '108', '141', '83', '16', '60', '143', '148', '65', '51', '70', '152', '46', '95', '161', '140', '170', '25', '181', '27', '54', '101', '39', '56', '162', '96', '58', '117', '89', '90', '23', '175', '154', '130', '153', '28', '113', '119', '87', '147', '142', '157', '15', '52', '66', '178', '79', '115', '169', '177', '69', '50', '100', '75', '48', '37', '126', '187', '6', '180', '45', '9', '20', '129', '32', '93', '167', '24', '30', '136', '13', '78', '63', '99', '149', '88', '116', '168', '4', '179', '67', '173', '3', '145', '33', '17', '86', '118', '183', '10', '34', '7', '12', '47', '138', '132', '73', '61', '85', '74', '55', '36', '166', '92']

with open ("/Users/Leo/Desktop/ceitinspector/ceitinspector/utils/test_scripts.json", 'r') as fp:
    content1 = fp.read()
    test_scripts = json.loads(content1)

with open ("/Users/Leo/Desktop/ceitinspector/ceitinspector/utils/test_oracles.json", 'r') as fp:
    content2 = fp.read()
    test_oracles = json.loads(content2)

new_test_scripts = {}
new_test_oracles = {}

new_count = 1
for i in range(252):
    count = str(i+1)
    #if count not in FAIL and count not in NOTESTS:
    if count in PASS:
        new_test_scripts[str(new_count)] = test_scripts[count]
        new_test_oracles[str(new_count)] = test_oracles[count]
        new_count += 1
    else:
        pass
with open("/Users/Leo/Desktop/ceitinspector/ceitinspector/utils/new_test_scripts.json", 'w') as fp1:
    with open("/Users/Leo/Desktop/ceitinspector/ceitinspector/utils/new_test_oracles.json", 'w') as fp2:
        json.dump(new_test_scripts, fp1)
        json.dump(new_test_oracles, fp2)

WRONG = []