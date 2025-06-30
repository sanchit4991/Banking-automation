from tkinter import Tk,ttk,Label,Frame,Entry,Button,BooleanVar,Checkbutton,messagebox,filedialog,Menu
from tkinter import Scrollbar,HORIZONTAL,VERTICAL,BOTTOM,LEFT,RIGHT,BOTH,END,X,Y
from tkinter.ttk import Combobox,Treeview,Style
import time
from PIL import Image,ImageTk
import random
import myproject_db_sqlite
import myproject_mail
import sqlite3
from threading import Thread
import re
import os
import shutil

def generate_captcha():
    captcha=[]
    for i in range(3):
        captcha.append(chr(random.randint(65,90)))
        captcha.append(str(random.randint(0,9)))
    random.shuffle(captcha)
    captcha=''.join(captcha)
    return captcha

def refresh():
    captcha=generate_captcha()
    captcha_lbl.config(text=captcha)

def myclock():
    updated_time=time.strftime('%r')
    myclock_lbl.configure(text=updated_time)
    root.after(1000,myclock)

root_color='#f8fafc'
child_window_color='#dbeafe'
root_text_fg='#1e3a8a'
today=time.strftime('%A, %d %B %Y')

root=Tk()
root.attributes('-fullscreen',True)
root.resizable(width=False,height=False)
root.configure(bg=root_color)
root.title('ABC Bank')

title_lbl=Label(root,text='Banking Automation',font=('Helvetica',50,'bold'),bg=root_color,fg=root_text_fg)
title_lbl.pack(pady=5)
today_lbl=Label(root,text=today,font=('Helvetica',20),bg=root_color,fg=root_text_fg)
today_lbl.pack(pady=5)
myclock_lbl=Label(root,text=time.strftime('%r'),font=('Helvetica',20),bg=root_color,fg=root_text_fg)
myclock_lbl.pack(pady=5)
myclock()

# img1_path='my_project_imgs_/pngtree-bank-icon-png-image_6057224.jpg'
# img2_path='my_project_imgs_/images.png'
# img3_path='my_project_imgs_/images-2.png'
# l_img_path=[img1_path,img2_path,img3_path]
# l_imgs=[ImageTk.PhotoImage(Image.open(path).resize((300,150))) for path in l_img_path]

# logo_lbl=Label(root)
# logo_lbl.place(relx=0,rely=0)

# index=0
# def switch_imgs():
#     global index
#     logo_lbl.config(image=l_imgs[index])
#     index=(index+1)%len(l_imgs)
#     root.after(2000,switch_imgs)

# switch_imgs()

logo1_img=Image.open('my_project_imgs/logo.png').resize((300,154))
logo1_img_bitmap=ImageTk.PhotoImage(logo1_img,master=root)

logo1_lbl=Label(root,image=logo1_img_bitmap)
logo1_lbl.place(relx=0,rely=0)

footer_lbl=Label(root,text='Developed by: Sanchit Bhakuni',font=('Helvetica',20),bg=root_color,fg=root_text_fg)
footer_lbl.pack(side='bottom',pady=5)

def main_screen():
    def forgot_pass():
        if captcha_lbl.cget('text')!=inputcap_entry.get():
            messagebox.showerror('invalid captcha','Invalid captcha!')
            refresh()
            return
        frm.destroy()
        forgot_pass_screen_user()

    def toggle_password():
        if show_var.get():
            pass_entry.config(show='')
        else:
            pass_entry.config(show='*')

    def login():
        login_type=login_type_combo.get()
        acno=acno_entry.get()
        password=pass_entry.get()
        input_cap=inputcap_entry.get()
        captcha_lbl_var=captcha_lbl.cget('text')

        if input_cap!=captcha_lbl_var:
            refresh()
            messagebox.showerror('invalid captcha','Invalid captcha!')
            return

        if login_type=='Admin':
            if input_cap==captcha_lbl_var and pass_entry.get()=='admin':
                frm.destroy()
                admin_screen()
            elif pass_entry.get()!='admin':
                messagebox.showerror('invalid','Incorrect password!')
                return
        elif login_type=='User':
            # global user_uscreen
            user=myproject_db_sqlite.udetails(acno,password)
            if user==None:
                messagebox.showerror('invalid','Invalid username/password!')
                captcha_lbl.config(text=generate_captcha())
                return
            frm.destroy()
            user_screen_fun(user)
        else:
            messagebox.showinfo('Please Login','Select Login Type')
            captcha_lbl.config(text=generate_captcha())

    def reset():
        frm.destroy()
        main_screen()

    frm=Frame(root)
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.75)
    frm.configure(bg=child_window_color)

    login_type_lbl=Label(frm,text='Login Type',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    login_type_lbl.place(relx=.35,rely=.1)

    login_type_combo=Combobox(frm,values=['Admin','User'],font=('Helvetica',20),width=17,state='readonly',justify='center')
    login_type_combo.set('Select')
    login_type_combo.place(relx=.45,rely=.1)

    acno_lbl=Label(frm,text='Account No.',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    acno_lbl.place(relx=.35,rely=.2)
    acno_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
    acno_entry.place(relx=.45,rely=.2)
    acno_entry.focus()

    pass_lbl=Label(frm,text='Password',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    pass_lbl.place(relx=.35,rely=.3)
    pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,show='*',highlightbackground=root_color)
    pass_entry.place(relx=.45,rely=.3)

    show_var=BooleanVar()
    show_check=Checkbutton(frm,text='Show Password',variable=show_var,command=toggle_password,fg=root_text_fg,bg=root_color,font=('Helvetica',15,'bold'))
    show_check.place(relx=.65,rely=.31)

    global captcha_lbl
    captcha_lbl=Label(frm,text=generate_captcha(),font=('Helvetica',20),bg=root_color,fg=root_text_fg)
    captcha_lbl.place(relx=.45,rely=.4)

    refresh_btn=Button(frm,text='Refresh',command=refresh,fg=root_text_fg)
    refresh_btn.place(relx=.55,rely=.4)

    inputcap_lbl=Label(frm,text='Captcha',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    inputcap_lbl.place(relx=.35,rely=.5)
    inputcap_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
    inputcap_entry.place(relx=.45,rely=.5)

    login_btn=Button(frm,text='Login',command=login,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
    login_btn.place(relx=.463,rely=.62)
    reset_btn=Button(frm,text='Reset',command=reset,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
    reset_btn.place(relx=.563,rely=.62)
    forgot_pass_btn=Button(frm,text='Forgot Password',command=forgot_pass,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
    forgot_pass_btn.place(relx=.475,rely=.72)

def admin_screen():
    current_frm=[]

    def clear_frm():
        if current_frm:
            current_frm[0].destroy()
            current_frm.clear()

    def open_acn():
        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.15,rely=0,relwidth=.848,relheight=1)
        current_frm.append(ifrm)

        def db_open_acn():
            uemail=email_entry.get()
            pattern=r'[\w.&-]+@[a-zA-Z]+\.[a-zA-Z]+'
            if not re.fullmatch(pattern,uemail):
                messagebox.showerror('Invalid email','Invalid email!')
                return
            submit_btn.config(state='disabled')
            processing_lbl=Label(ifrm,text='Creating account, do not press the back button or switch screen!',font=('Helvetica',10,'bold'),bg=root_color,fg=root_text_fg)
            processing_lbl.place(relx=.43,rely=.588)
            uname=name_entry.get()
            upass=generate_captcha()
            umob=mobile_entry.get()
            usex=sex_combo.get()
            uacn_open_date=today
            ubal=0.0
            uaddress=address_entry.get()
            upan=pan_entry.get()
            upassport=passport_entry.get()

            try:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='insert into accounts values(null,?,?,?,?,?,?,?,?,?,?)'
                curobj.execute(query,(uname,upass,uemail,umob,usex,uacn_open_date,ubal,uaddress,upan,upassport))
                conobj.commit()
                conobj.close()
                
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select max(accounts_acno) from accounts')
                tup_urecord=curobj.fetchone()
                conobj.close()

                myproject_mail.acn_opening(user=uname,acno=tup_urecord[0],acn_open_date=uacn_open_date,acn_pass=upass,recipient=uemail)

                root.after(0,lambda: messagebox.showinfo('Account Open Success',f'Account opened! Details sent to user on email id: {uemail}'))
            except Exception as e:
                root.after(0,lambda e=e: messagebox.showerror('Account Open Error',e))

            processing_lbl.config(text='')
            submit_btn.config(state='normal')

        def db_open_acn_thread():
            Thread(target=db_open_acn).start()

        ifrm_welcome_lbl=Label(ifrm,text='Open Account Screen',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg)
        ifrm_welcome_lbl.pack()
        name_lbl=Label(ifrm,text='Name',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        name_lbl.place(relx=.03,rely=.13)
        name_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        name_entry.place(relx=.03,rely=.18)

        email_lbl=Label(ifrm,text='Email',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        email_lbl.place(relx=.38,rely=.13)
        email_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        email_entry.place(relx=.38,rely=.18)

        mobile_lbl=Label(ifrm,text='Mobile',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        mobile_lbl.place(relx=.73,rely=.13)
        mobile_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        mobile_entry.place(relx=.73,rely=.18)

        sex_lbl=Label(ifrm,text='Sex',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        sex_lbl.place(relx=.03,rely=.288)
        sex_combo=Combobox(ifrm,values=['Male','Female','Intersex'],font=('',20),width=17,state='readonly',justify='center')
        sex_combo.set('Select')
        sex_combo.place(relx=.03,rely=.338)

        passport_lbl=Label(ifrm,text='Passport',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        passport_lbl.place(relx=.38,rely=.288)
        passport_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        passport_entry.place(relx=.38,rely=.338)

        pan_lbl=Label(ifrm,text='PAN',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        pan_lbl.place(relx=.73,rely=.288)
        pan_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        pan_entry.place(relx=.73,rely=.338)

        address_lbl=Label(ifrm,text='Address',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        address_lbl.place(relx=.03,rely=.446)
        address_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        address_entry.place(relx=.03,rely=.496)

        submit_btn=Button(ifrm,text='Submit',command=db_open_acn_thread,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=child_window_color)
        submit_btn.place(relx=.43,rely=.654)

    def view_acn():
        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.15,rely=0,relwidth=.848,relheight=1)
        current_frm.append(ifrm)

        def view_acn_details():
            uacn=acno_entry.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where accounts_acno=?'
            row=curobj.execute(query,(uacn,))
            tup_urecord=row.fetchone()
            conobj.close()
            if tup_urecord==None:
                messagebox.showinfo('No record','Account does not exist')
                return

            user_data=myproject_db_sqlite.Accounts(*tup_urecord)

            ifrm_1=Frame(ifrm,bg=child_window_color)
            ifrm_1.place(relx=0.02,rely=.21,relheight=.45,relwidth=.46)
            ifrm_2=Frame(ifrm,bg=child_window_color)
            ifrm_2.place(relx=0.52,rely=.21,relheight=.45,relwidth=.46)

            udetails_dict_1={'Account Number:':user_data.uacno,'Account open date:':user_data.uacnopendate,
                        'Name:':user_data.uname,
                        'Sex:':user_data.usex,
                        'Available balance:':user_data.ubal}

            for i,(lbl_txt,uatt) in enumerate(udetails_dict_1.items()):
                Label(ifrm_1,text=lbl_txt,font=('Helvetica',20),width=15,bg=child_window_color,fg=root_text_fg,anchor='e').grid(row=i,column=0,padx=10,pady=5)
                Label(ifrm_1,text=uatt,font=('Helvetica',20),width=20,bg=child_window_color,anchor='w').grid(row=i,column=1,pady=5)

            udetails_dict_2={'Email:':user_data.uemail,'Mobile number:':user_data.umob,'Address:':user_data.uadd,
                            'PAN:':user_data.upan,'Passport:':user_data.upassport}

            for i,(lbl_txt,uatt) in enumerate(udetails_dict_2.items()):
                Label(ifrm_2,text=lbl_txt,font=('Helvetica',20),width=12,bg=child_window_color,fg=root_text_fg,anchor='e').grid(row=i,column=0,padx=10,pady=5)
                Label(ifrm_2,text=uatt,font=('Helvetica',20),width=24,bg=child_window_color,anchor='w').grid(row=i,column=1,pady=5)

        ifrm_welcome_lbl=Label(ifrm,text='View Account Screen',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg)
        ifrm_welcome_lbl.pack()

        acno_lbl=Label(ifrm,text='Account No.',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        acno_lbl.place(relx=.03,rely=.11)
        acno_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        acno_entry.place(relx=.16,rely=.11)

        view_btn=Button(ifrm,text='view',command=view_acn_details,font=('Helvetica',20,'bold'),fg=root_text_fg,highlightbackground=child_window_color)
        view_btn.place(relx=.43,rely=.11)

    def delete_acn():
        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.15,rely=0,relwidth=.848,relheight=1)

        def delete_acn_cnf():
            countdown_lbl=Label(ifrm,text='',font=('Helvetica',20),width=20,anchor='w',bg=root_color,fg=root_text_fg)
            countdown_lbl.place(relx=.4,rely=.41)
            countdown=30
            countdown_fun_scheduler=None
            def countdown_fun():
                nonlocal countdown,countdown_fun_scheduler
                if countdown>0:
                    countdown_lbl.config(text='')
                    countdown_lbl.config(text=f'Time left:{countdown}')
                    countdown-=1
                    countdown_fun_scheduler=root.after(1000,countdown_fun)
                else:
                    delete_acn_btn.config(state='normal',text='Resend OTP')
                    delete_acn_btn.place(relx=.21,rely=.41)
                    countdown_lbl.config(text='OTP expired')
                    captcha_lbl.config(text=generate_captcha())

            def submit():
                nonlocal countdown_fun_scheduler
                if delete_acn_btn['state']=='normal':
                    root.after(0,lambda: messagebox.showerror('otp expired','OTP expired, please resend!'))
                    return
                if enter_otp_entry.get()==otp_gen:
                    if countdown_fun_scheduler:
                        root.after_cancel(countdown_fun_scheduler)
                    countdown_lbl.config(text='')
                    def handle_cnf():
                        resp=messagebox.askyesno('confirm',f"Are you sure you want to delete Account no. {tup_uacno[0]} of user '{tup_uacno[1]}' ?")
                        if resp is True:
                            acn_status_lbl=Label(ifrm,text='Deleting account, please wait...',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
                            acn_status_lbl.place(relx=.23,rely=.71)
                            def delete_acn_logic():
                                try:
                                    conobj=sqlite3.connect(database='bank.sqlite')
                                    curobj=conobj.cursor()
                                    query='delete from accounts where accounts_acno=?'
                                    curobj.execute(query,(tup_uacno[0],))
                                    conobj.commit()
                                    conobj.close()
                                    acn_status_lbl.config(text='')
                                    root.after(0,lambda: messagebox.showinfo('deleted',f"Account deleted successfully!"))
                                except Exception as e:
                                    root.after(0,lambda e=e: messagebox.showerror('error',e))
                                ifrm.destroy()
                                delete_acn()
                            Thread(target=delete_acn_logic).start()
                        elif resp is False:
                            root.after(0, lambda: messagebox.showinfo('Aborted', 'Account deletion aborted.'))
                            ifrm.destroy()
                            delete_acn()
                    root.after(0,handle_cnf)
                else:
                    root.after(0,lambda: messagebox.showerror('invalid otp','Invalid OTP!'))
                    
            delete_acn_btn.config(state='disabled')
            uacno=acno_entry.get()
            admin_captcha=inputcap_entry.get()
            actual_captcha=captcha_lbl.cget('text')
            if admin_captcha!=actual_captcha:
                root.after(0,lambda: messagebox.showerror('Incorrect captcha','Incorrect captcha'))
                delete_acn_btn.config(state='normal')
                captcha_lbl.config(text=generate_captcha())
                return
            
            try:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where accounts_acno=?'
                row=curobj.execute(query,(uacno,))
                tup_uacno=row.fetchone()
                conobj.close()
                if not tup_uacno:
                    root.after(0,lambda: messagebox.showerror('No record','Account does not exist'))
                    delete_acn_btn.config(state='normal')
                    captcha_lbl.config(text=generate_captcha())
                    return

                otp_gen=str(random.randint(1000,9999))
                myproject_mail.acn_deletion(tup_uacno[0],tup_uacno[1],otp_gen,tup_uacno[3])
                root.after(0,lambda: messagebox.showinfo('otp',f'OTP sent on user email {tup_uacno[3]}'))
            except Exception as e:
                root.after(0,lambda: messagebox.showerror('error',e))
                delete_acn_btn.config(state='normal')
                ifrm.destroy()
                delete_acn()
                return
            countdown_fun()
            
            enter_otp_lbl=Label(ifrm,text='Enter OTP',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
            enter_otp_lbl.place(relx=.03,rely=.51)
            enter_otp_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
            enter_otp_entry.place(relx=.16,rely=.51)
            submit_btn=Button(ifrm,text='Submit',command=submit,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=child_window_color)
            submit_btn.place(relx=.23,rely=.61)

        def delete_acn_cnf_thread():
            Thread(target=delete_acn_cnf).start()

        ifrm_welcome_lbl=Label(ifrm,text='Delete Account Screen',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg)
        ifrm_welcome_lbl.pack()
        current_frm.append(ifrm)

        acno_lbl=Label(ifrm,text='Account No.',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        acno_lbl.place(relx=.03,rely=.11)
        acno_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        acno_entry.place(relx=.16,rely=.11)
        global captcha_lbl
        captcha_lbl=Label(ifrm,text=generate_captcha(),font=('Helvetica',20),bg=root_text_fg,fg=root_color)
        captcha_lbl.place(relx=.16,rely=.21)
        refresh_btn=Button(ifrm,text='Refresh',command=refresh,borderwidth=0,highlightthickness=0,bg=child_window_color,fg=root_text_fg)
        refresh_btn.place(relx=.26,rely=.21)

        inputcap_lbl=Label(ifrm,text='Captcha',font=('Helvetica',20,'bold'),bg=root_color,fg=root_text_fg)
        inputcap_lbl.place(relx=.03,rely=.31)
        inputcap_entry=Entry(ifrm,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color)
        inputcap_entry.place(relx=.16,rely=.31)

        delete_acn_btn=Button(ifrm,text='Delete',font=('Helvetica',17,'bold'),command=delete_acn_cnf_thread,fg=root_text_fg,highlightbackground=child_window_color)
        delete_acn_btn.place(relx=.23,rely=.41)

    def logout():
        response=messagebox.askyesnocancel('Logout','Are you sure you want to logout?')
        if response:
            frm.destroy()
            main_screen()
    
    def choose_photo_fun():
        nonlocal path_img
        path=filedialog.askopenfilename()
        if not path:
            return
        shutil.copy(path,'my_project_imgs/x-admin_img-y.png')
        admin_img=Image.open(path_img:='my_project_imgs/x-admin_img-y.png').resize((150,170))
        admin_img_bitmap=ImageTk.PhotoImage(admin_img,master=root)
        default_img_bitmap_lbl.image=admin_img_bitmap
        default_img_bitmap_lbl.config(image=admin_img_bitmap)
    
    def delete_photo_fun():
        nonlocal path_img
        if path_img=='my_project_imgs/default_img.png':
            messagebox.showerror('error','Cannot delete default photo')
            return
        if os.path.exists('my_project_imgs/x-admin_img-y.png'):
            resp=messagebox.askyesno('cnf','Are you sure you want to delete this photo?')
            if resp:
                os.remove('my_project_imgs/x-admin_img-y.png')
                default_img=Image.open(path_img:='my_project_imgs/default_img.png').resize((150,170))
                default_img_bitmap=ImageTk.PhotoImage(default_img,master=root)
                default_img_bitmap_lbl.image=default_img_bitmap
                default_img_bitmap_lbl.config(image=default_img_bitmap)
    
    def show_context_menu_fun(event):
        context_menu.tk_popup(event.x_root,event.y_root)

    frm=Frame(root)
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.75)
    frm.configure(bg=child_window_color)
    ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
    ifrm.place(relx=.15,rely=0,relwidth=.848,relheight=1)
    current_frm.append(ifrm)

    welcome_lbl=Label(frm,text='Welcome, Admin!',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    welcome_lbl.place(relx=0.01,rely=0.015)

    if os.path.exists('my_project_imgs/x-admin_img-y.png'):
        path_img='my_project_imgs/x-admin_img-y.png'
    else:
        path_img='my_project_imgs/default_img.png'

    default_img=Image.open(path_img).resize((150,170))
    default_img_bitmap=ImageTk.PhotoImage(default_img,master=root)
    default_img_bitmap_lbl=Label(frm,image=default_img_bitmap)
    default_img_bitmap_lbl.image=default_img_bitmap
    default_img_bitmap_lbl.place(relx=0.01,rely=0.115)

    edit_photo_lbl=Label(frm,text='📸',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    edit_photo_lbl.place(relx=0.11,rely=0.36)
    context_menu=Menu(frm,tearoff=0)
    context_menu.add_command(label='Choose photo',command=choose_photo_fun)
    context_menu.add_command(label='Delete existing',command=delete_photo_fun)

    edit_photo_lbl.bind('<Button-1>',show_context_menu_fun)

    openacn_btn=Button(frm,text='Open Account',command=open_acn,width=12,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    openacn_btn.place(relx=.01,rely=0.465)
    viewacn_btn=Button(frm,text='View Account',command=view_acn,width=12,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    viewacn_btn.place(relx=.01,rely=0.565)
    delacn_btn=Button(frm,text='Delete Account',command=delete_acn,width=12,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    delacn_btn.place(relx=.01,rely=0.665)
    logout_btn=Button(frm,text='Logout',command=logout,width=12,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    logout_btn.place(relx=.01,rely=0.765)

def forgot_pass_screen_user():
    def back():
        frm.destroy()
        main_screen()

    def send_otp():
        countdown_lbl=Label(frm,text='',font=('Helvetica',20),width=20,anchor='w',bg=child_window_color,fg=root_text_fg)
        countdown_lbl.place(relx=.624,rely=.3)
        countdown=30
        countdown_fun_scheduler=None
        def countdown_fun():
            nonlocal countdown,countdown_fun_scheduler
            if countdown>0:
                countdown_lbl.config(text='')
                countdown_lbl.config(text=f'Time left:{countdown}')
                countdown-=1
                countdown_fun_scheduler=root.after(1000,countdown_fun)
            else:
                send_otp_btn.config(state='normal',text='Resend OTP')
                send_otp_btn.place(relx=.504,rely=.3)
                countdown_lbl.config(text='OTP expired')
        
        def verify_otp():
            nonlocal countdown_fun_scheduler
            if send_otp_btn['state']=='normal':
                root.after(0,lambda: messagebox.showerror('otp expired','OTP expired, please resend!'))
                return
            if enter_otp_entry.get()==otp_gen:
                def change_pass_fun():
                    user_data=myproject_db_sqlite.Accounts(*tup_urecord)
                    if new_pass_entry.get()=='' or cnf_new_pass_entry.get()=='':
                        messagebox.showerror('empty','Empty field!')
                        return
                    if new_pass_entry.get()!=cnf_new_pass_entry.get():
                        messagebox.showerror('mismatch','Passwords do not match!')
                        return
                    if new_pass_entry.get()==user_data.upass:
                        messagebox.showerror('old pass','New password can not be same as last set password!')
                        return
                    user_data.update_pass(new_pass_entry.get(),user_data.uacno)
                    print(user_data.upass)
                    messagebox.showinfo('updated','Congratulations, your password has been reset successfully!')
                    main_screen()

                verify_otp_btn.config(state='disabled')
                if countdown_fun_scheduler:
                    root.after_cancel(countdown_fun_scheduler)
                countdown_lbl.config(text='')
                new_pass_lbl=Label(frm,text='New password:',width=18,anchor='e',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
                new_pass_lbl.place(relx=.255,rely=.6)
                new_pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
                new_pass_entry.place(relx=.45,rely=.6)
                cnf_new_pass_lbl=Label(frm,text='Confirm new password:',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
                cnf_new_pass_lbl.place(relx=.255,rely=.7)
                cnf_new_pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
                cnf_new_pass_entry.place(relx=.45,rely=.7)
                submit_btn=Button(frm,text='Submit',command=change_pass_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=child_window_color)
                submit_btn.place(relx=.504,rely=.8)

            else:
                root.after(0,lambda: messagebox.showerror('invalid otp','Invalid OTP!'))


        send_otp_btn.config(state='disabled')
        uacno=acno_entry.get()
        uemail=email_entry.get()
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where accounts_acno=? and accounts_email=?'
        row=curobj.execute(query,(uacno,uemail))
        tup_urecord=row.fetchone()
        conobj.close()

        if not tup_urecord:
            messagebox.showerror('error','Email/Account No. invalid!')
            send_otp_btn.config(state='normal')
            return
        
        enter_otp_lbl=Label(frm,text='Enter OTP',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
        enter_otp_lbl.place(relx=.315,rely=.4)
        enter_otp_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
        enter_otp_entry.place(relx=.45,rely=.4)
        verify_otp_btn=Button(frm,text='Verify OTP',command=verify_otp,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=child_window_color)
        verify_otp_btn.place(relx=.504,rely=.5)

        otp_gen=str(random.randint(1000,9999))
        myproject_mail.acn_deletion(tup_urecord[0],tup_urecord[1],otp_gen,tup_urecord[3])
        messagebox.showinfo('otp',f'OTP sent on user email {uemail}')
        countdown_fun()

    frm=Frame(root)
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.75)
    frm.configure(bg=child_window_color)

    back_btn=Button(frm,text='Back',command=back,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
    back_btn.place(relx=.01,rely=0.015)

    acno_lbl=Label(frm,text='Account No.',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    acno_lbl.place(relx=.34,rely=.1)
    acno_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
    acno_entry.place(relx=.45,rely=.1)

    email_lbl=Label(frm,text='Email',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    email_lbl.place(relx=.385,rely=.2)
    email_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color)
    email_entry.place(relx=.45,rely=.2)

    send_otp_btn=Button(frm,text='Send OTP',command=send_otp,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
    send_otp_btn.place(relx=.504,rely=.3)

def user_screen_fun(user_data:myproject_db_sqlite.Accounts):
    current_frm=[]

    def clear_frm():
        if current_frm:
            current_frm[0].destroy()
            current_frm.clear()

    def profile():
        def toggle_edit_save_fun():
            updated_udetails_li=[]
            if edit_save_btn['text']=='Edit':
                for lbl,entry in entries.items():
                    if lbl not in ('Account Number:','Account open date:','Name:','Sex:','Available balance:'):
                        entry.config(state='normal')
                edit_save_btn.config(text='Save')
            else:
                resp=messagebox.askyesno('cnf','Are you sure you want to save these changes?')
                if not resp:
                    return
                for lbl,entry in entries.items():
                    if lbl not in ('Account Number:','Account open date:','Name:','Sex:','Available balance:'):
                        updated_udetails_li.append(entry.get())
                        entry.config(state='disabled')
                print(updated_udetails_li)
                user_data.update_att(user_data.uacno,updated_udetails_li[0],
updated_udetails_li[1],updated_udetails_li[2],updated_udetails_li[3],updated_udetails_li[4])
                edit_save_btn.config(text='Edit')
        
        def current_pass_fun():
            change_pass_btn.config(state='disabled')
            def verify_current_pass_fun():
                def change_pass_fun():
                    if new_pass_entry.get()=='' or cnf_new_pass_entry.get()=='':
                        messagebox.showerror('empty','Empty field!')
                        return
                    if new_pass_entry.get()!=cnf_new_pass_entry.get():
                        messagebox.showerror('mismatch','Passwords do not match!')
                        return
                    if new_pass_entry.get()==current_pass:
                        messagebox.showerror('old pass','New password can not be same as last set password!')
                        return
                    user_data.update_pass(new_pass_entry.get(),user_data.uacno)
                    print(user_data.upass)
                    messagebox.showinfo('updated','Congratulations, your password has been reset successfully!')
                    profile()
                
                current_pass=current_pass_entry.get()
                if current_pass_entry.get()!=user_data.upass:
                    messagebox.showerror('wrong pass','Incorrect password!')
                    return
                current_pass_lbl.destroy()
                current_pass_entry.destroy()
                verify_current_pass_btn.destroy()
                new_pass_lbl=Label(frm,text='New password:',width=14,anchor='e',font=('Helvetica',20),bg=root_color,fg=root_text_fg)
                new_pass_lbl.place(relx=.35,rely=.7)
                new_pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color,bg=child_window_color)
                new_pass_entry.place(relx=.5,rely=.7)
                cnf_new_pass_lbl=Label(frm,text='Confirm new password:',width=20,anchor='e',font=('Helvetica',20),bg=root_color,fg=root_text_fg)
                cnf_new_pass_lbl.place(relx=.3,rely=.8)
                cnf_new_pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color,bg=child_window_color)
                cnf_new_pass_entry.place(relx=.5,rely=.8)
                submit_btn=Button(ifrm,text='Submit',command=change_pass_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
                submit_btn.place(relx=.45,rely=.9)

            current_pass_lbl=Label(frm,text='Current password:',font=('Helvetica',20),bg=root_color,fg=root_text_fg)
            current_pass_lbl.place(relx=.35,rely=.7)
            current_pass_entry=Entry(frm,font=('Helvetica',20),bd=2.3,highlightbackground=root_color,bg=child_window_color)
            current_pass_entry.place(relx=.5,rely=.7)
            verify_current_pass_btn=Button(ifrm,text='Verify',command=verify_current_pass_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
            verify_current_pass_btn.place(relx=.63,rely=.7)

        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.2,rely=0,relwidth=.798,relheight=1)
        current_frm.append(ifrm)

        ifrm_welcome_lbl=Label(ifrm,text='Profile View',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg)
        ifrm_welcome_lbl.pack()

        ifrm_1=Frame(ifrm,bg=child_window_color)
        ifrm_1.place(relx=0.02,rely=.1,relheight=.45,relwidth=.46)
        ifrm_2=Frame(ifrm,bg=child_window_color)
        ifrm_2.place(relx=0.52,rely=.1,relheight=.45,relwidth=.46)

        udetails_dict_1={'Account Number:':user_data.uacno,'Account open date:':user_data.uacnopendate,
                       'Name:':user_data.uname,
                       'Sex:':user_data.usex,
                       'Available balance:':user_data.ubal}

        for i,(lbl_txt,uatt) in enumerate(udetails_dict_1.items()):
            Label(ifrm_1,text=lbl_txt,font=('Helvetica',20),width=15,bg=child_window_color,fg=root_text_fg,anchor='e').grid(row=i,column=0,padx=10,pady=5)
            Label(ifrm_1,text=uatt,font=('Helvetica',20),width=20,bg=child_window_color,anchor='w').grid(row=i,column=1,pady=5)

        udetails_dict_2={'Email:':user_data.uemail,'Mobile number:':user_data.umob,'Address:':user_data.uadd,
                        'PAN:':user_data.upan,'Passport:':user_data.upassport}
        
        entries={}

        for i,(lbl_txt,uatt) in enumerate(udetails_dict_2.items()):
            Label(ifrm_2,text=lbl_txt,font=('Helvetica',20),width=12,bg=child_window_color,fg=root_text_fg,anchor='e').grid(row=i,column=0,padx=10,pady=5)

            ent=Entry(ifrm_2,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color,bg=root_color)
            ent.insert(0,uatt)
            ent.grid(row=i,column=1,pady=5)
            ent.config(state='disabled')
            entries[lbl_txt]=ent

        edit_save_btn=Button(ifrm_2,text='Edit',command=toggle_edit_save_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
        edit_save_btn.grid(row=len(udetails_dict_2),column=1,sticky='e',pady=5)

        change_pass_btn=Button(ifrm,text='Change password',command=current_pass_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg)
        change_pass_btn.place(relx=.4,rely=.6)

    def transact_fun():
        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.2,rely=0,relwidth=.798,relheight=1)
        ifrm.grid_propagate(False)
        current_frm.append(ifrm)

        ifrm_welcome_lbl=Label(ifrm,text='Transact screen',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg)
        ifrm_welcome_lbl.pack()

        # Combobox - fixed at top-left (row=0)
        combo = Combobox(ifrm, values=['Deposit', 'Withdraw', 'Transfer within bank'], state="readonly", font=('Helvetica', 20),justify='center')
        combo.set('Select an action')
        combo.pack(pady=20)

        # Dynamic frame starts below combobox (row=1)
        dynamic_frame = Frame(ifrm, bg=root_color)
        dynamic_frame.pack(pady=20)

        # Function to update widgets based on selection
        def on_selection(event):
            selected = combo.get()

            # Clear existing widgets in dynamic_frame
            for widget in dynamic_frame.winfo_children():
                widget.destroy()

            # Add new widgets depending on selection
            if selected == 'Deposit':
                def deposit_fun():
                    try:
                        if float(deposit_ent.get())<=0:
                            messagebox.showerror('invalid','Invalid amount!')
                            return
                        pbal=user_data.ubal
                        user_data.deposit(float(deposit_ent.get()),user_data.uacno)
                        myproject_db_sqlite.stmts('credit',user_data.uacno,float(deposit_ent.get()),pbal,user_data.ubal)
                        messagebox.showinfo('deposited',f'Rs {deposit_ent.get()} have been deposited in your account!')
                        transact_fun()
                    except ValueError as e:
                        messagebox.showerror('invalid',e)
                Label(dynamic_frame, text="Account Balance:", font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=0, column=0, sticky='w',padx=5,pady=10)
                Label(dynamic_frame, text=user_data.ubal, font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=0, column=1, sticky='w',padx=5,pady=10)
                Label(dynamic_frame, text="Deposit Amount:", font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=1, column=0, sticky='w',padx=5,pady=10)
                deposit_ent=Entry(dynamic_frame,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color,bg=child_window_color)
                deposit_ent.grid(row=1, column=1,pady=10)
                Button(dynamic_frame,text='Deposit',command=deposit_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg).grid(row=2,column=1,padx=10,pady=10)

            elif selected == 'Withdraw':
                def withdraw_fun():
                    try:
                        if float(withdraw_ent.get())>user_data.ubal:
                            messagebox.showerror('invalid','Insufficient balance!')
                            return
                        if float(withdraw_ent.get())<=0:
                            messagebox.showerror('invalid','Invalid amount!')
                            return
                        pbal=user_data.ubal
                        user_data.withdraw(float(withdraw_ent.get()),user_data.uacno)
                        myproject_db_sqlite.stmts('debit',user_data.uacno,float(withdraw_ent.get()),pbal,user_data.ubal)
                        messagebox.showinfo('deposited',f'Rs {withdraw_ent.get()} have been debited from your account!')
                        transact_fun()
                    except ValueError as e:
                        messagebox.showerror('invalid',e)
                Label(dynamic_frame, text="Account Balance:", font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=0, column=0, sticky='w',padx=5,pady=10)
                Label(dynamic_frame, text=user_data.ubal, font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=0, column=1, sticky='w',padx=5,pady=10)
                Label(dynamic_frame, text="Withdraw Amount:", font=('Helvetica', 20), bg=root_color,fg=root_text_fg).grid(row=1, column=0, sticky='w',padx=5,pady=10)
                withdraw_ent=Entry(dynamic_frame,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color,bg=child_window_color)
                withdraw_ent.grid(row=1, column=1,pady=10)
                Button(dynamic_frame,text='Withdraw',command=withdraw_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg).grid(row=2,column=1,padx=10,pady=10)

            elif selected == "Transfer within bank":
                def transfer_fun():
                    try:
                        if int(to_acn_ent.get())==user_data.uacno:
                            messagebox.showerror('invalid','Can not transfer to own account!')
                            return
                        if int(to_acn_ent.get()) not in user_data.acnos():
                            messagebox.showerror('invalid acno','Destination account does not exist!')
                            return
                        if float(amt_ent.get())>user_data.ubal:
                            messagebox.showerror('invalid','Insufficient balance!')
                            return
                        if float(amt_ent.get())<=0:
                            messagebox.showerror('invalid','Invalid amount!')
                            return
                        from_acn_pbal=user_data.ubal
                        tup=user_data.transfer(float(amt_ent.get()),user_data.uacno,int(to_acn_ent.get()))
                        myproject_db_sqlite.stmts('debit',user_data.uacno,float(amt_ent.get()),from_acn_pbal,user_data.ubal,f'To Account number:{int(to_acn_ent.get())}')
                        myproject_db_sqlite.stmts('credit',int(to_acn_ent.get()),float(amt_ent.get()),tup[0],tup[1],f'From Account number:{user_data.uacno}')
                        messagebox.showinfo('transferred',f'Rs {amt_ent.get()} have been transferred to Account number:{to_acn_ent.get()} from your account!')
                        transact_fun()
                    except ValueError as e:
                        messagebox.showerror('invalid',e)
                    
                Label(dynamic_frame, text="Account Balance:", font=('Helvetica', 20),width=14,anchor='e', bg=root_color,fg=root_text_fg).grid(row=0, column=0, sticky='w',pady=10)
                Label(dynamic_frame, text=user_data.ubal, font=('Helvetica', 20),bg=root_color,fg=root_text_fg).grid(row=0, column=1, sticky='w',padx=5,pady=10)
                Label(dynamic_frame, text="To account:", font=('Helvetica', 20),width=14,anchor='e',bg=root_color,fg=root_text_fg).grid(row=1, column=0, sticky='w',padx=5,pady=10)
                to_acn_ent=Entry(dynamic_frame,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color,bg=child_window_color)
                to_acn_ent.grid(row=1, column=1,pady=10)
                Label(dynamic_frame, text="Transfer amount:", font=('Helvetica', 20), width=14,anchor='e',bg=root_color,fg=root_text_fg).grid(row=2, column=0, sticky='w',pady=10)
                amt_ent=Entry(dynamic_frame,font=('Helvetica',20),bd=2.3,highlightbackground=child_window_color,bg=child_window_color)
                amt_ent.grid(row=2, column=1,pady=10)
                Button(dynamic_frame,text='Transfer',command=transfer_fun,font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg).grid(row=3,column=1,padx=10,pady=10)

        # Bind event
        combo.bind("<<ComboboxSelected>>", on_selection)

    def transaction_history():
        clear_frm()
        ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
        ifrm.place(relx=.2,rely=0,relwidth=.798,relheight=1)
        current_frm.append(ifrm)

        ifrm_welcome_lbl=Label(ifrm,text='Transaction History Screen',font=('Helvetica',20),bg=child_window_color,fg=root_text_fg,pady=10)
        ifrm_welcome_lbl.pack(anchor='n')

        # --- Treeview Style Config ---
        style = Style()
        # style.theme_use('default')

        style.configure("Custom.Treeview",
            background=root_color,
            foreground="black",
            rowheight=28,
            fieldbackground=root_color,
            borderwidth=1,
            relief='solid'
        )

        style.configure("Custom.Treeview.Heading",
            background=child_window_color,
            foreground=root_text_fg,
            font=('Helvetica', 15, 'bold'),
            anchor='center'
        )

        style.map("Custom.Treeview", background=[('selected',child_window_color)])

        # --- Frame to hold Treeview + Scrollbars ---
        table_frame = Frame(ifrm, bg=root_color)
        table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Scrollbars ---
        x_scroll = Scrollbar(table_frame, orient=HORIZONTAL)
        y_scroll = Scrollbar(table_frame, orient=VERTICAL)

        # --- Treeview ---
        columns = ('txn_id', 'date', 'amt', 'type', 'previous bal', 'updated bal', 'transfer')
        
        border_frame = Frame(table_frame, bg=root_text_fg, bd=1, relief="solid")
        border_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        tree = Treeview(
            border_frame,
            columns=columns,
            show='headings',
            style='Custom.Treeview',
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        # Attach scrollbars
        x_scroll.config(command=tree.xview)
        y_scroll.config(command=tree.yview)
        x_scroll.pack(side=BOTTOM, fill=X)
        y_scroll.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=True)

        # --- Define headings & center align text ---
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            
            if col in ('amt', 'type'):
                tree.column(col, anchor='center', width=80)
            elif col in ('date', 'transfer'):
                tree.column(col, anchor='center', width=180)
            else:
                tree.column(col, anchor='center', width=120)

        # --- Fetch & insert data ---
        rows=myproject_db_sqlite.ustmts(user_data.uacno)

        for row in rows:
            tree.insert("", END, values=row)

    def logout():
        response=messagebox.askyesnocancel('Logout','Are you sure you want to logout?')
        if response:
            frm.destroy()
            main_screen()
    
    def choose_photo_fun():
        nonlocal path_profile_picture
        path=filedialog.askopenfilename()
        if not path:
            return
        shutil.copy(path,f'my_project_imgs/{user_data.uacno}.png')
        uimg=Image.open(path_profile_picture:=f'my_project_imgs/{user_data.uacno}.png').resize((170,150))
        uimg_bitmap=ImageTk.PhotoImage(uimg,master=root)
        user_img_bitmap_lbl.image=uimg_bitmap
        user_img_bitmap_lbl.config(image=uimg_bitmap)

    def delete_photo_fun():
        nonlocal path_profile_picture
        if path_profile_picture=='my_project_imgs/default_img.png':
            messagebox.showerror('error','Cannot delete default photo')
            return
        if not os.path.exists(path_profile_picture):
            return
        resp=messagebox.askyesno('cnf','Are you sure you want to delete your existing photo?')
        if resp:
            os.remove(path_profile_picture)
            user_img=Image.open(path_profile_picture:='my_project_imgs/default_img.png').resize((170,150))
            user_img_bitmap=ImageTk.PhotoImage(user_img,master=root)
            user_img_bitmap_lbl.image=user_img_bitmap
            user_img_bitmap_lbl.config(image=user_img_bitmap)

    def show_context_menu(event):
        context_menu.tk_popup(event.x_root,event.y_root)

    frm=Frame(root)
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.75)
    frm.configure(bg=child_window_color)
    ifrm=Frame(frm,bg=root_color,highlightthickness=2,highlightbackground=child_window_color)
    ifrm.place(relx=.2,rely=0,relwidth=.798,relheight=1)
    current_frm.append(ifrm)

    welcome_lbl=Label(frm,text=f'Welcome, {user_data.uname}!',font=('Helvetica',20,'bold'),bg=child_window_color,fg=root_text_fg)
    welcome_lbl.pack(side='top',anchor='w',padx=10,pady=10)

    if os.path.exists(f'my_project_imgs/{user_data.uacno}.png'):
        path_profile_picture=f'my_project_imgs/{user_data.uacno}.png'
    else:
        path_profile_picture='my_project_imgs/default_img.png'
    
    user_img=Image.open(path_profile_picture).resize((170,150))
    user_img_bitmap=ImageTk.PhotoImage(user_img,master=root)
    user_img_bitmap_lbl=Label(frm,image=user_img_bitmap)
    user_img_bitmap_lbl.image=user_img_bitmap
    user_img_bitmap_lbl.pack(side='top',anchor='w',padx=25,pady=10)

    edit_photo_lbl=Label(frm,text='📸',font=('Helvetica',20),bg=child_window_color,anchor='nw')
    edit_photo_lbl.place(relx=.132,rely=.3173)

    context_menu=Menu(frm,tearoff=0)
    context_menu.add_command(label='Choose photo',command=choose_photo_fun)
    context_menu.add_command(label='Delete existing',command=delete_photo_fun)

    edit_photo_lbl.bind('<Button-1>',show_context_menu)

    profile_btn=Button(frm,text='Profile',command=profile,width=16,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    profile_btn.pack(side='top',anchor='w',padx=25,pady=10)
    transact_btn=Button(frm,text='Transact',command=transact_fun,width=16,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    transact_btn.pack(side='top',anchor='w',padx=25,pady=10)
    transaction_history_btn=Button(frm,text='Transaction history',command=transaction_history,width=16,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    transaction_history_btn.pack(side='top',anchor='w',padx=25,pady=10)
    logout_btn=Button(frm,text='Logout',command=logout,width=16,anchor='c',font=('Helvetica',17,'bold'),bd=2.3,fg=root_text_fg,highlightbackground=root_color)
    logout_btn.pack(side='top',anchor='w',padx=25,pady=10)

main_screen()
root.mainloop()