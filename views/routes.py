from flask import Flask, abort , redirect , render_template , request , session , make_response
from models.Database import execute_query

def init_routes(app):
    @app.route('/' , methods = ['GET' , 'POST'])
    def home():
        # logic xử lý xử lý function stay_login  làm sau
        return render_template('login.html')
    @app.route('/login' , methods=['POST'])
    def login():
        msv = request.form.get('msv')
        passwd = request.form.get('password')

        query = f"select * from log_in where msv = '{msv}' and passwd ='{passwd}'"
        print(query)
        user = execute_query(query)

        if user:
            # session() trong FLASK lưu trên client (hiểu nó như là cookies trong PHP) - FLASK session
            session['user'] = user[0]['msv']
            session['role'] = user[0]['role']
            
            response = make_response(redirect('/admin' if user[0]['role']==1 else '/user'))

            # code function stay_login ở đây
            if request.form.get('stay_login') :
                msv = user[0]['msv']
                role = user[0]['role']
                response.set_cookie('auth' , f"{msv}--{role}" , max_age=60*60*24 , httponly=False)
            return response
        # login sai
        return redirect('/')
    
    @app.route('/logout')
    def logout():
        session.clear() # xóa toàn bộ FLASK session
        response = make_response(redirect('/'))
        response.set_cookie('auth' , '' , expires=0) 

        return response

    
    @app.route('/user')
    def user_page():
        if 'role' in session and session['role'] == 0:
            return render_template('user.html')
        return redirect('/')
    
    @app.route('/search', methods=['POST'])
    def search():
        msv = request.form.get('msv')
        query = f"select * from user where msv='{msv}'"

        try:
            results = execute_query(query )
            print('query : ' + query)
            return render_template('user.html', results=results , msv = msv )
        except Exception as e:
            abort(400)
        
    @app.route('/comment',methods=['POST'])
    def add_comment():
        cmt = request.form.get('comment')
        msv = session.get('user')

       

        query = f"INSERT INTO comment(msv , cmt) VALUES('{msv}' , '{cmt}')"

        row = execute_query(query)
        
        message = 'cant leave the comment'
        if row:
            message = 'sucsess'
        return render_template('user.html' , message = message)
    

    @app.route('/admin')
    def admin():
        role = session.get('role')
        query = f"SELECT * FROM user"
        users = execute_query(query)

        if role and  role == 1:
            return render_template('admin.html' , users = users)
        return redirect('/')
    
    @app.route('/admin/comments')
    def view_comment():
        role = session.get('role')
        if role and role != 1:
            return redirect('/')
        query = f"SELECT * FROM comment"

        comments = execute_query(query)

        return render_template('comments.html' , comments=comments)
    @app.route('/admin/add_user' , methods=['POST'])
    def add_user():
        role = session.get('role')
        if role and role != 1:
            return redirect('/')
        msv = request.form.get('msv')
        passwd = request.form.get('passwd')
        role_add = request.form.get('role')
        hoten = request.form.get('hoten')
        gpa = request.form.get('gpa')
    
        # bảng log_in    
        query_login = f"INSERT INTO log_in(msv , passwd , role) VALUES('{msv}' , '{passwd}' , '{role_add}')"
        query_user = f"INSERT INTO user(msv , hoten , gpa) VALUES('{msv}' , '{hoten}' , '{gpa}')"

        execute_query(query_login)
        execute_query(query_user)

        return redirect('/admin')
    
    @app.route('/admin/delete_user' , methods = ['POST'])
    def delete_user():
        role = session.get('role')
        if role and role != 1:
            return redirect('/')
        msv = request.form.get('msv')
        query = f"DELETE FROM log_in WHERE msv = '{msv}'"

        execute_query(query)

        return redirect('/admin')