#written by funcbone.
Version = 'v.1.0'

from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.pyplot as plt
import os

#默认数据
xe = [0,0.019,0.0721,0.0966,0.1238,0.1661,0.2337,0.2608,0.3273,0.3965,0.5079,0.5198,0.5732,0.6763,0.7472,0.8943,1]
ye = [0,0.170,0.3891,0.4375,0.4704,0.5089,0.5445,0.5580,0.5826,0.6122,0.6564,0.6599,0.6841,0.7385,0.7815,0.8943,1]
Q = []
H = []
N = []
η = []
'''
Q = [5.934163701,5.655516014,5.407829181,4.922775801,4.406761566,4.045551601,3.787544484,3.550177936,3.281850534,3.013523132,2.786476868,2.538790036,1.217793594,0.85658363,0]
H = [8.8495246,9.744564973,10.61777509,12.08040204,13.48845336,14.492645,15.00565594,15.57324252,16.10808372,16.66475517,17.11227536,17.55979554,20.48504945,21.09629653,22.46068734]
N = [780.0442522,779.0000163,781.0884882,777.9557803,776.9115444,768.5576568,761.2480052,753.9383535,746.6287019,735.1421065,725.743983,717.3900954,658.9128824,642.2051072,591.0375459]
η = [18.25,19.18,19.93,20.72,20.74,20.68,20.24,19.88,19.19,18.52,17.81,16.84,10.26,7.63,0.00]
'''
def fullCic(xe = xe,ye = ye,Xw = 0.0117,Xd = 0.8315,infoR01 = 1,sca01 = 1,limit = 0.1):
    #字体和分辨率设置
    plt.rc("font",family = "KaiTi")
    plt.rcParams['figure.dpi'] = 200

    #图像框架设置
    fig = plt.figure(figsize=(5.5, 3.5))
    fig.canvas.manager.set_window_title('精馏塔全回流理论板绘制')
    host = host_subplot(111, axes_class=axisartist.Axes)
    ax = plt.subplot(1,1,1)
    aspectratio=1.0
    ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    ax.set_aspect(ratio_default*aspectratio)
    host.axis["top"].set_visible(False)
    host.axis["right"].set_visible(False)
    par1 = host.twinx()
    par2 = host.twiny()
    par1.set_yticks([])
    par2.set_xticks([])
    plt.xticks([])
    plt.yticks([])
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.xlabel('x')
    plt.ylabel('y')

    #相平衡曲线及对角线绘制
    plt.plot(xe,ye,'k',linewidth=0.4)
    plt.plot([0,1],[0,1],'k',linewidth=0.5)
    plt.plot([Xw,Xw],[0,Xw],'k--',linewidth=0.4)
    plt.plot([Xd,Xd],[0,Xd],'k--',linewidth=0.4)
    plt.xticks([Xw,Xd,1], ["Xw", "Xd",'1.0'])
    plt.yticks([1], ['1.0'])

    #理论板绘制
    y1 = x1 = Xd
    steps = 0
    while 1 :
        for num in ye :
            if num > y1 :
                pointA = ye.index(num)
                pointB = pointA - 1
                break
        x = xe[pointA]-(ye[pointA]-y1)*(xe[pointA]-xe[pointB])/(ye[pointA]-ye[pointB])
        plt.plot([x,x1],[y1,y1],'k',linewidth=0.4)
        plt.plot([x,x],[y1,x],'k',linewidth=0.4)
        steps += 1
        if steps > 100:
            input('\n！！！理论板数已大于100，请检查是否形成无穷大理论板数！！！\n\n(按回车继续)\n')
            plt.close()
            return 0
        y1 = x1 = x
        if x <= Xw :
            break

    #右侧附带数据说明
    if infoR01 == 1:
        plt.text(1.03,0.97,'全回流实验数据：')
        plt.text(1.03,0.97-0.05,' 理论板数：{}'.format(steps))
        plt.text(1.03,0.92-0.05,' Xw： {}'.format(Xw))
        plt.text(1.03,0.87-0.05,' Xd： {}'.format(Xd))

    #附图
    if sca01 == 1:
        axins = ax.inset_axes((1.15, 0.05, 0.2, 0.2))
        axins.plot(xe,ye,'k',linewidth=0.4)
        axins.plot([0,1],[0,1],'k',linewidth=0.5)
        axins.plot([Xw,Xw],[0,Xw],'k--',linewidth=0.4)
        axins.plot([Xd,Xd],[0,Xd],'k--',linewidth=0.4)

        y1 = x1 = Xd
        steps = 0
        while 1 :
            for num in ye :
                if num > y1 :
                    pointA = ye.index(num)
                    pointB = pointA - 1
                    break
            x = xe[pointA]-(ye[pointA]-y1)*(xe[pointA]-xe[pointB])/(ye[pointA]-ye[pointB])
            axins.plot([x,x1],[y1,y1],'k',linewidth=0.4)
            axins.plot([x,x],[y1,x],'k',linewidth=0.4)
            steps += 1

            y1 = x1 = x
            if x <= Xw :
                break

        axins.set_xlim(0,limit)
        axins.set_ylim(0,limit)
        axins.set_yticks([limit])
        axins.set_yticklabels([limit])
        axins.set_xticks([Xw,limit])
        axins.set_xticklabels(['Xw',limit])

        mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec='darkgray', lw=0.5)
    plt.tight_layout()
    plt.show()
def nonfullCic(xe = xe,ye = ye,infoR01 = 1,sca01 = 1,Xw = 0.0071,Xd = 0.6514,Xf = 0.0556,d1 = 0.3257,k1 = 0.5,kq = 9.8510,dq = -0.4924,R = 1,limit = 0.05):
# 标 1 为精馏段数据 ， 标 2 为提馏段数据
    #实验数据
    Xq = (dq-d1)/(k1-kq)
    Yq = k1*Xq+d1   #Xq,Yq为d点坐标
    k2 = (Yq-Xw)/(Xq-Xw)
    d2 = Xw*(1-k2)

    #判断d点是否合理
    '''
    for dy in xe :
        if Xq <= dy :
            numdy = xe.index(dy)
            break
    pay = ye[numdy]
    pax = xe[numdy]
    pby = ye[numdy]
    pbx = xe[numdy]
    yqc = (pay-pby)*(Xq-pax)/(pax-pby)+pax
    if Yq >= yqc :
        print('\n ！！！理论板数无穷大，无法绘制！！！\n')
        print(Yq,yqc)
        plt.close()
        input('')
        return 0
    '''

    #字体和分辨率设置
    plt.rc("font",family = "KaiTi")
    plt.rcParams['figure.dpi'] = 200

    #图像框架设置
    fig = plt.figure(figsize=(5.5, 3.5))
    fig.canvas.manager.set_window_title('精馏塔部分回流理论板绘制')
    host = host_subplot(111, axes_class=axisartist.Axes)
    ax = plt.subplot(1,1,1)
    aspectratio=1.0
    ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    ax.set_aspect(ratio_default*aspectratio)
    host.axis["top"].set_visible(False)
    host.axis["right"].set_visible(False)
    par1 = host.twinx()
    par2 = host.twiny()
    par1.set_yticks([])
    par2.set_xticks([])
    plt.xticks([])
    plt.yticks([])
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.xlabel('x')
    plt.ylabel('y')

    #相平衡曲线及对角线绘制


    plt.plot(xe,ye,'k',linewidth=0.4)
    plt.plot([0,1],[0,1],'k',linewidth=0.5)

    plt.plot([Xw,Xw],[0,Xw],'k--',linewidth=0.4)
    plt.plot([Xd,Xd],[0,Xd],'k--',linewidth=0.4)
    plt.plot([Xf,Xf],[0,Xf],'k--',linewidth=0.4)
    plt.plot([Xf,Xq],[Xf,Yq],'k--',linewidth=0.4)
    plt.plot([0,Xq],[d1,Yq],'k--',linewidth=0.4)
    plt.plot([Xf,Xq],[Xf,Yq],'k--',linewidth=0.4)

    plt.plot([Xq,Xd],[Yq,Xd],'k',linewidth=0.4)
    plt.plot([Xw,Xq],[Xw,Yq],'k',linewidth=0.4)

    plt.xticks([Xw,Xf,Xd,1], ["Xw","Xf","Xd",'1.0'])
    plt.yticks([d1,1], ['Xd/(R+1)','1.0'])

    #理论板绘制
    y1 = x1 = Xd
    steps = 0
    while 1 :
        for num in ye :
            if num > y1 :
                pointA = ye.index(num)
                pointB = pointA - 1
                break
        x = xe[pointA]-(ye[pointA]-y1)*(xe[pointA]-xe[pointB])/(ye[pointA]-ye[pointB])
        plt.plot([x,x1],[y1,y1],'k',linewidth=0.4)
        if x >=  Xq:
            y = k1*x+d1
        else:
            y = k2*x+d2
        if x >= Xw :
            plt.plot([x,x],[y1,y],'k',linewidth=0.4)
        else:
            plt.plot([x,x],[y1,x],'k',linewidth=0.4)
        steps += 1
        if steps > 100 :
            print('\n ！！！理论板数以大于100，请检查是否形成无穷大理论板数！！！')
            input(' (按回车继续)')
            plt.close()
            return('none')

        x1 = x
        y1 = y

        if x <= Xw :
            break

    #右侧附带数据说明
    if infoR01 == 1 :
        plt.text(1.03,0.97,'部分回流实验数据：')
        plt.text(1.03,0.92,' 理论板数：{}'.format(steps))
        plt.text(1.03,0.87,' Xw： {}'.format(Xw))
        plt.text(1.03,0.82,' Xd： {}'.format(Xd))
        plt.text(1.03,0.77,' Xf： {}'.format(Xf))
        plt.text(1.03,0.72,' Xd/(R+1)：')
        plt.text(1.03,0.67,'      {:.4f}'.format(Xd/(R+1)))
        plt.text(1.03,0.62,' d点坐标：')
        plt.text(1.03,0.57,'  ({:.4f},{:.4f})'.format(Xq,Yq))
        ax.annotate('d', xy=(Xq+0.0,Yq-0.0), xytext=(Xq+0.045,Yq-0.045),
                    arrowprops=dict(facecolor='black',headwidth=2,width=0.1,headlength=4),
                    )

    #附图
    if sca01 == 1 :
        axins = ax.inset_axes((1.15, 0.05, 0.2, 0.2))
        axins.plot(xe,ye,'k',linewidth=0.4)
        axins.plot([0,1],[0,1],'k',linewidth=0.5)

        axins.plot([Xw,Xw],[0,Xw],'k--',linewidth=0.4)
        axins.plot([Xd,Xd],[0,Xd],'k--',linewidth=0.4)
        axins.plot([Xf,Xf],[0,Xf],'k--',linewidth=0.4)
        axins.plot([Xf,Xq],[Xf,Yq],'k--',linewidth=0.4)
        axins.plot([0,Xq],[d1,Yq],'k--',linewidth=0.4)
        axins.plot([Xf,Xq],[Xf,Yq],'k--',linewidth=0.4)

        axins.plot([Xq,Xd],[Yq,Xd],'k',linewidth=0.4)
        axins.plot([Xw,Xq],[Xw,Yq],'k',linewidth=0.4)


        y1 = x1 = Xd
        steps = 0
        while 1 :
            for num in ye :
                if num > y1 :
                    pointA = ye.index(num)
                    pointB = pointA - 1
                    break
            x = xe[pointA]-(ye[pointA]-y1)*(xe[pointA]-xe[pointB])/(ye[pointA]-ye[pointB])
            axins.plot([x,x1],[y1,y1],'k',linewidth=0.4)
            if x >=  Xq:
                y = k1*x+d1
            else:
                y = k2*x+d2
            if x >= Xw :
                axins.plot([x,x],[y1,y],'k',linewidth=0.4)
            else:
                axins.plot([x,x],[y1,x],'k',linewidth=0.4)
            steps += 1


            x1 = x
            y1 = y

            if x <= Xw :
                break
        axins.set_xlim(0,limit)
        axins.set_ylim(0,limit)
        axins.set_yticks([limit])
        axins.set_yticklabels([limit])
        axins.set_xticks([Xw,limit])
        axins.set_xticklabels(['Xw',limit])

        mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec='darkgray', lw=0.5)
    plt.tight_layout()
    plt.show()
def pump(Q = Q,H = H,N = N,η = η):
    plt.rc("font",family = "KaiTi")
    plt.rcParams['figure.dpi'] = 200


    fig = plt.figure(figsize=(5.5, 3.5))
    fig.canvas.manager.set_window_title('离心泵特性曲线绘制')


    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(right=5)

    ax = plt.subplot(1,1,1)
    aspectratio=0.38
    ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    ax.set_aspect(ratio_default*aspectratio)

    #设置寄生轴
    par1 = host.twinx()
    par2 = host.twinx()

    #设置第三Y轴位置
    par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))

    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)

    #曲线绘制
    p1, = host.plot(Q,H, label=" H'-Q")
    p2, = par1.plot(Q,N, label=" N'-Q")
    p3, = par2.plot(Q,η, label="η'-Q")

    host.set_xlabel("流量 Q (m^3/h)")
    host.set_ylabel("扬程 H' (m)")
    par1.set_ylabel("轴功率 N' (w)")
    par2.set_ylabel("效率 η'")

    host.legend(loc="center right")

    #标签设置
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    #坐标轴样式设置
    host.axis["top"].set_visible(False)
    host.axis["left"].set_axisline_style("->",size = 1)
    par1.axis["right"].set_axisline_style("->",size = 1)
    par2.axis["right"].set_axisline_style("->",size = 1)
    # ↑ 框架绘制
    plt.tight_layout()
    plt.show()

def easyDrawInfo():
    print('='*70,)
    print(' easyDraw {}  funcbone.com\n'.format(Version))
    print(' 欢迎使用，本程序目前用于绘制三种图像：\n\n 1、精馏塔全回流理论板绘制\n 2、精馏塔部分回流理论板绘制\n 3、离心泵特性曲线绘制\n')
    print(' 输入对应的序号进行图像绘制\n\n 输入0或exit退出\n about  --关于本软件')
    print('='*70)
def fullCicInfo():
    print('-'*70)
    print(' 精馏塔全回流理论板绘制\n')
    print(' 本程序默认使用 乙醇-水 相平衡曲线绘制\n')
    print(' 请输入相关数据：\n Xw --塔釜物质的量分数\n Xd --回流液物质的量分数')
    print(' 格式如下：\n\n θ Xw,Xd\n\n 请用逗号间隔两个数据\n 如：\n θ 0.1,0.8')
    print('\n 指令：\n show   --绘制图像\n set    --设置图像右侧的信息标注和附图\n back   --返回上一层级')
    print('\n ！！重复填写的数据将被覆盖！！')
    print('-'*70)
def nonfullCicInfo():
    print('-'*70)
    print(' 精馏塔部分回流理论板绘制\n')
    print(' 本程序默认使用 乙醇-水 相平衡曲线绘制\n')
    print(' 指令：\n')
    print(' data  --填写数据\n edit  --编辑已输入的数据\n show  --绘制图像\n set   --设置图像右侧的信息标注和附图\n back  --返回上一层级')
    print('\n ！！重复填写的数据将被覆盖！！')
    print('-'*70)
def pumpInfo():
    print('-'*70)
    print(' 离心泵特性曲线绘制\n')
    print(' 指令：\n')
    print(' data  --填写数据\n edit  --编辑已输入的数据\n show  --绘制图像\n list  --显示已输入数据\n clear --清除已输入数据\n back  --返回上一层级')
    print('-'*70)
def nonfullCicEditInfo():
    print('-'*70)
    print('\n 请输入需要修改的数据名称(如：Xw)\n 输入done退出修改模式\n')

def idtf(x):

    if x == '':
        return('none')
    x=str(x)
    x=x.replace('，',',')
    n=x.find(',')

    noL="?!;:'\"*\\()%#@~/+。？！～、：＃；％＊—…＆·￥（）‘’“”[]｛｝[]"
    for let in noL:
        if let in x:
            return('none')

    if x.isdigit():
        return eval(x)
    if x[0]=='-' and x[1:].isdigit():
        return eval(x)

    if n==(len(x)-1) :
        return('none')

    if x.isalpha():
        if x=='exit' or x=='back' or x=='list' or x=='edit' or x=='show' or x=='set':return(x)
        else:return('none')


    numP = x.count('.')
    if numP == 1:
        indexP = x.index('.')
        if (x[:indexP]+x[indexP+1:]).isdigit() and x[-1]!='.':
            return eval(x)

    numN = x.count('-')
    if numN == 1 :
        indexN = x.index('-')
        if numP == 1 and indexN == 0 and x[-1]!='.' and (x[indexN+1:indexP]+x[indexP+1:]).isdigit():
            return eval(x)


    if n<1 or x.count(',')!=1:
        return('none')
    else:
        if x[:n].count('.')>1 or x[n:].count('.')>1:return('none')

        if x[0]=='.':
            x='0'+x
        if x[n+1]=='.':
            x=x[:n+1]+'0'+x[n+1:]

        for num in x:
            if num.isalpha():return('none')
        key=0
        if n!=1:
            for num in x[:n]:
                if num=='0':
                    key+=1
                elif num=='.':
                    key-=1;break
                else:
                    break
            x=x[key:]
        key=n+1
        for num in x[n+1:]:
            if num=='0':
                key+=1
            elif num=='.':
                key-=1;break
            else:
                break
        x=x[:n+1]+x[key:]
        if x.index(',') == 0 or x.index(',') == -1:
            return('none')
        else:
            return(eval(x))
#对用户输入内容进行处理
#返回命令字符串，返回正负整数，返回正负小数， 返回元组，其他返回'none'
def isfloat(x):
    if x == '-':return(('-',0))
    if x == '':return(('',0))
    numN = x.count('-')
    numP = x.count('.')
    if x.isdigit() :
        return((float(eval(x)),1))
    if x[0] == '-' and numN == 1 and numP == 0 and x[1:].isdigit():
        return((float((eval(x))),1))
    else:
        if numN == numP == 1:
            if x[0] == '-':
                if x.index('.') == (len(x)-1) :
                    if x[1:-1].isdigit():
                        return((float(eval(x)),1))
                else:
                    if (x[1:x.index('.')]+x[x.index('.')+1:]).isdigit():
                        return((float(eval(x)),1))
                if x[1]=='.' and x[2:].isdigit():
                    return((float(eval('-0.'+x[2:])),1))
                else:
                    return(('none',0))
            else:
                return(('none',0))
        else:
            if numN == 0 and numP == 1 :
                return((float(eval(x)),1))
            if numN == 1 and numP == 0 :
                if x[1:].isdigit():
                    return((float(eval(x)),1))
                else:
                    return(('none',0))
            else:
                return(('none',0))
#字符串输入，输出正负小数，其他情况返回'none',返回元组(num,bool),num为数字bool为1，num为none bool为0
def aboutInfo():
    os.system('cls')
    print('#'*70)
    print(' easyDraw {} funcbone.com'.format(Version))
    print('\n 本软件为方便化工原理实验作图，由funcbone编制作\n 使用python及第三方库matplotlib绘制曲线\n\n 如使用过程中遇到恶性漏洞，请截图反馈帮助完善软件！\n\n 联系方式：\n QQ:352121146\n 邮箱：funcbone@163.com\n 网站：funcbone.com')
    print('\n 源码：\n https://github.com/funcbone/easyDraw')
    print('\033[4;30;36m\nWe are all in the gutter, but some of us are looking at the stars.\033[0m')
    print('#'*70)

str1 = '显示'
str0 = '不显示'
while 1 :
    os.system('cls')
    easyDrawInfo()
    order = input('\nθ ')
    Xw = Xd = Xf = k1 = d1 = kq = dq = R = 'none'
    Q = []
    H = []
    N = []
    η = []
    infoR01 = sca01 = 1
    if order == 'about':
        aboutInfo()
        input('\n (按回车继续)')
    if order == 'exit' or order == '0':
        order = input('\n ！退出后已输入的数据将被清除，是否确定要退出(Y/N)！')
        if order == 'y' or order == '1':
            exit()
        else:
            continue

    if order == '1' :
        limit = 0.1
        while 1 :
            os.system('cls')
            fullCicInfo()
            if infoR01 == 1 :
                s1 = str1
            else:
                s1 = str0
            if sca01 == 1 :
                s2 = str1
            else:
                s2 = str0
            if Xw == 'none' or Xd == 'none' :
                print('\n (！还未完成数据输入！)')
            else:
                print('\n Xw = {:<7}   右侧信息是否显示：  {}   \n Xd = {:<7}   附图是否显示：\t    {}\n\t\t附图XY限值：\t    {:<7}'.format(Xw,s1,Xd,s2,limit))
            order = idtf(input('\nθ '))
            if order == 'exit' or order == 0:
                order = input('\n ！退出后已输入的数据将被清除，是否确定要退出(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    exit()
                else:
                    continue
            if order == 'set' :
                order = input('\n 是否显示右侧信息标注(Y/N): ')
                if order == 'Y' or order == 'y' or order == '1':
                    infoR01 = 1
                if order == 'N' or order == 'n' or order == '0':
                    infoR01 = 0
                order = input('\n 是否显示右侧附图(Y/N): ')
                if order == 'Y' or order == 'y' or order == '1':
                    sca01 = 1
                if order == 'N' or order == 'n' or order == '0':
                    sca01 = 0
                order = isfloat(input('\n 附图XY限值：'))
                if order[1] == 1 :
                    limit = order[0]
                continue
            if order == 'show' :
                if Xw == 'none' or Xd == 'none':
                    input(' (！还未完成数据输入！)\n(按回车继续输入)')
                else:
                    fullCic(Xw = Xw,Xd = Xd,infoR01 = infoR01,sca01 = sca01,limit = limit)
                    plt.close()
                    continue
            if order == 'back':
                order = input('\n ！返回上一层级数据将被清除，是否确定要返回(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    break
                else:
                    continue
            if str(type(order))=="<class 'tuple'>":
                if 0<order[0]<1 and 0<order[1]<1:
                    Xw = order[0]
                    Xd = order[1]
                else:
                    input('\n ！！！输入数据不合理！！！\n (按回车继续)')
                    continue

    if order == '2' :
        limit = 0.05
        while 1:
            os.system('cls')
            nonfullCicInfo()
            if infoR01 == 1 :
                s1 = str1
            else:
                s1 = str0
            if sca01 == 1 :
                s2 = str1
            else:
                s2 = str0
            if Xw == 'none' and Xd == 'none' and Xf == 'none' and k1 == 'none' and d1 == 'none' and kq =='none' and dq == 'none' :
                print('\n (！还未完成数据输入！)')
            else:
                print('\n Xw = {:<7} \tXd = {:<7} \tXf = {:<7} \t右侧信息是否显示：{:<7} \n k1 = {:<7} \td1 = {:<7} \tR  = {:<7} \t附图是否显示：\t  {:<7}\n kq = {:<7} \tdq = {:<7} \t\t\t附图XY限值：\t  {}\n'.format(Xw,Xd,Xf,s1,k1,d1,R,s2,kq,dq,limit))
            order = input('\nθ ')
            if order == 'exit' or order == '0':
                order = input('\n ！退出后已输入的数据将被清除，是否确定要退出(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    exit()
                else:
                    continue
            if order == 'back':
                order = input('\n ！返回上一层级数据将被清除，是否确定要返回(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    break
                else:
                    continue
            if order == 'data':
                Xw = idtf(input(' 塔釜物质的量分数   Xw = '))
                Xd = idtf(input(' 回流液物质的量分数 Xd = '))
                Xf = idtf(input(' 进料液物质的量分数 Xf = '))
                k1 = idtf(input(' 精馏段斜率         k1 = '))
                d1 = idtf(input(' 精馏段截距         d1 = '))
                kq = idtf(input(' q线斜率            kq = '))
                dq = idtf(input(' q线截距            dq = '))
                R = idtf(input(' 回流比             R = '))
                continue
            if order == 'set' :
                order = input('\n 是否显示右侧信息标注(Y/N): ')
                if order == 'Y' or order == 'y' or order == '1':
                    infoR01 = 1
                if order == 'N' or order == 'n' or order == '0':
                    infoR01 = 0
                order = input('\n 是否显示右侧附图(Y/N): ')
                if order == 'Y' or order == 'y' or order == '1':
                    sca01 = 1
                if order == 'N' or order == 'n' or order == '0':
                    sca01 = 0
                order = isfloat(input('\n 附图XY限值：'))
                if order[1] == 1 :
                    limit = order[0]
                continue
            if order == 'show':
                if Xw == 'none' or Xd == 'none' or Xf == 'none' or k1 == 'none' or d1 == 'none' or kq =='none' or dq == 'none':
                    input(' (！还未完成数据输入！)\n(按回车继续输入)')
                else:
                    if 0<Xw<1 and 0<Xd<1 and 0<Xf<1:
                        nonfullCic(Xw = Xw,Xd = Xd,infoR01 = infoR01,sca01 = sca01,Xf = Xf,k1 = k1,d1 = d1,kq = kq,dq = dq,R = R,limit = limit)
                        plt.close()
                        continue
                    else:
                        print('\n ！！输入数据不合理！！\n')
                        input(' (按回车继续)')
                        continue
            if order == 'edit':
                if Xw == 'none' and Xd == 'none' and Xf == 'none' and k1 == 'none' and d1 == 'none' and kq =='none' and dq == 'none':
                    input(' 还未输入数据\n(按回车继续输入)')
                    continue
                else:
                    while 1:
                        os.system('cls')
                        print('\n','-'*70,sep='')
                        print('\n Xw = {:<6} \tXd = {:<6} \tXf = {:<6}  \n k1 = {:<6} \td1 = {:<6} \tR  = {:<6} \n kq = {:<6} \tdq = {:<6}\n'.format(Xw,Xd,Xf,k1,d1,R,kq,dq))
                        nonfullCicEditInfo()
                        order = input(' θ ')
                        if order == 'done':
                            break
                        if order == 'Xw' or order == 'xw':Xw = idtf(input('\n Xw = '))
                        if order == 'Xd' or order == 'xd':Xd = idtf(input('\n Xd = '))
                        if order == 'Xf' or order == 'xf':Xf = idtf(input('\n Xf = '))
                        if order == 'k1':k1 = idtf(input('\n k1 = '))
                        if order == 'd1':d1 = idtf(input('\n d1 = '))
                        if order == 'kq':kq = idtf(input('\n kq = '))
                        if order == 'dq':dq = idtf(input('\n dq = '))
                        if order == 'R' or order == 'r':R = idtf(input('\n R = '))

    if order == '3' :
        while 1:
            os.system('cls')
            pumpInfo()
            if Q == H == N == η == [] or Q == 'none' or H == 'none' or N == 'none' or η ==  'none':
                print('\n (！还未完成数据输入！)')
            else:
                print('\n (已完成数据输入 list --查看)')
            order = input('\nθ ')
            if order == 'exit' or order == '0':
                order = input('\n ！退出后已输入的数据将被清除，是否确定要退出(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    exit()
                else:
                    continue
            if order == 'back':
                order = input('\n ！返回上一层级数据将被清除，是否确定要返回(Y/N)！')
                if order == 'y' or order  == 'Y' or order == '1':
                    break
                else:
                    continue
            if order == 'data':
                while 1:
                    os.system('cls')
                    print('\n Q\' = {}'.format(Q))
                    order = isfloat(input("\n 流量 Q (m^3/h) = "))
                    if order[1]==0:
                        if order[0] == '-' and len(Q)>0 :
                            Q.pop(-1)
                        if order[0] == '' :
                            del order
                            break
                    if order[1]==1:
                        Q.append(order[0])
                while 1:
                    os.system('cls')
                    print('\n H\' = {}'.format(H))
                    order = isfloat(input("\n 扬程 H' (m) = "))
                    if order[1]==0:
                        if order[0] == '-' and len(H)>0 :
                            H.pop(-1)
                        if order[0] == '' :
                            del order
                            break
                    if order[1]==1:
                        H.append(order[0])
                while 1:
                    os.system('cls')
                    print('\n N\' = {}'.format(N))
                    order = isfloat(input("\n 轴功率 N' (w) = "))
                    if order[1]==0:
                        if order[0] == '-' and len(N)>0 :
                            N.pop(-1)
                        if order[0] == '' :
                            del order
                            break
                    if order[1]==1:
                        N.append(order[0])
                while 1:
                    os.system('cls')
                    print('\n η\' = {}'.format(η))
                    order = isfloat(input("\n 效率 η' = "))
                    if order[1]==0:
                        if order[0] == '-' and len(η)>0 :
                            η.pop(-1)
                        if order[0] == '' :
                            del order
                            break
                    if order[1]==1:
                        η.append(order[0])
                continue
            if order == 'list' :
                if Q == H == N == η == [] or Q == 'none' or H == 'none' or N == 'none' or η ==  'none':
                    print('\n (！还未完成数据输入！)')
                    input(' (按回车继续)')
                    continue
                else:
                    print('\n Q = {}\n 数据个数：{}\n\n H = {}\n 数据个数：{}\n\n N = {}\n 数据个数：{}\n\nη = {}\n 数据个数：{}\n'.format(Q,len(Q),H,len(H),N,len(N),η,len(η)))
                    input(' (按回车继续)')
                    continue
            if order == 'show' :
                if Q == H == N == η == [] or Q == 'none' or H == 'none' or N == 'none' or η ==  'none':
                    print('\n (！还未完成数据输入！)')
                    input(' (按回车继续)')
                    continue
                else:
                    if len(Q) == len(H) == len(N) == len(η) :
                        pump(Q = Q,H = H,N = N,η = η)
                        plt.close()
                        continue
                    else:
                        print('\n ！！！请检查，各项数据个数不同！！！')
                        input(' (按回车继续)')
                        continue
            if order == 'clear':
                if Q == H == N == η == [] or Q == 'none' or H == 'none' or N == 'none' or η ==  'none':
                    print('\n (！还未完成数据输入！)')
                    input(' (按回车继续)')
                    continue
                else:
                    while 1 :
                        print('\n Q\' = {}\n 数据个数：{}\n\n H\' = {}\n 数据个数：{}\n\n N\' = {}\n 数据个数：{}\n\nη\'(Eta) = {}\n 数据个数：{}\n'.format(Q,len(Q),H,len(H),N,len(N),η,len(η)))
                        print('\n 请输入需要清除数据的变量名即可清除变量的所以数据\n done  --完成清除\n\n θ ',end='')
                        order = input()
                        if order == 'Q' or order == 'q':
                            Q = []
                        if order == 'H' or order == 'h':
                            H = []
                        if order == 'N' or order == 'n':
                            N = []
                        if order == 'η' or order =='Eta' or order == 'eta':
                            η = []
                        if order == 'done':
                            order = ''
                            break
