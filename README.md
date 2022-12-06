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

4. 用户提交订单

   * 请求url

   ```
   /info/orders
   ```

   * 请求参数：一个json对象（可通过`request.json`获取），该json对象是一个列表，列表中每个元素形如下的字典，key表示的含义分别为商店名，商品名，数量，总单价。

   ```python
   {'storename': somevalue, 'goodsname': somevalue, 'number': somevalue, 'price': somevalue}
   ```

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则订单提交成功，否则s包含订单提交失败的原因

5. 用户修改个人信息(identity=customer)

   * 请求url

   ```
   /info/changesetting
   ```

   * 请求参数（合法请求应包含至少一个参数）

| 参数      | 说明                                                         |
| --------- | ------------------------------------------------------------ |
| name      | 新的登录用户名，格式要求同注册时一致，可选参数，为空则不修改 |
| password  | 新的登录密码，格式要求同注册时一致，可选参数，为空则不修改   |
| telephone | 新的电话，格式要求同注册时一致，可选参数，为空则不修改       |
| address   | 新的住址，可选参数，为空则不修改                             |

6. TODO



information needed by jinja template:

1. `/front-end/user.html`
   * `g.username` 中存储了用户名
   * `g.goods`是一个python列表（可使用for循环迭代即可），每个元素表示了一个菜品，具有`storename`, `goodsname`, `price`, `sellcount`属性（可使用中括号语法[]或者 . 语法获取其值即可） ，其值分别表示商店名，商品名，价格，月售出份数，类型都是字符串。
   * `g.orders`是一个python列表（可使用for循环迭代即可），每个元素具有`id`, `goodsname`, `storename`, `price`, `number`, `status`属性（可使用中括号语法[]或者 . 语法获取其值即可），表示该用户进行中的订单（不包括已完成的），其值分别表示订单编号，商品名，商店名，总单价，商品数量，订单状况（如骑手配送中，商家未接单等等）。
