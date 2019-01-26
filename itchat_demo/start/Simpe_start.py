#!/usr/bin/python
# -*- coding: UTF-8 -*-


import itchat, threading, requests, json, time
from flask import Flask
from flask import request
from multiprocessing import Process, Queue

"""消息类型常量"""
add_friend_request_type = 1  # 他人添加机器人为好友请求
msg_request_open_room = 2  # '开房'关键字请求待开房
msg_request_open_room_type = 3  # '开房'关键字请求获取房间类型
show_cfg_robot_open_room_type = 4  # 显示配置机器人开房类型
show_already_cfg_robot_open_room_type = 5  # 显示已配置机器人开房类型
show_robot_room_type_by_agent_mid = 6  # 根据代理商id查询机器人房间配置
exec_cfg_robot_room_type = 7  # 显示配置机器人开房类型

"""返回值常量"""
success = "success"
error = "error"
message = "message"
data = "data"

"""错误码比对表"""


def check_int(str):
    """检查字符串是否可以转int"""
    try:
        int(str)
        return True
    except:
        return False


# postUrl = 'http://192.168.1.128:8090/gdrobot/api/robot/sendMsgToJava.html'
postUrl = 'http://192.168.1.204:8080/robot/api/robot/sendMsgToJava.html'


def send_post_request_to_java(type=0, data=None):
    """发送请求到java app后台
        返回值是一个dict
    """
    if data is None:
        data = {}
    send_data = {'type': type, 'data': json.dumps(data)}
    response = requests.post(postUrl, data=send_data)
    j = json.loads(response.text)
    return j


# @itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
# def text_reply(msg):  # Note 通知类型，比如添加好友成功后，会收到好友界面的系统的通知:"你已经成功添加了xx为好友，现在可以开始聊天"
    # print('Text', 'Map', 'Card', 'Note', 'Sharing ---::', msg['Type'], msg['Text'], msg)
    # itchat.send('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])


@itchat.msg_register('Text')
def private_chat(msg):
    print(msg)
    text = msg['Text']
    texts = text.split('+', 2)
    if text == '配置':# 显示当前代理商所有已经配置的房间配置
        agent = itchat.search_friends(userName=msg['FromUserName'])
        if agent is not None and agent != '':
            nn = agent['RemarkName']
            rens = nn.split('_', 2)
            if nn.startswith('QS_') and len(rens) == 3 and check_int(rens[1]) and check_int(rens[2]):
                robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
                d = {"code": str(rens[1]), "amid": str(rens[2]), "msgid": str(msg['MsgId']), "robName": robot_nickname}
                rd = send_post_request_to_java(show_cfg_robot_open_room_type, data=d)
                try:
                    rr = eval(rd)
                except:
                    rr = rd
                if int(rr[success]) == 1:  # 成功
                    itchat.send(rr[data], msg['FromUserName'])
    elif text == '查看':# 查看代理商已经配置当前机器人对应的玩法配置
        agent = itchat.search_friends(userName=msg['FromUserName'])
        if agent is not None and agent != '':
            nn = agent['RemarkName']
            rens = nn.split('_', 2)
            if nn.startswith('QS_') and len(rens) == 3 and check_int(rens[1]) and check_int(rens[2]):
                robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
                d = {"code": str(rens[1]), "amid": str(rens[2]), "msgid": str(msg['MsgId']), "robName": robot_nickname}
                rd = send_post_request_to_java(show_already_cfg_robot_open_room_type, data=d)
                try:
                    rr = eval(rd)
                except:
                    rr = rd
                if int(rr[success]) == 1:  # 成功
                    itchat.send(rr[data], msg['FromUserName'])
    elif check_int(text):# 查看指定房间类型中所有自己类型配置
        agent = itchat.search_friends(userName=msg['FromUserName'])
        if agent is not None and agent != '':
            nn = agent['RemarkName']
            rens = nn.split('_', 2)
            if nn.startswith('QS_') and len(rens) == 3 and check_int(rens[1]) and check_int(rens[2]):
                robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
                d = {"code": str(rens[1]), "amid": str(rens[2]), "msgid": str(msg['MsgId']), "robName": robot_nickname
                     , "roomType": str(text)}
                rd = send_post_request_to_java(show_robot_room_type_by_agent_mid, data=d)
                try:
                    rr = eval(rd)
                except:
                    rr = rd
                if int(rr[success]) == 1:  # 成功
                    itchat.send(rr[data], msg['FromUserName'])
    elif len(texts) == 2 and check_int(texts[0]) and check_int(texts[1]):# 保存机器人新的玩法配置
        agent = itchat.search_friends(userName=msg['FromUserName'])
        if agent is not None and agent != '':
            nn = agent['RemarkName']
            rens = nn.split('_', 2)
            if nn.startswith('QS_') and len(rens) == 3 and check_int(rens[1]) and check_int(rens[2]):
                robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
                d = {"code": str(rens[1]), "amid": str(rens[2]), "msgid": str(msg['MsgId']), "robName": robot_nickname
                    , "roomType": str(texts[0]), "subset": str(texts[1])}
                rd = send_post_request_to_java(exec_cfg_robot_room_type, data=d)
                try:
                    rr = eval(rd)
                except:
                    rr = rd
                if int(rr[success]) == 1:  # 成功
                    itchat.send(rr[data], msg['FromUserName'])
    else:
        itchat.send('''您好，欢迎使用乐玩开房神器！\n
        如果你要配置该机器人开的房间类型，请输入\"配置\""\n
        如果你要查看该机器人已配置的房间类型，请输入\"查看\"''', msg['FromUserName'])


@itchat.msg_register('Friends')
def add_friend(msg):
    valify_msg = msg['Text']['autoUpdate']['Content']  # 验证消息格式：auth_code+mid，amid+dmid
    li = valify_msg.split('+', 1)
    if len(li) == 2 and check_int(li[0]) and check_int(li[1]):
        robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
        d = {"authCode": str(li[0]), "mid": str(li[1]), "robName": robot_nickname}
        rd = send_post_request_to_java(type=add_friend_request_type, data=d)  # result
        print(rd)
        if int(rd[success]) == 1:  # 成功
            itchat.add_friend(userName=msg['RecommendInfo']['UserName'], status=3)  # 同意加为好友
            add_name = rd[data]['name']
            # itchat.send_msg(add_name + ":感谢您加我为好友！" + '我的名字叫：' + robot_nickname, msg['RecommendInfo']['UserName'])
            itchat.send_msg('您好；机器人代开房授权成功！欢迎使用牵手开房神器。\n\n'
                            + '按如下操作，即可开通服务；\n'
                            + '1.打开游戏客户端，找到机器人开房配置进行配置\n'
                            + '2.私聊机器人，发送“配置”，即可看到所有的房间类型\n'
                            + '3.根据机器人返回消息提示，完成对该机器人的配置\n'
                            + '4.在群中编辑发送“开心”，即可开房。', msg['RecommendInfo']['UserName'])
            itchat.set_alias(userName=msg['RecommendInfo']['UserName'],
                             alias="QS_" + str(li[0]) + "_" + str(li[1]))  # 修改备注名称
        else:
            print(int(rd[error]))
    else:
        print("msg not match !")


@itchat.msg_register('Text', isGroupChat=True)
def text_reply(msg):
    print(msg)
    # try:
    #     qunzhuUserName = msg['User']['ChatRoomOwner']
    # except:
    #     pass
    # d = send_post_request_to_java(type=1, data={'name1': 'value1', 'name2': 'value2'})
    # print(d['name1'])
    # qunzhuUserName = msg['User']['MemberList'][0]['UserName']
    # print(itchat.update_friend(userName=qunzhuUserName))
    # print(itchat.search_friends(userName=qunzhuUserName))
    # print(itchat.get_friends(update=True)) # 机器人更新好友列表
    # print(itchat.get_chatrooms(update=True)) # 机器人更新群列表
    # frindLists = itchat.get_friends(update=True)
    # itchat.set_alias(userName=qunzhuUserName, alias="Saywewe555416461646461646946164646163465461641646464646464676761") # 修改备注名称
    # frindLists = itchat.get_friends()
    # for frind in frindLists:
    #     if frind['UserName'] == qunzhuUserName:
    #         print(frind['RemarkName'])
    # if str(msg['Content']) == 'aa':
    #     prefix = "请点击此链接完成待开房："
    #     print('robot send message by key word ::机器人开房')
    #     itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], prefix + javaCallBackUrl + '?fun=' + msg['FromUserName']),
    #                 msg['FromUserName'])
    # if msg['isAt']:
    #     itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])
    #     if str(msg['Content']).find("开房") > 0:
    #         prefix = "请点击此链接完成待开房："
    #         print('robot send message by at me ::开房')
    #         itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], prefix + javaCallBackUrl + '?fun=' + msg['FromUserName']),msg['FromUserName'])

    # if str(msg['Content']) == '开房':
    #     frindLists = itchat.get_friends()
    #     for frind in frindLists:
    #         print(frind['UserName'],msg['ActualUserName'],msg['User']['ChatRoomOwner'])
    #         if frind['UserName'] == msg['ActualUserName']:
    #             remark_name = frind['RemarkName']
    #             li = remark_name.split('_', 2)
    #             if remark_name.startswith('QS_') and len(li) == 3 and check_int(li[1]) and check_int(li[2]):
    #                 robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
    #                 d = {"amid": str(li[1]), "mid": str(li[2]), "msgid": str(msg['MsgId']), "robName": robot_nickname}
    #                 rd = send_post_request_to_java(msg_request_open_room, data=d)
    #                 print(rd)

    if str(msg['Content']) == '开心':
        try:
            qunzhuUserName = msg['User']['ChatRoomOwner']
        except:
            qunzhuUserName = '0'
        qunzhu = itchat.search_friends(userName=qunzhuUserName)
        if qunzhu is not None and qunzhu != '':
            qunzhu_rn = qunzhu['RemarkName']
            qunzhu_li = qunzhu_rn.split('_', 2)
            if qunzhu_rn.startswith('QS_') and len(qunzhu_li) == 3 and check_int(qunzhu_li[1]) and check_int(qunzhu_li[2]):
                    robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
                    d = {"code": str(qunzhu_li[1]), "amid": str(qunzhu_li[2]), "msgid": str(msg['MsgId']),"robName": robot_nickname}
                    rd = send_post_request_to_java(msg_request_open_room, data=d)
                    print('has ChatRoomOwner response type ', rd)
                    try:
                        rr = eval(rd)
                    except:
                        rr = rd
                    if int(rr[success]) == 1:  # 成功
                        itchat.send(rr[data], msg['FromUserName'])
        else:
            robot_nickname = itchat.search_friends(userName=msg['ToUserName'])['NickName']
            for member in msg['User']['MemberList']:
                m = itchat.search_friends(userName=member['UserName'])
                if m is not None and m != '':
                    rename = m['RemarkName']
                    rens = rename.split('_', 2)
                    if rename.startswith('QS_') and len(rens) == 3 and check_int(rens[1]) and check_int(rens[2]):
                        d = {"code": str(rens[1]), "amid": str(rens[2]), "msgid": str(msg['MsgId']),"robName": robot_nickname}
                        rd = send_post_request_to_java(msg_request_open_room, data=d)
                        print('not has ChatRoomOwner response type ', rd)
                        try:
                            rr = eval(rd)
                        except:
                            rr = rd
                        if int(rr[success]) == 1:  # 成功
                            itchat.send('开房成功！点击此链接加入房间：' + rr[data], msg['FromUserName'])
                            break


def itchatProcess():
    # itchat.auto_login(enableCmdQR=True, hotReload=True)
    itchat.auto_login(enableCmdQR=True)
    # itchat.auto_login(enableCmdQR=2, hotReload=True)linux下打开控制台扫描
    itchat.run()


"""web web web web web web web web web web web web web web web web web web web  应用开始"""
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    print(itchat.search_friends())
    print(itchat.search_mps)
    print(itchat.search_chatrooms)
    return '<h1>Home</h1>'


# 客户端发送的是   content={json}类型的数据
@app.route('/sendOpenRoomResult.html', methods=['POST'])
def signin():
    immutableMultiDict = request.form
    v1 = immutableMultiDict.get('goldNum', default='')
    v2 = immutableMultiDict.get('sendType', default='')
    v3 = immutableMultiDict.get('signCode', default='')
    print(v1, v2, v3)
    # itchat.send_msg(msg="ddddddddddddd",toUserName="@@f799308a6aa2dd35c42d0f05258e4fc1b6bb98c5faf36140865ac6493b64a726")
    return ''


def webProcess():
    app.run(port=5555)


"""web web web web web web web web web web web web web web web web web web web  应用结束"""

if __name__ == '__main__':
    t1 = threading.Thread(target=itchatProcess, name='Thread-A')
    # t2 = threading.Thread(target=webProcess, name='Thread-B')
    t1.start()
    # t2.start()
    t1.join()
    # t2.join()
