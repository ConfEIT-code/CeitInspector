
| type | symptom                                                   |
| ---- | --------------------------------------------------------- |
| A    | Error in server greeting.                                 |
| B    | Connecting to 127.0.0.1:21... failed: Connection refused. |
| C    | Error in server response, closing control connection.     |
| D    | Login incorrect.                                          |
| E    | Hang during the connection from client to server


|          | ID   | name                          | num  | type |
| -------- | ---- | ----------------------------- | ---- | ---- |
| fuzzing| 1    | vsftpd:ftp_username           | 1    | A    |
| fuzzing| 2    | vsftpd:listen_port            | 1    | B    |
|  fuzzing | 3    | vsftpd:secure_chroot_dir      | 1    | A    |
|  fuzzing| 4    | vsftpd:pam_service_name       | 1    | C    |
| fuzzing  | 5    | vsftpd:nopriv_user            | 1    | A    |
| conferr  | 6    | vsftpd:xferlog_file           | 1    | A    |
| conferr | 7    | vsftpd:ftp_username           | 3    | AAA  |
| conferr   | 8    | vsftpd:nopriv_user            | 3    | AAA  |
| conferr  | 9    | vsftpd:secure_chroot_dir      | 3    | AAA  |
|conferr  | 10   | vsftpd:listen_port            | 1    | B    |
| conferr  | 11   | vsftpd:delay_successful_login | 1    |  E    |
| conferr  | 12   | vsftpd:pam_service_name       | 2    | DD   |
| conftest  | 13   | vsftpd:pam_service_name       | 1    | D    |
| conftest  | 14   | vsftpd:ftp_username           | 1    | A    |
| conftest  | 15   | vsftpd:vsftpd_log_file        | 2    | AA   |
| conftest  | 16   | vsftpd:delay_successful_login | 2    | CC   |
| conftest  | 17   | vsftpd:listen_port            | 3    | BBB  |
| conftest | 18   | vsftpd:secure_chroot_dir      | 4    | AAAA |
| conftest | 19   | vsftpd:nopriv_user            | 1    | A    |
| conftest | 20   | vsftpd:xferlog_file           | 2    | AA   |