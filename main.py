from flask import Flask,request,render_template,redirect,make_response,jsonify,session,abort,url_for,Response
import re,random,pymysql
import urllib.parse,urllib.request,json
import smtplib,os
from email.mime.text import MIMEText
from email.header import Header
import datetime
app=Flask(__name__)

app.secret_key = b'\xa3P\x05\x1a\xf8\xc6\xff\xa4!\xd2\xb5\n\x96\x05\xed\xc3\xc90=\x07\x8d>\x8e\xeb'
db = pymysql.connect("47.103.50.75","mx123","123456","mydb")

@app.route("/")
def home():
    return render_template("home.html")

def send_email_code(email):
    '''
    函数功能：发送邮箱验证码（6位随机数字）
    函数参数：
    email 接收验证码的邮箱
    返回值：发送成功返回验证码，失败返回False
    '''
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "xg@itmaxub.cn"  # 用户名
    mail_pass = "igfixexvdnxpdhia"  # 口令
    sender = 'xg@itmaxub.cn'
    receivers = ['%s'%email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    verify_code = str(random.randint(100000, 999999))
    message = MIMEText(verify_code, 'plain', 'utf-8')
    subject = "验证码"
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
      
        k=1
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
        k=0

    if k==1:
        return verify_code
    else:
        return False

def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数字）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "181173",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
            "key": "4573a1de4d447819432ad57487e27b80",  # 应用APPKEY(应用详细页查询)
        }
        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)
        print(res)
        print(verify_code)
        if res and res['error_code'] == 0:
        # if not res :
            return False
        else:
            return verify_code
    except:
        return False

# send_sms_code("17371290626")
@app.route("/reg", methods=["GET", "POST"])
def reg_handle():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        phone = request.form.get("phone")
        verify_code = request.form.get("verify_code")
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")
        email = request.form.get("email")
        print(upass,upass2)
        if not (uname and uname.strip() and upass and upass2 and phone):
            abort(500)
        if re.search(r"[\u4E00-\u9FFF]",uname):
            abort(Response("用户名含有汉字！"))
        if not re.fullmatch("[a-zA-Z0-9_]{4,20}",uname):
            abort(Response("用户名不合法"))
       
        if not (len(upass) >=6 or len(upass) <=15 and upass == upass2) :
            abort(Response("密码错误"))
      
        if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+", email):
            abort(Response("邮箱验证码错误！"))
        try:
            cur = db.cursor()
            cur.execute("insert into mb_user values (default,%s,md5(%s),%s,%s,sysdate(),sysdate(),'1','1')",(uname,uname+upass,phone,email,))
            res = cur.rowcount
            cur.close()
            db.commit()
        except:
            abort(Response("注册失败！"))
        
        return redirect(url_for("login_handle"))
@app.route("/user_center")

def user_center():
    user_info = session.get("user_info")
    
    print(user_info)
    print(session)

    if user_info:
        return render_template("user_center.html", uname=user_info.get("uname"))
    else:
        return redirect(url_for("login_handle"))


@app.route("/login", methods=["GET", "POST"])
def login_handle():
    if request.method=="GET":
        return render_template("login.html") 
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        
        if not (uname and uname.strip() and upass and upass.strip()):
            abort(Response("登录失败！"))
        if not re.fullmatch("[a-zA-Z0-9_]{4,20}",uname):
            abort(Response("用户名不合法"))
        if not (len(upass) >=6 or len(upass) <=15 ) :
            abort(Response("密码错误"))
           
        cur = db.cursor()
        cur.execute("select * from mb_user where uname=%s and upass=md5(%s) ",(uname,uname+upass))
        res = cur.fetchone()
        cur.close()
        if res: 
            cur_login_time=datetime.datetime.now()
            session["user_info"] = {

                "uid": res[0],
                "uname":res[1],
                "upass":res[2],
                "phone":res[3],
                "email":res[4],
                "reg_time":res[5],
                "last_login_time":res[6],
                "priv":res[7],
                "state":res[8],
                "login_time":cur_login_time
            }
        try:
            cur = db.cursor()
            cur.execute("update into mb_user set last_login_time=%s where uid =%s ",(cur_login_time,res[0]))
            res = cur.rowcount
            cur.close()
            db.commit()
        except Exception as e :
            print(e)
        print("登录成功！", session)
        return  redirect("/user_center")
    else:
            #登录失败
        return render_template("login.html",login_fail=1)



        
@app.route("/check_uname")
def check_uname():
    uname = request.args.get("uname")
    if not uname :
        abort(500)
  

    res = {"err":1,"desc":"用户名没有被注册！"}
    cur = db.cursor()
    cur.execute("select uid FROM mb_user where uname=%s",(uname,))
    if cur.rowcount == 0:
        #用户没有被注册
        res["err"]=0
        res["desc"]="用户名没有被注册！"
        cur.close()
        return jsonify(res)
    else:
        #用户名已经被注册
        print(res)
        return jsonify(res)

@app.route("/logout")
def logout_handle():
    res={"err":1,"desc":"未登录"}
    if session.get("user_info"):
       
        print(session.get("user_info")["uname"])
        session.pop("user_info")
       
        res["err"]=0
        res["desc"]="注销成功！"
        
    return jsonify(res)

@app.route("/root",methods=["GET","POST"])
def root():
    if request.method == "GET":
    
        return render_template("root.html")
    else:
        cur = db.cursor()
        content= request.form.get("content")
        mid= request.form.get("mid")
        cur.execute("update mb_message set content=%s where mid=%s ",(content,mid))
        cur.close()
        db.commit()
        # abort(Response("修改成功！"))
    return redirect("/message_board")

@app.route("/delete",methods=["GET","POST"])
def route():
    if request.method == "GET":
        return render_template("delete.html")
    else:
        uname= request.form.get("uname")
        cur = db.cursor()
        cur.execute("delete from mb_user where uname=%s",(uname,))
        cur.close()
        db.commit()
    return redirect("/")
@app.route("/select_user")
def select_user():
     
    cur = db.cursor()
    cur.execute("select * from mb_user")
    res=cur.fetchall()
    return render_template("se_user.html",users=res)



# 这是一个留言板的页面
@app.route("/message_board",methods=["POST","GET"])
def message_board_handle():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT uname,pub_time,content,cid from (select uid,pub_time,content,cid from mb_message limit 0,10) e,mb_user WHERE mb_user.uid=e.uid\
")
        res = cur.fetchall()
        cur.close()
        return render_template("message_board.html",messages=res,x=1)
    elif request.method == "POST":
        user_info = session.get("user_info")
        if not user_info :
            abort(Response("未登录！"))


        content = request.form.get("content")
        if content:
            content = content.strip()
            if 0 <len(content) <=200:
                uid = user_info.get("uid")
                pub_time = datetime.datetime.now()
                from_ip = request.remote_addr

                try:
                    cur = db.cursor()
                    cur.execute("insert into mb_message (uid,content,pub_time,from_ip) values (%s,%s,%s,%s) ",( uid ,content,pub_time,from_ip))
                    cur.close()
                    db.commit()
                    return "留言成功"
                except Exception as e :
                    print(e)
            abort(Response("留言失败！"))
@app.route("/page2")
def page2():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT uname,pub_time,content,cid from (select uid,pub_time,content,cid from mb_message limit 11,20) e,mb_user WHERE mb_user.uid=e.uid\
")
        res = cur.fetchall()
        cur.close()
        return render_template("message_board.html",messages=res,x=2)
@app.route("/page3")
def page3():
    if request.method == "GET":
        cur = db.cursor()
        cur.execute("SELECT uname,pub_time,content,cid from (select uid,pub_time,content,cid from mb_message limit 21,30) e,mb_user WHERE mb_user.uid=e.uid\
")
        res = cur.fetchall()
        cur.close()
        return render_template("message_board.html",messages=res,x=3)
        
# @app.route("/phone")
# def phone():
#     email = request.args.get("email")
    
#     result = {"err": 0, "desc":"内部错误"}
#     verify_code=send_email_code(email)
   
#     session[email]=verify_code
 
    # if verify_code :
    #     #发送短信验证码成功
    #     session[email]=verify_code
    #     result["err"] = 0
    #     result["desc"]= "发送邮箱验证成功！"
    # return jsonify(result)
   
if __name__ == "__main__":
    app.run(port=80,debug=True)
