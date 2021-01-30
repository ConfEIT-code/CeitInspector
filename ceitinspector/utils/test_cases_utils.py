from file_system_utils import get_files_in_dir
import json

TEST_SCRIPTS_FILE = "test_scripts.json"

TEST_ORACLES_FILE = "test_oracles.json"



def main():
    t_files = []
    files = get_files_in_dir("/Users/Leo/Desktop/Docker/mod_perl-2.0.10/t", recursion=True)
    for k, v in files.items():
        for filename in v:
            if ".t" in filename and "txt" not in filename:
                p = k[42:]
                file = p + '/' + filename
                t_files.append(file)

    json_template1 = {}
    json_template2 = {}

    json_template1["1"] = {"script" : "ps -ef | grep /root/httpd/prefork/bin/httpd | grep -v grep | awk '{print $2}' | xargs kill -9"}
    json_template1["2"] = {"script" : "t/TEST -verbose -start-httpd"}
    json_template2["1"] = {
        "oracle": "",
        "running": False,
        "timeout": 1,
        "ignored": False,
        "log2annotate": [
        ],
        "log2purge": [
        ]
    }
    json_template2["2"] = {
        "oracle": "started",
        "running": True,
        "timeout": 3,
        "ignored": False,
        "log2annotate": [
        ],
        "log2purge": [
        ]
    }

    count = 3
    for f in t_files:
        json_template1[str(count)] = {"script" : "t/TEST -verbose " + f}
        json_template2[str(count)] = {
        "oracle": "Result: PASS",
        "running": False,
        "timeout": 3,
        "ignored": False,
        "log2annotate": [
        ],
        "log2purge": [
        ]
    }
        count += 1

    json_template1[str(count)] = {"script" : "t/TEST -verbose -stop-httpd"}
    json_template2[str(count)] = {
        "oracle": "shutdown",
        "running": True,
        "timeout": 4,
        "ignored": False,
        "log2annotate": [
        ],
        "log2purge": [
        ]
    }

    with open(TEST_SCRIPTS_FILE, 'w') as fp:
        json.dump(json_template1, fp)
    with open(TEST_ORACLES_FILE, 'w') as fp:
        json.dump(json_template2, fp)

if __name__ == '__main__':
    main()