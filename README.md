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
   | storename | 展示给客户的商店名称，在identity=tradesman时含有该参数       |

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

5. 修改个人信息(session中identity=customer/tradesman，identity为其他值时接口尚未设计好)

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
   | address   | 新的住址(identity=customer)或新的店铺地址(identity=tradesman), 可选参数，为空则不修改 |

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则修改成功，否则s包含修改失败的原因

6. 订单状况改变

   * 请求url

   ```
   /info/orderchange
   ```

   * 请求参数

   | 参数     | 说明                                      |
   | -------- | ----------------------------------------- |
   | id       | 订单编号                                  |
   | previous | 一个包含数字0-6的字符串，表示订单当前状态 |
   | next     | 一个包含数字0-6的字符串，订单新状态       |

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则修改成功，否则s包含修改失败的原因

7. 商家修改，添加，删除菜品

   * 请求url

   ```
   /info/goodschange
   ```

   * 请求参数

   | 参数      | 说明                 |
   | --------- | -------------------- |
   | prevname  | 菜品原名称，可选参数 |
   | prevprice | 菜品原价格，可选参数 |
   | newname   | 菜品新名称，可选参数 |
   | newprice  | 菜品新价格，可选参数 |
   | storename | the name of store, will exist if `identity == manager` |

   参数有三种组合可能，仅有`prevname`, `prevprice`，表示删除该菜品。仅有`newname`, `newprice`，表示添加新菜品。包含`prevname`和`prevprice`，`newname`和`newprice`中至少包含一个（不存在的参数表示不修改该项），表示修改原菜名（单价）到新菜名（单价）

   * 请求方法：POST
   * 返回值：一个字符串s，如果s=='true'则修改成功，否则s包含修改失败的原因

8. Get goods info of a specific store
   * url
   ```
   /info/goodsinfo
   ```
   * request parameter
   
   | 参数      | 说明                 |
   | --------- | --------------------|
   | storename |  the name of this store |  

   * method: POST
   * return value: a json string containing a array, each element of which has `goodsname`, `sellcount`, `price` key, and corresponding value of key is obvious by the name of key, or error string if some error occurs.

9. Change user info by manager
   * url
   ```
   /info/manager_changeuser
   ```
   * request parameter
  | 参数      | 说明                                                         |
   | --------- | ------------------------------------------------------------ |
   | prevusername | required parameter, identify the username of user whose info will be changed |
   | name      | new username, don't change if empty                         |
   | password  | new password, don't change if empty                           |
   | telephone | new telephone, don't change if empty                                |
   | birthday  | new user's birthday, don't change if empty |
   | gender    | new gender, don't change if empty |
   | realname  | new real name, don't change if empty |
   | id        | new card id, don't change if empty             |
   | address   | new delivery address, don't change if empty |
   
   * method: POST
   * notes: if all parameters are empty except `prevusername`, delete this user's info
   * return value: a string containing `true` if success, otherwise containing error info

10. Change order info by manager
   * url
   ```
   /info/manager_changeorder
   ```
   * request parameter
   | 参数      | 说明                                                         |
   | --------- | ------------------------------------------------------------ |
   | id | required parameter, identify the id of the order whose info will be changed |
   | status      | new order status(a string containing 0-6), don't change if empty                         |
   | storename  | identify store name which accepts this order, don't change if empty                          |
   | goodsname | the goodsname that this order purchasing, don't change if empty                             |
   | number  | the number of purchasing, don't change if empty  |
   | price   | total price, don't change if empty  |
   | address  | delivery address, don't change if empty   |

   * method: POST
   * notes: if all parameters are empty except `id`, delete this order
   * return value: a string containing `true` if success, otherwise containing error info

11. Change rider info by manager
   * url
   ```
   /info/manager_changerider
   ```
   * request parameter
  | 参数      | 说明                                                         |
   | --------- | ------------------------------------------------------------ |
   | prevridername | required parameter, identify the ridername of rider whose info will be changed |
   | name      | new ridername(for login), don't change if empty                         |
   | password  | new password, don't change if empty                           |
   | telephone | new telephone, don't change if empty                                |
   | realname  | new real name of rider, don't change if empty |
   | address   | new home address, don't change if empty |
   
   * method: POST
   * notes: if all parameters are empty except `prevridername`, delete this rider
   * return value: a string containing `true` if success, otherwise containing error info

12. Change store info by manager
   * url
   ```
   /info/manager_changerider
   ```
   * request parameter
  | 参数      | 说明                                                         |
   | --------- | ------------------------------------------------------------ |
   | prevstorename | required parameter, identify the store name whose info will be changed |
   | name      | new login name, don't change if empty                         |
   | password  | new password, don't change if empty                           |
   | telephone | new telephone, don't change if empty                                |
   | storename  | new store name(the name customer will see), don't change if empty |
   | address   | new address of store, don't change if empty |
   
   * method: POST
   * notes: if all parameters are empty except `prevstorename`, delete this store and all its goods info
   * return value: a string containing `true` if success, otherwise containing error info

information needed by jinja template:

1. `user.html`
   * `g.username` 中存储了用户名
   * `g.goods`是一个python列表（可使用for循环迭代即可），每个元素表示了一个菜品，具有`storename`, `goodsname`, `price`, `sellcount`属性（可使用中括号语法[]或者 . 语法获取其值即可） ，其值分别表示商店名，商品名，价格，月售出份数，类型都是字符串。
   * `g.orders`是一个python列表（可使用for循环迭代即可），每个元素具有`id`, `goodsname`, `storename`, `price`, `number`, `status`属性（可使用中括号语法[]或者 . 语法获取其值即可），表示该用户进行中的订单（不包括已完成的），其值分别表示订单编号，商品名，商店名，总单价，商品数量，订单状况（如骑手配送中，商家未接单等等）。
2. `tradesman.html`
   * `g.username`存储了商店名称
   * `g.goods`是一个python列表（可使用for循环迭代即可），每个元素表示了该商店的一个菜品，具有`goodsname`, `price`, `sellcount`属性（可使用中括号语法[]或者 . 语法获取其值即可） ，其值分别表示商品名，价格，月售出份数，类型都是字符串。
   * `g.orders`是一个python列表（可使用for循环迭代即可），每个元素具有`id`, `goodsname`, `price`, `number`, `address`属性（可使用中括号语法[]或者 . 语法获取其值即可），表示该商家未确认的订单（订单状态0），其值分别表示订单编号，商品名，总单价，商品数量，配送地址。
3. `rider.html`
   * `g.username` stores username of rider
   * `g.waitingOrders` is a iterable object, each element of which has `id`, `storename`, `address`, `goodsname`, `number`, `useraddr` attributes. `g.waitingOrders` contains all orders waiting for riders to deliver
   * `g.accOrders` is a iterable object, each element of which has `id`, `storename`, `address`, `goodsname`, `number`, `useraddr` attributes. `g.accOrders` contains all orders this rider is delivering
4. `manager.html`
   * `g.username`stores the username of manager
   * `g.users` is a iterable object, each element of which has `username`, `gender`, `birthday`, `realname`, `id`, `address`, `telephone` attributes. `g.users` contains all users signing up
   * `g.orders` is a iterable object, each element of which has `id`, `status`, `storename`, `goodsname`, `number`, `price`, `address`(delivery address ) attributes. `g.orders` contains all orders that haven't been completed
   * `g.riders` is a iterable object, each element of which has `ridername`, `address`, `realname`, `telephone` attributes. `g.riders` contains all riders signing up.
   * `g.stores` is a iterable object, each element of which has `address`, `storename`(the store name customers will see), `telephone` attributes. `g.stores` contains all stores signing up.