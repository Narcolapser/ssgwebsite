At the beginning of this month, USD ITS had its 5th annual chili cook-off. Last year I was recruited in to help with notifying everyone and coordinating who was bringing what. To achieve this, I made a google form/spreadsheet and google site and wrote all sorts of clever spreadsheet functions to get the information and display it as desired. It also made me a list of people who hadn't responded yet so I could remind them. It worked really well but was not quite the amazing-ness I wanted. While a lot of it was streamlined, there were parts of it that still needed to be managed by hand. So this year I wanted to improve on that. So here are the things I tried and the lessons I learned.

#Flask-CAS

While I didn't end up using it, the first thing I tried to do was integrate Flask with our CAS (Central Authentication Service) servers. This would populate user name and email so you would just have to choose what you were bringing and hit submit. I got it to work, and it worked fine as long as you were inside the USD network. It wasn't going to work outside, and there was nowhere I could host my Flask server, so I had to forgo using this utility, but it was a good exercise in Flask and CAS. Time not wasted, in my opinion. The biggest lesson I learned from this escapade, though is that certs are annoying. 

#Cookies

Without the features that being CAS-ified allowed, I needed to find another way around that. So I turned to cookies. There isn't much to say on this front honestly. Cookies in Flask are soo incredibly easy that it's hardly worth mentioning. It looked something like this:

To set the cookie:

        resp = make_response(redirect('/chili'))
        resp.set_cookie('email',form.email.data)


To get the cookie:

        email = request.cookies.get('email')

~Tada! Like magic, I'm storing info in the user's browser. Amazing how simple this is.

#Flask Forms

This was also my first hurrah with Forms in Flask. It wasn't very hard, which is certainly something I appreciate about Flask specifically and python in general. Kind of the theme of this post "wasn't so hard since I was using python!" The thing I learned about though is mostly the declaring different types of methods in Flask and about the "make_response" method, which I used to redirect the user after they submitted their form:

        from flask import make_response


        @app.route('/register', methods=['GET', 'POST'])
        def register():
                form = RegistrationForm(request.form)
                if request.method == 'POST' and form.validate():
                        insert_resp(form.email.data,form.dish.data,form.nation.data)
                        resp = make_response(redirect('/chili'))
                        resp.set_cookie('email',form.email.data)
                        return resp
                return render_template('register.html', form=form, nations=nations, flags=flags)


#O365 Integration

This one was almost cheating. Not exactly something I learned since I wrote the O365 library. But it did serve a fantastic roll! This year the whole process was automated. As soon as I had the system up and running, it ran on its own, all the way through the holidays. I assembled it with a pair of files, all people, and have already responded. It would compare the two lists and then send a message to those yet to respond (and myself just so I could see that it was running.) It worked like a dream. Next year I will probably do something similar again. And now that I've got a lot of the coding managed already, it shouldn't take much effort. Though I'll probably put in a fair bit of energy so I can add cool new features!
