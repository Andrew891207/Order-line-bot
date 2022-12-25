from transitions.extensions import GraphMachine
from utils import send_text_message, send_button_message, send_image_message, send_text_image
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction



#glibal variable
price=0

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    #start
    def is_going_to_lobby(self, event):
        global price
        price=0
        text = event.message.text
        return text == '選單'

    def on_enter_lobby(self, event):
        title = '選單'
        text = '請選擇你想要的功能?'
        btn = [
            MessageTemplateAction(
                label = '菜單',
                text = '菜單'
            ),
            MessageTemplateAction(
                label = '手沖咖啡推薦',
                text = '手沖咖啡推薦'
            ),
            MessageTemplateAction(
                label = '甜點照片以及熱量',
                text = '甜點照片以及熱量'
            ),
            MessageTemplateAction(
                label = '店家資訊',
                text = '店家資訊'
            ),
        ]
        url = 'https://wowlavie-aws.hmgcdn.com/file/article_all/%E5%A4%A7%E7%A8%BB%E5%9F%95%E3%80%8CTWATUTIA%E3%80%8D%E5%92%96%E5%95%A1%E5%BB%B31.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text == "菜單"

    def is_going_to_rec_coffee(self, event):
        text = event.message.text
        return text == "手沖咖啡推薦"

    def is_going_to_cal_dessert(self, event):
        text = event.message.text
        return text == "甜點照片以及熱量"

    def is_going_to_intro(self, event):
        text = event.message.text
        return text == "店家資訊"

    #state of menu
    def on_enter_menu(self, event):
        url = 'https://i.imgur.com/XqVG9Qy.png'
        text= "以下為本店的菜單，若想品嘗手沖咖啡或是查看甜點的成分及熱量，歡迎回到主選單查看推薦"
        text1= "輸入【選單】以重新開啟選單，或是輸入【點餐】進入點餐環節"
        send_text_image(event.reply_token, text, url, text1)
        
    def is_going_to_order(self, event):
        text = event.message.text
        if text == '點餐':
            return True       
        return False

    def on_enter_order(self, event):
        send_text_message(event.reply_token, "請輸入餐點品項全名，若要點取手沖咖啡，只需輸入【手沖咖啡】即可，咖啡豆品種請在至櫃台結帳時選擇")
    
    def is_going_to_order1(self, event):
        global price
        text = event.message.text
        if text == '手沖咖啡':
            price=price+150
            return True
        elif text == '美式咖啡':
            price=price+80
            return True
        elif text == '卡布奇諾':
            price=price+120
            return True
        elif text == '紅茶':
            price=price+60
            return True
        elif text == '奶茶':
            price=price+80
            return True
        elif text == '布朗尼':
            price=price+60
            return True
        elif text == '馬芬':
            price=price+60
            return True
        elif text == '司康':
            price=price+50
            return True
        elif text == '手工軟餅乾':
            price=price+70
            return True
            
        return False
        
    def on_enter_order1(self, event):
        global price
        text="目前價格為"
        text1=str(price)
        text2="元，若點餐完畢請輸入【結帳】，並至櫃台結帳，若要繼續點餐，繼續輸入餐點名稱即可"
        text4=text+text1+text2
        send_text_message(event.reply_token, text4)

    def is_going_to_order2(self, event):
        global price
        text = event.message.text
        if text == '手沖咖啡':
            price=price+150
            return True
        elif text == '美式咖啡':
            price=price+80
            return True
        elif text == '卡布奇諾':
            price=price+120
            return True
        elif text == '紅茶':
            price=price+60
            return True
        elif text == '奶茶':
            price=price+80
            return True
        elif text == '布朗尼':
            price=price+60
            return True
        elif text == '馬芬':
            price=price+60
            return True
        elif text == '司康':
            price=price+50
            return True
        elif text == '手工軟餅乾':
            price=price+70
            return True
            
        return False
        
    def on_enter_order2(self, event):
        global price
        text="目前價格為"
        text1=str(price)
        text2="元，若點餐完畢請輸入【結帳】，若要繼續點餐，繼續輸入餐點名稱即可"
        text4=text+text1+text2
        send_text_message(event.reply_token, text4)

    def is_going_to_cash(self, event):
        text = event.message.text
        if text == "結帳":
            return True
        return False

    def on_enter_cash(self, event):
        global price
        text="總共為"
        text1=str(price)
        text2="元，請至櫃台結帳，謝謝!\n若想使用其他選單功能，請再次輸入【選單】即可"
        text4=text+text1+text2
        price=0
        send_text_message(event.reply_token, text4)



    #state of rec_coffee
    def on_enter_rec_coffee(self, event):
        title = '手沖咖啡風味推薦'
        text = '您喜歡醇厚還是清爽的口感呢?'
        btn = [
            MessageTemplateAction(
                label = '醇厚',
                text = '醇厚'
            ),
            MessageTemplateAction(
                label = '清爽',
                text = '清爽'
            ),
        ]
        url = 'https://images.chinatimes.com/newsphoto/2022-03-29/1024/20220329003266.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    #state of bitter
    def is_going_to_bitter(self, event):
        text = event.message.text
        if text == '醇厚':
            return True
        return False

    def on_enter_bitter(self, event):
        title = '以下有三種豆子的推薦'
        text = '想選擇哪一款豆子查看風味描述呢'
        btn = [
            MessageTemplateAction(
                label = "瓜地馬拉 阿卡特南果",
                text = "瓜地馬拉 阿卡特南果"
            ),
            MessageTemplateAction(
                label = "玻利維亞 卡杜拉",
                text = "玻利維亞 卡杜拉"
            ),
            MessageTemplateAction(
                label = "宏都拉斯 帕拉伊內馬",
                text = "宏都拉斯 帕拉伊內馬"
            ),
        ]
        url = 'https://img.ltn.com.tw/Upload/food/page/2018/06/28/180628-7760-0-jYh8n.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_bitter_first(self, event):
        text = event.message.text
        if text == "瓜地馬拉 阿卡特南果":
            return True
        return False

    def on_enter_bitter_first(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑烤杏仁香氣\n☑入口後有紅李子、紅蘋果、奶油糖風味\n☑尾韻帶有糖紅感和杏仁香氣\n主風味:\n☑烤杏仁、紅李子、紅蘋果\n\n輸入【選單】以新重開啟選單")

    def is_going_to_bitter_second(self, event):
        text = event.message.text
        if text == "玻利維亞 卡杜拉":
            return True
        return False

    def on_enter_bitter_second(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑乾香帶有核桃、黑巧克力、黑糖糕的香氣\n☑入口後感受到甜棗、烤榛果的滑順口感\n☑尾韻帶有黑棗和紅糖的風味\n主風味:\n☑烤榛果、黑棗、紅糖\n\n輸入【選單】以新重開啟選單")

    def is_going_to_bitter_third(self, event):
        text = event.message.text
        if text == "宏都拉斯 帕拉伊內馬":
            return True
        return False

    def on_enter_bitter_third(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑香氣帶有烤榛果、仙楂以及橙皮\n☑入口後轉為酸甜的橘子、青蘋果\n☑尾韻環繞著紅糖的甜感和青蘋果的香氣\n主風味:\n☑青蘋果、橙皮、仙楂\n\n輸入【選單】以新重開啟選單")

    #state of sour
    def is_going_to_sour(self, event):
        text = event.message.text
        if text == '清爽':
            return True
        return False

    def on_enter_sour(self, event):
        title = '以下有三種豆子的推薦'
        text = '想選擇哪一款豆子查看風味描述呢'
        btn = [
            MessageTemplateAction(
                label = "衣索比亞 耶家雪菲",
                text = "衣索比亞 耶家雪菲"
            ),
            MessageTemplateAction(
                label = "巴拿馬 藝妓",
                text = "巴拿馬 藝妓"
            ),
            MessageTemplateAction(
                label = "瓜地馬拉 卡度艾",
                text = "瓜地馬拉 卡度艾"
            ),
        ]
        url = 'https://img.ltn.com.tw/Upload/food/page/2018/06/28/180628-7760-0-jYh8n.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_sour_first(self, event):
        text = event.message.text
        if text == "衣索比亞 耶家雪菲":
            return True
        return False

    def on_enter_sour_first(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑乾香帶有百香果、蜜餞、巧克力\n☑入口後可以感受到橘子、百香果以及滑順的口感\n☑尾韻環繞著紅櫻桃風味和可可香氣\n主風味:\n☑百香果、蜜餞、可可\n酸度:4分(由弱至強1~5)\n\n輸入【選單】以新重開啟選單")

    def is_going_to_sour_second(self, event):
        text = event.message.text
        if text == "巴拿馬 藝妓":
            return True
        return False

    def on_enter_sour_second(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑豐富的熱帶水果香氣，如白桃、百香果\n☑入口後有鳳梨、芒果以及其他熱帶水果的酸甜口感\n☑尾韻環繞著楓糖甜感和鳳梨果醬香氣\n主風味:\n☑百香果、鳳梨、楓糖\n酸度:3.5分(由弱至強1~5)\n\n輸入【選單】以新重開啟選單")

    def is_going_to_sour_third(self, event):
        text = event.message.text
        if text == "瓜地馬拉 卡度艾":
            return True
        return False

    def on_enter_sour_third(self, event):
        send_text_message(event.reply_token, "風味描述:\n☑香氣帶有紅葡萄柚、紅色莓果、蜜糖\n☑入口後感受到紅蘋果、葡萄風味、並帶有滑順的口感\n☑尾段環繞著葡萄風味和蜜糖甜感，並富有奶油糖香氣\n主風味:\n☑葡萄、紅葡萄柚、蜜糖\n酸度:3.5分(由弱至強1~5)\n\n輸入【選單】以新重開啟選單")

    #state of dessert
    def on_enter_cal_dessert(self, event):
        title = '甜點成分以及熱量'
        text = '請選擇甜點?'
        btn = [
            MessageTemplateAction(
                label = '布朗尼',
                text = '布朗尼'
            ),
            MessageTemplateAction(
                label = '馬芬',
                text = '馬芬'
            ),
            MessageTemplateAction(
                label = '司康',
                text = '司康'
            ),
            MessageTemplateAction(
                label = '手工軟餅乾',
                text = '手工軟餅乾'
            ),
        ]
        url = 'https://en.pimg.jp/069/869/417/1/69869417.jpg'
        send_button_message(event.reply_token, title, text, btn, url)      
       
    def is_going_to_brownie(self, event):
        text = event.message.text
        if text == '布朗尼':
           return True
        return  False

    def on_enter_brownie(self, event):
        text= "成分:巧克力磚、糖、低筋麵粉、糖、奶油、鮮奶、蛋\n熱量:約460大卡"
        url = 'https://www.foodnext.net/dispPageBox/getFile/GetImg.aspx?FileLocation=%2FPJ-FOODNEXT%2FFiles%2F&FileName=photo-03695-i.jpg'
        text1="輸入【選單】以重新開啟選單"
        send_text_image(event.reply_token, text, url, text1)

    def is_going_to_muffin(self, event):
        text = event.message.text
        if text == '馬芬':
           return True
        return  False

    def on_enter_muffin(self, event):
        text= "成分:麵粉、牛奶、奶油、蛋、糖、巧克力豆\n熱量:約390大卡"
        url = 'https://assets.tmecosys.com/image/upload/t_web767x639/img/recipe/ras/Assets/68dba1fc-cc29-461e-8c3c-540f91cbba14/Derivates/469d2c85-6dc3-4d05-8143-6dbeb56ad68c.jpg'
        text1="輸入【選單】以重新開啟選單"
        send_text_image(event.reply_token, text, url, text1)

    def is_going_to_scone(self, event):
        text = event.message.text
        if text == '司康':
           return True
        return  False

    def on_enter_scone(self, event):
        text= "成分:低筋麵粉、無鹽奶油、糖、無鋁泡打粉、檸檬汁、牛奶、蛋\n熱量:約280大卡"
        url = 'https://imageproxy.icook.network/resize?background=255%2C255%2C255&height=675&nocrop=false&stripmeta=true&type=auto&url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Frecipe%2Fcover%2F171742%2Ffaf56abad0160e97.jpg&width=1200'
        text1="輸入【選單】以重新開啟選單"
        send_text_image(event.reply_token, text, url, text1)

    def is_going_to_cookie(self, event):
        text = event.message.text
        if text == '手工軟餅乾':
           return True
        return  False

    def on_enter_cookie(self, event):
        text= "成分:蛋、60%德國巧克力、麵粉、糖、發酵奶油、小蘇打\n熱量:約250大卡"
        url = 'https://www.freemart.com.tw/file_manager/uimage/product/p00036567_l.jpg'
        text1="輸入【選單】以重新開啟選單"
        send_text_image(event.reply_token, text, url, text1)

    #state of introduction
    def on_enter_intro(self, event):
        text= "店家名稱:肥宅咖啡廳\n地址:台南市肥宅區肥宅路1段1號\n營業時間:每周六日10:00~18:00\n聯絡電話:0988888888\n店狗名字:阿呆"
        url = 'https://images.chinatimes.com/newsphoto/2020-10-28/656/20201028004982.jpg'
        text1="輸入【選單】以重新開啟選單"
        send_text_image(event.reply_token, text, url, text1)
        






"""


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
"""