Source code of a takeaway management platform for homework of the database course.

* front-end: code of html, css, js
* back-end: code of python flask ?

interface protocol:

1. 验证登录

   * 请求URL：

   ```
   /auth/login
   ```

   * 请求参数

   | 参数     | 说明（格式要求）                                             |
   | -------- | ------------------------------------------------------------ |
   | identity | 取值应为customer, tradesman, rider, manager中的一个，必选参数 |
   | name     | 用户名，长度在3-20之间，必选参数                             |
   | password | 密码，长度在6-20之间，必选参数                               |

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'表示登录成功，否则s包含登陆失败原因

   

2. 用户注册

   * 请求URL：

   ```
   /auth/signup
   ```

   * 请求参数

   | 参数      | 说明                                                         |
   | --------- | ------------------------------------------------------------ |
   | identity  | 取值应为customer, tradesman, rider中的一个，必选参数         |
   | name      | 注册用户名，长度在3-20之间，必选参数                         |
   | password  | 注册密码，长度在6-20之间，必选参数                           |
   | telephone | 11位电话号码，必选参数                                       |
   | birthday  | 用户出生年月日, 格式为 xxxx-xx-xx，在identity=customer时含有该参数 |
   | gender    | 性别，取值为man, woman中的一个，在identity=customer时含有该参数 |
   | realname  | 顾客或骑手的真实姓名，在identity=customer or rider时含有该参数 |
   | id        | 身份证号，在identity=customer时含有该参数                    |
   | address   | 必选参数，在identity=customer时含义为送餐地址，在identity=tradesman时含义为商店地址，在identity=rider时含义为骑手家庭住址 |
   | storename | 展示给客户的商店名称，在identity=tradesman时含义有参数       |

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则注册成功，否则s包含注册失败原因



3. 用户登出（删除session）

   * 请求url

   ```
   /auth/logout
   ```

   * 请求参数：无
   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则登出成功，否则s包含登出失败的原因

4. 获取商家信息

   * 请求url

   ```
   /info/tradesman
   ```

   * 请求参数 TODO
