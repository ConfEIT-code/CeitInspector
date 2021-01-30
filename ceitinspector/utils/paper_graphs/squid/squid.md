| type | symptom                                                      |
| ---- | ------------------------------------------------------------ |
| A    | No such file or directory                                    |
| B    | FATAL: Sign hash 'xxx' is not supported                      |
| C    | FATAL: Could not create a DNS socket                         |
| D    | ERROR: Cannot connect to 127.0.0.1:3128                      |
| E    | FATAL: Can't parse configuration token: 'xxx'                |
| F    | commBind: Cannot bind_observer socket xxx Cannot assign requested address |
| G    | FATAL: dying from an unhandled exception: theProcessCount > 0 |

|          | ID   | name                          | num  | type |
| -------- | ---- | ----------------------------- | ---- | ---- |
| fuzzing  | 1    | Squid:wccp_address            | 1    | A    |
|  fuzzing  | 2    | Squid:hosts_file              | 1    | A    |
| fuzzing | 3    | Squid:tcp_outgoing_address    | 1    | A    |
|   fuzzing       | 4    | Squid:sslproxy_cert_sign_hash | 1    | B    |
|   fuzzing       | 5    | Squid:udp_incoming_address    | 1    | A    |
|   fuzzing       | 6    | Squid:wccp2_address           | 1    | A    |
|   fuzzing       | 7    | Squid:udp_outgoing_address    | 1    | C    |
|    fuzzing      | 8    | Squid:debug_options           | 1    | A    |
|    fuzzing      | 9    | Squid:error_directory         | 1    | A    |
|   fuzzing       | 10   | Squid:mime_table              | 1    | A    |
| fuzzing  | 11   | Squid:icon_directory          | 1    | A    |
| conferr         | 12   | Squid:wccp_address            | 1    | D    |
|    conferr      | 13   | Squid:hosts_file              | 3    | AAA  |
|          conferr | 14   | Squid:tcp_outgoing_address    | 2    | DD   |
| conferr         | 15   | Squid:sslproxy_cert_sign_hash | 2    | BB   |
|    conferr      | 16   | Squid:udp_incoming_address    | 1    | D    |
|        conferr  | 17   | Squid:client_netmask          | 2    | DD   |
|     conferr     | 18   | Squid:wccp2_address           | 1    | D    |
|   conferr       | 19   | Squid:url_rewrite_extras      | 1    | E    |
|   conferr       | 20   | Squid:udp_outgoing_address    | 1    | D    |
|   conferr       | 21   | Squid:debug_options           | 1    | A    |
|   conferr       | 22   | Squid:error_directory         | 3    | AAA  |
|  conferr        | 23   | Squid:store_id_extras         | 1    | E    |
|  conferr        | 24   | Squid:mime_table              | 3    | AAA  |
| conferr  | 25   | Squid:icon_directory          | 3    | AAA  |
| conftest         | 26   | Squid:hosts_file              | 4    | AAAA |
| conftest         | 27   | Squid:tcp_outgoing_address    | 1    | A    |
| conftest         | 28   | Squid:sslproxy_cert_sign_hash | 1    | B    |
| conftest         | 29   | Squid:udp_incoming_address    | 2    | FF   |
|  conftest        | 30   | Squid:udp_outgoing_address    | 2    | CC   |
|  conftest        | 31   | Squid:debug_options           | 1    | A    |
|   conftest       | 32   | Squid:digest_bits_per_entry   | 1    | A    |
| conftest         | 33   | Squid:error_directory         | 2    | AA   |
|   conftest       | 34   | Squid:mime_table              | 3    | AAA  |
|  conftest        | 35   | Squid:icon_directory          | 2    | AA   |
| conftest | 36   | Squid:workers                 | 1    | G    |