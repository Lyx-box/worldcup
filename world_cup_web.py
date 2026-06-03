# -*- coding: utf-8 -*-
import streamlit as st
import sys
import random

# 全局变量提前在最顶部定义，彻底避开global报错
player_stat = {}
player_nation_map = {}

# 2026世界杯12小组分组
GROUP_DATA = {
    "A": ["墨西哥", "南非", "韩国", "捷克"],
    "B": ["加拿大", "波黑", "卡塔尔", "瑞士"],
    "C": ["巴西", "摩洛哥", "海地", "苏格兰"],
    "D": ["美国", "巴拉圭", "澳大利亚", "土耳其"],
    "E": ["德国", "库拉索", "科特迪瓦", "厄瓜多尔"],
    "F": ["荷兰", "日本", "瑞典", "突尼斯"],
    "G": ["比利时", "埃及", "伊朗", "新西兰"],
    "H": ["西班牙", "佛得角", "沙特阿拉伯", "乌拉圭"],
    "I": ["法国", "塞内加尔", "伊拉克", "挪威"],
    "J": ["阿根廷", "阿尔及利亚", "奥地利", "约旦"],
    "K": ["葡萄牙", "刚果（金）", "乌兹别克斯坦", "哥伦比亚"],
    "L": ["英格兰", "克罗地亚", "加纳", "巴拿马"]
}

TEAM_INFO = {
    "墨西哥": {"power":7.2, "gk":"奥乔亚", "players":{"洛萨诺":["FW",8.0,False],"劳尔·希门尼斯":["FW",7.5,False],"阿尔瓦雷斯":["MF",7.5,False],"皮内达":["MF",6.5,False],"安图尼亚":["FW",6.7,False],"桑切斯":["DF",6.8,False]}},
    "南非": {"power":5.1, "gk":"威廉姆斯", "players":{"福斯特":["FW",5.5,False],"莫科纳":["DF",5.2,False],"莫雷纳":["MF",4.9,False],"兹瓦内":["FW",4.7,False],"马沙巴":["DF",4.5,False]}},
    "韩国": {"power":6.3, "gk":"赵贤祐", "players":{"孙兴慜":["FW",8.5,False],"李刚仁":["MF",7.6,False],"黄义助":["FW",7.0,False],"金玟哉":["DF",7.8,False],"郑优营":["MF",6.8,False],"黄喜灿":["FW",7.2,False]}},
    "捷克": {"power":5.8, "gk":"帕夫伦卡", "players":{"希克":["FW",7.3,False],"绍切克":["MF",6.9,False],"曹法尔":["DF",6.5,False],"扬克托":["MF",6.2,False],"希卢斯":["FW",6.0,False]}},
    "加拿大": {"power":5.9, "gk":"克雷波", "players":{"阿方索·戴维斯":["DF",8.2,False],"戴维":["FW",7.1,False],"布坎南":["FW",6.5,False],"欧斯塔基奥":["MF",6.3,False],"哈钦森":["MF",6.0,False]}},
    "波黑": {"power":5.3, "gk":"塞西奇", "players":{"哲科":["FW",6.7,False],"皮亚尼奇":["MF",6.2,False],"科拉希纳茨":["DF",6.0,False],"德米罗维奇":["FW",5.8,False]}},
    "卡塔尔": {"power":4.8, "gk":"巴尔沙姆", "players":{"阿菲夫":["FW",6.2,False],"阿里":["FW",5.8,False],"海多斯":["MF",5.5,False],"哈桑":["DF",5.2,False]}},
    "瑞士": {"power":6.9, "gk":"科贝尔", "players":{"扎卡":["MF",7.2,False],"阿坎吉":["DF",7.4,False],"沙奇里":["MF",7.0,False],"恩博洛":["FW",6.8,False],"弗罗伊勒":["MF",6.5,False]}},
    "巴西": {"power":9.1, "gk":"阿利松", "players":{"维尼修斯":["FW",9.2,False],"拉菲尼亚":["FW",8.7,False],"内马尔":["FW",8.8,True],"恩德里克":["FW",8.2,False],"马丁内利":["FW",8.3,False],"卡塞米罗":["MF",8.5,False],"吉马良斯":["MF",8.4,False],"马尔基尼奥斯":["DF",8.6,False],"库尼亚":["FW",7.8,False],"伊戈尔·蒂亚戈":["FW",7.5,False]}},
    "摩洛哥": {"power":7.0, "gk":"布努", "players":{"阿什拉夫":["DF",7.9,False],"布拉欣·迪亚斯":["MF",7.5,False],"马兹拉维":["DF",7.0,False],"阿姆拉巴特":["MF",7.2,False]}},
    "海地": {"power":3.6, "gk":"普拉西德", "players":{"皮埃尔":["FW",4.2,False],"约瑟夫":["MF",3.9,False],"让":["DF",3.7,False]}},
    "苏格兰": {"power":5.7, "gk":"戈登", "players":{"罗伯逊":["DF",7.3,False],"麦克托米奈":["MF",6.8,False],"蒂尔尼":["DF",6.5,False],"亚当斯":["FW",6.2,False]}},
    "美国": {"power":6.6, "gk":"特纳", "players":{"普利西奇":["FW",8.3,False],"麦肯尼":["MF",7.2,False],"德斯特":["DF",6.8,False],"巴洛贡":["FW",7.0,False],"小维阿":["FW",6.5,False]}},
    "巴拉圭": {"power":4.5, "gk":"席尔瓦", "players":{"阿尔米隆":["MF",6.1,False],"恩西索":["FW",5.9,False],"巴尔武埃纳":["DF",5.5,False]}},
    "澳大利亚": {"power":5.2, "gk":"瑞安", "players":{"伊兰昆达":["FW",6.0,False],"莱基":["FW",5.8,False],"穆伊":["MF",5.5,False],"苏塔":["DF",5.6,False]}},
    "土耳其": {"power":6.1, "gk":"居诺克", "players":{"居莱尔":["MF",7.5,False],"恰尔汗奥卢":["MF",6.7,False],"瑟云聚":["DF",6.5,False],"云代尔":["FW",6.3,False],"伊尔迪兹":["MF",7.2,False]}},
    "德国": {"power":9.0, "gk":"诺伊尔", "players":{"穆西亚拉":["MF",9.2,False],"维尔茨":["MF",8.9,False],"哈弗茨":["FW",8.6,False],"基米希":["MF",8.9,False],"吕迪格":["DF",8.4,False],"萨内":["FW",8.3,False]}},
    "库拉索": {"power":3.3, "gk":"罗梅罗", "players":{"库伊珀":["MF",3.9,False],"巴库纳":["DF",3.7,False],"胡拉多":["FW",3.5,False],"陈达毅":["FW",3.8,False]}},
    "科特迪瓦": {"power":6.4, "gk":"阿里", "players":{"阿莱":["FW",7.8,False],"凯西":["MF",7.5,False],"拜利":["DF",7.2,False],"扎哈":["FW",7.0,False],"恩迪卡":["DF",7.3,False]}},
    "厄瓜多尔": {"power":5.6, "gk":"多明戈斯", "players":{"恩内尔·瓦伦西亚":["FW",7.0,False],"凯塞多":["MF",6.8,False],"埃斯图皮尼安":["DF",6.5,False],"帕乔":["DF",6.3,False],"因卡皮耶":["DF",6.4,False]}},
    "荷兰": {"power":8.7, "gk":"弗莱肯", "players":{"德容":["MF",8.5,False],"加克波":["FW",9.0,False],"范戴克":["DF",8.8,False],"德利赫特":["DF",8.4,False],"德佩":["FW",8.2,False],"邓弗里斯":["DF",7.9,False]}},
    "日本": {"power":6.7, "gk":"权田修一", "players":{"三笘薫":["FW",8.4,False],"久保建英":["MF",7.9,False],"富安健洋":["DF",7.5,False],"南野拓实":["FW",7.2,False],"远藤航":["MF",7.0,False],"堂安律":["FW",7.1,False]}},
    "瑞典": {"power":5.9, "gk":"奥尔森", "players":{"伊萨克":["FW",7.7,False],"福斯贝里":["MF",7.2,False],"林德洛夫":["DF",7.0,False],"库卢塞夫斯基":["FW",6.8,False],"哲凯赖什":["FW",7.5,False]}},
    "突尼斯": {"power":5.0, "gk":"达门", "players":{"哈兹里":["FW",6.0,False],"姆萨克尼":["MF",5.7,False],"布龙":["DF",5.5,False],"汉尼拔·梅布里":["MF",5.8,False]}},
    "比利时": {"power":8.2, "gk":"库尔图瓦", "players":{"德布劳内":["MF",9.1,False],"卢卡库":["FW",8.3,False],"多库":["FW",7.8,False],"蒂勒曼斯":["MF",7.5,False],"阿马杜·奥纳纳":["MF",7.2,False]}},
    "埃及": {"power":5.5, "gk":"阿布加巴尔", "players":{"萨拉赫":["FW",8.5,False],"埃尔内尼":["MF",6.2,False],"赫加齐":["DF",6.0,False],"特雷泽盖":["FW",5.8,False],"马尔穆什":["FW",6.3,False]}},
    "伊朗": {"power":5.3, "gk":"贝兰万德", "players":{"塔雷米":["FW",7.1,False],"贾汉巴赫什":["MF",6.5,False],"雷扎扬":["DF",5.8,False]}},
    "新西兰": {"power":3.2, "gk":"奥基夫", "players":{"伍德":["FW",4.0,False],"鲁费":["MF",3.7,False],"史密斯":["DF",3.5,False]}},
    "西班牙": {"power":9.4, "gk":"乌奈·西蒙", "players":{"罗德里":["MF",9.0,False],"佩德里":["MF",9.0,False],"亚马尔":["FW",8.9,False],"加维":["MF",8.9,False],"莫拉塔":["FW",8.2,False],"拉波尔特":["DF",8.4,False]}},
    "佛得角": {"power":3.5, "gk":"维尔吉利奥", "players":{"门德斯":["MF",4.1,False],"塔瓦雷斯":["DF",3.9,False],"里贝罗":["FW",3.7,False]}},
    "沙特阿拉伯": {"power":4.2, "gk":"奥韦斯", "players":{"多萨里":["MF",5.9,False],"谢赫里":["FW",5.5,False],"布莱克":["DF",5.2,False]}},
    "乌拉圭": {"power":7.6, "gk":"罗切特", "players":{"努涅斯":["FW",8.7,False],"巴尔韦德":["MF",8.4,False],"本坦库尔":["MF",7.8,False],"阿劳霍":["DF",8.2,False],"希门尼斯":["DF",7.5,False]}},
    "法国": {"power":9.2, "gk":"迈尼昂", "players":{"姆巴佩":["FW",9.6,False],"登贝莱":["FW",8.6,False],"奥利塞":["FW",8.2,False],"楚阿梅尼":["MF",9.0,False],"坎特":["MF",8.5,False],"扎伊尔-埃梅里":["MF",8.3,False],"于帕梅卡诺":["DF",8.3,False],"孔德":["DF",8.5,False]}},
    "塞内加尔": {"power":7.1, "gk":"门迪", "players":{"马内":["FW",8.2,False],"库利巴利":["DF",7.8,False],"盖耶":["MF",7.5,False],"迪亚":["FW",7.2,False]}},
    "伊拉克": {"power":3.8, "gk":"哈米德", "players":{"阿里":["FW",4.5,False],"阿卜杜勒拉希姆":["MF",4.2,False],"哈桑":["DF",4.0,False]}},
    "挪威": {"power":7.3, "gk":"尼兰德", "players":{"哈兰德":["FW",9.4,False],"厄德高":["MF",8.8,False],"索尔洛特":["FW",7.5,False],"金特尔":["DF",7.0,False]}},
    "阿根廷": {"power":9.3, "gk":"大马丁", "players":{"梅西":["FW",9.3,False],"阿尔瓦雷斯":["FW",9.1,False],"恩佐·费尔南德斯":["MF",8.7,False],"麦卡利斯特":["MF",8.5,False],"德保罗":["MF",8.2,False],"罗梅罗":["DF",8.4,False],"劳塔罗·马丁内斯":["FW",8.8,False]}},
    "阿尔及利亚": {"power":6.2, "gk":"姆博利", "players":{"马赫雷斯":["FW",7.9,False],"本拉赫马":["FW",7.2,False],"曼迪":["DF",6.8,False],"费古利":["MF",6.5,False]}},
    "奥地利": {"power":5.4, "gk":"巴赫曼", "players":{"阿瑙托维奇":["FW",6.5,False],"阿拉巴":["DF",7.0,False],"萨比策":["MF",6.7,False]}},
    "约旦": {"power":3.1, "gk":"阿卜杜拉", "players":{"塔马里":["FW",3.8,False],"马尔迪":["MF",3.5,False],"扎伊德":["DF",3.3,False]}},
    "葡萄牙": {"power":9.0, "gk":"迪奥戈·科斯塔", "players":{"C罗":["FW",8.5,False],"莱奥":["FW",9.2,False],"B费":["MF",8.8,False],"B席":["MF",8.6,False],"鲁本·迪亚斯":["DF",8.9,False],"坎塞洛":["DF",8.3,False]}},
    "刚果（金）": {"power":5.1, "gk":"姆帕萨", "players":{"卢卡库（刚果）":["FW",6.3,False],"姆本巴":["DF",6.0,False],"马苏阿库":["DF",5.8,False]}},
    "乌兹别克斯坦": {"power":3.4, "gk":"内马托夫", "players":{"肖穆罗多夫":["FW",4.3,False],"哈姆罗别科夫":["MF",4.0,False],"赛义菲耶夫":["DF",3.8,False]}},
    "哥伦比亚": {"power":6.5, "gk":"奥斯皮纳", "players":{"哈梅斯·罗德里格斯":["MF",7.8,False],"法尔考":["FW",7.2,False],"米纳":["DF",7.0,False],"夸德拉多":["DF",6.8,False]}},
    "英格兰": {"power":9.3, "gk":"皮克福德", "players":{"凯恩":["FW",9.5,False],"贝林厄姆":["MF",9.5,False],"萨卡":["FW",9.0,False],"福登":["MF",8.8,False],"阿诺德":["DF",8.2,False],"马奎尔":["DF",7.8,False]}},
    "克罗地亚": {"power":7.8, "gk":"利瓦科维奇", "players":{"莫德里奇":["MF",8.6,False],"布罗佐维奇":["MF",7.9,False],"科瓦契奇":["MF",7.7,False],"克拉马里奇":["FW",7.5,False]}},
    "加纳": {"power":5.8, "gk":"努鲁德恩", "players":{"阿尤":["FW",6.9,False],"托马斯":["MF",7.2,False],"帕尔特伊":["MF",6.8,False],"库杜斯":["FW",6.5,False]}},
    "巴拿马": {"power":3.7, "gk":"梅希亚", "players":{"戈多伊":["MF",4.4,False],"罗德里格斯":["FW",4.1,False],"戴维斯":["DF",3.9,False]}}
}

def get_available_players(team_name, is_knockout=False):
    info = TEAM_INFO[team_name]
    field_players = []
    gk_name = info["gk"]
    if gk_name not in player_nation_map:
        player_nation_map[gk_name] = team_name
    if gk_name not in player_stat:
        player_stat[gk_name] = [0,0,0,0,0,0,"GK",team_name,False]
    for name, (pos, val, injured) in info["players"].items():
        if injured and not is_knockout:
            continue
        if name == "梅西" and is_knockout and random.random() < 0.3:
            continue
        field_players.append((name, pos, val, False))
        player_nation_map[name] = team_name
        if name not in player_stat:
            player_stat[name] = [0,0,0,0,0,0,pos,team_name,False]
    sub_count = 1
    while len(field_players) < 11:
        sub_name = f"{team_name}替补{sub_count}"
        pos = random.choice(["FW","MF","DF"])
        avg_power = info["power"] / 1.2
        val = round(random.uniform(avg_power-1.5, avg_power-1.0),1)
        field_players.append((sub_name, pos, val, True))
        player_nation_map[sub_name] = team_name
        if sub_name not in player_stat:
            player_stat[sub_name] = [0,0,0,0,0,0,pos,team_name,True]
        sub_count +=1
    return field_players, gk_name

def calc_team_goals(team_power, team_name, is_knockout=False):
    base_goal = team_power / 13.0
    field,_ = get_available_players(team_name, is_knockout)
    top_fw = max([v for n,p,v,_ in field if p=="FW"], default=0)
    if top_fw >=9.0:
        base_goal *=1.08
    if is_knockout:
        base_goal *=0.9
    final = max(0, round(random.triangular(0, base_goal*2.8, base_goal*1.4)))
    return final

def assign_goals(team_name, total_g, is_knockout=False):
    field,_ = get_available_players(team_name,is_knockout)
    scorers = []
    assists = []
    w_list = []
    for n,p,v,sub in field:
        if player_stat[n][0]>=5:
            continue
        w = (v**2)*(3.2 if p=="FW" else 0.9 if p=="MF" else 0.08)*(0.5 if sub else 1)
        w_list.append((n,w))
    total_w = sum(w for _,w in w_list) if w_list else 1
    for _ in range(total_g):
        r = random.uniform(0,total_w)
        cur=0
        sc=""
        for name,w in w_list:
            cur+=w
            if cur>=r:
                sc=name
                break
        scorers.append(sc)
        player_stat[sc][0]+=1
        if total_g>=2 and random.random()<0.5 and len(w_list)>=2:
            pool=[n for n,_ in w_list if n!=sc]
            ast=random.choice(pool)
            assists.append(ast)
            player_stat[ast][1]+=1
    return scorers,assists

def calc_rating(team,concede,is_ko=False):
    info=TEAM_INFO[team]
    field,gk=get_available_players(team,is_ko)
    p=info["power"]
    if p>=8.5:
        sv=random.randint(1,3)
    elif p>=6.0:
        sv=random.randint(1,2)
    else:
        sv=random.randint(2,3)
    cs=1 if concede==0 else 0
    player_stat[gk][3]+=1
    player_stat[gk][4]+=sv
    player_stat[gk][5]+=cs
    gr=round(random.uniform(6.0,8.9),1)
    player_stat[gk][2]+=gr
    rt={}
    rt["GK"]=(gk,gr,sv)
    for n,p,v,sub in field:
        player_stat[n][3]+=1
        base=random.uniform(5.4,8.6)
        pen=0.3 if sub else 0
        add=player_stat[n][0]*0.2
        fin=round(min(9.5,base+add-pen),1)
        player_stat[n][2]+=fin
        rt[n]=fin
    return rt

def penalty(home,away):
    f1,_=get_available_players(home,True)
    f2,_=get_available_players(away,True)
    k1=[n for n,_,_,_ in f1]
    k2=[n for n,_,_,_ in f2]
    maxk=min(5,len(k1),len(k2))
    s1=s2=0
    res=[]
    res.append(f"\n===={home} VS {away} 点球大战（进球不计金靴）====")
    for i in range(maxk):
        if random.random()<0.74:
            s1+=1
            res.append(f"{home}：{k1[i]} 命中")
        else:
            res.append(f"{home}：{k1[i]} 射失")
        if random.random()<0.74:
            s2+=1
            res.append(f"{away}：{k2[i]} 命中")
        else:
            res.append(f"{away}：{k2[i]} 射失")
    while s1==s2:
        kk1=random.choice(k1)
        kk2=random.choice(k2)
        h1=random.random()<0.7
        h2=random.random()<0.7
        if h1:s1+=1
        if h2:s2+=1
        res.append(f"突然死亡：{kk1}{'命中'if h1 else '射失'}，{kk2}{'命中'if h2 else '射失'}")
    res.append(f"点球比分：{home} {s1}:{s2} {away}\n")
    win=home if s1>s2 else away
    return win,"\n".join(res)

def sim_match(h,a,isk=False,ft=None):
    p1=TEAM_INFO[h]["power"]
    p2=TEAM_INFO[a]["power"]
    g1=calc_team_goals(p1,h,isk)
    g2=calc_team_goals(p2,a,isk)
    sc1,as1=assign_goals(h,g1,isk)
    sc2,as2=assign_goals(a,g2,isk)
    rt1=calc_rating(h,g2,isk)
    rt2=calc_rating(a,g1,isk)
    out=[]
    out.append(f"【赛果】{h} {g1}:{g2} {a}")
    out.append(f"{h}门将：{rt1['GK'][0]}｜扑救{rt1['GK'][2]}｜评分{rt1['GK'][1]}")
    out.append(f"{a}门将：{rt2['GK'][0]}｜扑救{rt2['GK'][2]}｜评分{rt2['GK'][1]}")
    if g1>0:out.append(f"{h}进球：{sc1}｜助攻：{as1 if as1 else '无'}")
    if g2>0:out.append(f"{a}进球：{sc2}｜助攻：{as2 if as2 else '无'}")
    if ft in (h,a):
        txt="胜" if (g1>g2 and ft==h) or (g2>g1 and ft==a) else "平"
        out.append(f"★追踪球队{ft}本场：{txt}")
    if isk and g1==g2:
        w,ptxt=penalty(h,a)
        out.append(ptxt)
        return w,g1,g2,"\n".join(out)
    win=h if g1>g2 else a if g2>g1 else None
    return win,g1,g2,"\n".join(out)

def sim_group(gname,teams,ft):
    tbl={n:{"W":0,"D":0,"L":0,"GF":0,"GA":0,"PTS":0} for n in teams}
    fix=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    out=[f"\n=========={gname}组小组赛=========="]
    for i,j in fix:
        ta,tb=teams[i],teams[j]
        w,g1,g2,rt=sim_match(ta,tb,False,ft)
        out.append(rt)
        tbl[ta]["GF"]+=g1
        tbl[ta]["GA"]+=g2
        tbl[tb]["GF"]+=g2
        tbl[tb]["GA"]+=g1
        if w==ta:
            tbl[ta]["W"]+=1
            tbl[ta]["PTS"]+=3
            tbl[tb]["L"]+=1
        elif w==tb:
            tbl[tb]["W"]+=1
            tbl[tb]["PTS"]+=3
            tbl[ta]["L"]+=1
        else:
            tbl[ta]["D"]+=1
            tbl[ta]["PTS"]+=1
            tbl[tb]["D"]+=1
            tbl[tb]["PTS"]+=1
    sort_t=sorted(tbl.items(),key=lambda x:(-x[1]["PTS"],-(x[1]["GF"]-x[1]["GA"]),-x[1]["GF"]))
    out.append(f"\n【{gname}积分榜】")
    out.append(f"名次{'':<8}队伍{'':<8}胜{'':<3}平{'':<3}负{'':<3}进球{'':<4}失球{'':<4}净胜{'':<4}积分")
    for idx,(n,d) in enumerate(sort_t,1):
        gd=d["GF"]-d["GA"]
        out.append(f"{idx:<4}{n:<12}{d['W']:<4}{d['D']:<4}{d['L']:<4}{d['GF']:<5}{d['GA']:<5}{gd:<5}{d['PTS']:<4}")
    top2=[sort_t[0][0],sort_t[1][0]]
    third=(sort_t[2][0],sort_t[2][1]["PTS"],sort_t[2][1]["GF"]-sort_t[2][1]["GA"],sort_t[2][1]["GF"])
    out.append(f"{gname}出线：{top2}｜小组第三：{third[0]}")
    return top2,third,"\n".join(out)

def get_32(all_res):
    direct=[]
    third_list=[]
    for top2,th,_ in all_res:
        direct.extend(top2)
        third_list.append(th)
    third_list.sort(key=lambda x:(-x[1],-x[2],-x[3]))
    out=f"\n====淘汰第三淘汰：{[t[0] for t in third_list[8:]]}"
    adv3=[t[0] for t in third_list[:8]]
    return direct+adv3,out

def sim_knockout(t32,ft):
    rounds=["1/32决赛(32进16)","1/8决赛(16进8)","1/4决赛(8进4)","半决赛(4进2)","决赛(争冠)"]
    curr=t32.copy()
    semi=[]
    all_out=[]
    for rd in rounds:
        all_out.append(f"\n=========={rd}==========")
        win_list=[]
        for i in range(0,len(curr),2):
            t1,t2=curr[i],curr[i+1]
            w,_,_,rt=sim_match(t1,t2,True,ft)
            all_out.append(rt)
            win_list.append(w)
            if ft in (t1,t2) and w!=ft:
                all_out.append(f"★{ft}止步{rd}")
            if rd=="半决赛(4进2)":
                lose=t2 if w==t1 else t1
                semi.append(lose)
        curr=win_list
    all_out.append("\n==========三四名决赛==========")
    third,_,_,rt=sim_match(semi[0],semi[1],True,ft)
    all_out.append(rt)
    champ=curr[0]
    all_out.append(f"\n🏆冠军：{champ}｜🥉季军：{third}")
    return champ,third,"\n".join(all_out)

def award_text():
    boot=[]
    ball=[]
    glove=[]
    for n,(g,a,sc,pl,sv,cs,pos,nat,sub) in player_stat.items():
        if pl==0:continue
        avg=round(sc/pl,2)
        boot.append((-g,-a,pl,n,g,a,nat))
        ball.append((-avg,n,avg,nat))
        if pos=="GK":
            glove.append((-cs,-sv,n,cs,sv,nat))
    boot.sort()
    ball.sort()
    glove.sort()
    res=["\n"+"="*80,"        三大奖项(点球进球不计入金靴)","="*80]
    res.append("\n🥇金靴｜进球｜助攻｜国籍")
    for idx,(_,_,_,n,g,a,nat) in enumerate(boot[:10],1):
        res.append(f"{idx:<3}{n:<18}{g:<5}{a:<5}{nat}")
    res.append("\n🏆金球｜场均评分｜国籍")
    for idx,(_,n,avg,nat) in enumerate(ball[:10],1):
        res.append(f"{idx:<3}{n:<18}{avg:<7}{nat}")
    res.append("\n🧤金手套｜零封｜总扑救｜国籍")
    for idx,(_,_,n,cs,sv,nat) in enumerate(glove[:8],1):
        res.append(f"{idx:<3}{n:<18}{cs:<5}{sv:<5}{nat}")
    res.append("="*80)
    return "\n".join(res)

# 网页主体
st.set_page_config(page_title="2026世界杯模拟器",layout="wide")
st.title("🏆2026美加墨世界杯模拟器")
all_team=[]
for v in GROUP_DATA.values():
    all_team.extend(v)
sel=st.selectbox("选择追踪球队",all_team,index=all_team.index("阿根廷"))

if st.button("开始模拟",type="primary",use_container_width=True):
    # 直接重置全局变量，不用global（变量定义在文件最顶部）
    player_stat = {}
    player_nation_map = {}
    bar=st.progress(0)
    tip=st.empty()
    group_res=[]
    for idx,(gn,teamlist) in enumerate(GROUP_DATA.items()):
        tip.text(f"正在模拟 {gn} 小组赛")
        top2,th,txt=sim_group(gn,teamlist,sel)
        group_res.append((top2,th,txt))
        st.code(txt)
        bar.progress((idx+1)/16)
    tip.text("筛选32强队伍")
    t32,txt32=get_32(group_res)
    st.code(txt32)
    st.code(f"晋级32强名单：{t32}")
    bar.progress(13/16)
    tip.text("进行淘汰赛模拟")
    champ,third,txt_k=sim_knockout(t32,sel)
    st.code(txt_k)
    bar.progress(15/16)
    tip.text("统计个人奖项")
    award=award_text()
    st.code(award)
    bar.progress(1.0)
    st.success("模拟全部结束！")
    st.subheader("📌所选球队战绩")
    if sel==champ:
        st.balloons()
        st.success(f"🎉{sel}夺得本届世界杯冠军！")
    elif sel==third:
        st.info(f"🥉{sel}拿到季军！")
    elif sel in t32:
        st.warning(f"📌{sel}闯入淘汰赛，无缘冠季军")
    else:
        st.error(f"❌{sel}小组赛出局，没能晋级32强")