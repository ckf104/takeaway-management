import random
import string
import time

customer_list = []
tradesman_list = []
goods_list = []
rider_list = []
order_list = []

customer_name_list = ['James', 'Robert', 'John', 'Michael', 'William', 
             'Mary', 'Patricia', 'Jennifer', 'Jessica', 'Amelia',
             'Oliver', 'Jack', 'Harry', 'Jacob', 'Charlie',
             'Olivia', 'Isla', 'Emily', 'Poppy', 'Ava']

tradesman_name_list = ['张三', '李四', '王五', '赵六', '孙七']
storename_list = ['肯德基', '麦当劳', '汉堡王', '德克士', '华莱士']

goodsname_price_list = [('香辣鸡腿堡', 21.5), ('新奥尔良烤鸡腿堡', 22), ('劲脆鸡腿堡', 21.5), ('黄金SPA鸡排堡', 19), ('老北京鸡肉卷', 20),
                        ('香辣鸡翅', 13.5), ('黄金鸡块', 13.5), ('劲爆鸡米花', 16.5), ('霸王薯条', 15.5), ('醇香土豆泥', 9),
                        ('板烧鸡腿堡', 25.5), ('麦香鸡汉堡', 17.5), ('麦辣鸡腿堡', 24.5), ('双层吉士汉堡', 23.5), ('麦乐鸡', 15),
                        ('奥利奥麦旋风', 14.5), ('草莓麦旋风', 14.5), ('朱古力新地', 12.5), ('草莓新地', 12.5), ('香芋派', 8.5),
                        ('新年菠培皇堡', 36), ('新年菠培鸡腿皇堡', 36), ('大嘴安格斯', 52), ('安格斯厚牛堡', 42), ('三层天椒皇堡', 54),
                        ('新霸王鸡盒', 45), ('王道热辣鸡锁骨', 15), ('芋泥芝芝酥皮派', 9), ('霸王鸡条', 16.5), ('王道嫩香鸡块', 13.5),
                        ('脆皮手枪腿', 29), ('脆皮鸡腿', 9.9), ('黄金Q虾堡', 21), ('柠香鸡腿堡', 20), ('菠萝鸡腿堡', 23),
                        ('麻辣啃骨鸡', 13), ('椒香辣骨鸡', 15), ('魔法鸡块', 14), ('孜然鸡柳', 13), ('咔滋薯条', 13),
                        ('辣味鸡肉卷', 15), ('秘制鸡腿堡', 15), ('劲脆鲜虾堡', 15), ('牛气冲天堡', 15), ('深海鳕鱼堡', 15),
                        ('香酥鸡腿', 13), ('甘梅红薯条', 12), ('香芋地瓜丸', 9), ('秘制烤翅', 13), ('黑椒鸡块', 12)]

ridername_list = ['小明', '小红', '小王', '小张', '小李',
                  '小赵', '小陈', '小唐', '小周', '小孙']

for pos in range(len(customer_name_list)) :
    customer_name = customer_name_list[pos]
    
    name = customer_name
    
    chars = string.ascii_letters + string.digits
    password = ''.join([random.choice(chars) for i in range(10)])
    
    telephone = ''.join([random.choice(string.digits) for i in range(11)])
    
    s_tuple = (1976,1,1,0,0,0,0,0,0)
    e_tuple = (2005,12,31,23,59,59,0,0,0)
    start = time.mktime(s_tuple)
    end = time.mktime(e_tuple)
    birthday_secs = random.randint(start, end)
    birthday_tuple = time.localtime(birthday_secs)
    birthday = time.strftime("%Y-%m-%d", birthday_tuple)
    
    if pos < 5 or (pos >= 10 and pos < 15) :
        gender = 1
    else :
        gender = 0
    
    realname = customer_name
    
    id = ''.join([random.choice(string.digits) for i in range(18)])
    
    address = name + " home"
    
    customer_list.append((name,password,telephone,birthday,gender,realname,id,address))

for pos in range(len(tradesman_name_list)) :
    name = tradesman_name_list[pos]

    chars = string.ascii_letters + string.digits
    password = ''.join([random.choice(chars) for i in range(10)])
    
    telephone = ''.join([random.choice(string.digits) for i in range(11)])
    
    address = name + '店'
    
    storename = storename_list[pos]
    
    tradesman_list.append((name,password,telephone,address,storename))

for pos in range(len(goodsname_price_list)) :
    if pos < 10 :
        storename = storename_list[0]
    elif pos < 20 :
        storename = storename_list[1]
    elif pos < 30 :
        storename = storename_list[2]
    elif pos < 40 :
        storename = storename_list[3]
    else :
        storename = storename_list[4] 
    
    goodsname_price_tuple = goodsname_price_list[pos]
    goodsname = goodsname_price_tuple[0]
    price = goodsname_price_tuple[1]
    
    goods_list.append((storename, goodsname, price))
      
for ridername in ridername_list :
    name = ridername
    
    chars = string.ascii_letters + string.digits
    password = ''.join([random.choice(chars) for i in range(10)])
    
    telephone = ''.join([random.choice(string.digits) for i in range(11)])
    
    realname = name
    
    address = name + '家'
    
    rider_list.append((name,password,telephone,realname,address))

for customer_name in customer_name_list :
    for i in range(3) :
        s_tuple = (2020,1,1,0,0,0,0,0,0)
        e_tuple = (2022,12,31,23,59,59,0,0,0)
        start = time.mktime(s_tuple)
        end = time.mktime(e_tuple)
        order_time_secs = random.randint(start, end)
        order_time_struct = time.localtime(order_time_secs)
        order_time = time.strftime("%Y-%m-%d %H:%M:%S",order_time_struct)
        
        status = 6
        
        customer = customer_name
        
        rider_pos = random.randrange(len(ridername_list))
        rider = ridername_list[rider_pos]
        
        goods_pos = random.randrange(len(goodsname_price_list))
        goodsname = goodsname_price_list[goods_pos][0]
        price = goodsname_price_list[goods_pos][1]
        if goods_pos < 10 :
            storename = storename_list[0]
        elif goods_pos < 20 :
            storename = storename_list[1]
        elif goods_pos < 30 :
            storename = storename_list[2]
        elif goods_pos < 40 :
            storename = storename_list[3]
        else :
            storename = storename_list[4]
        
        number = random.randint(1,10)
        
        order_list.append((order_time, status, customer, rider, storename, goodsname, number, price))
        
      


    
    
    
        
    
