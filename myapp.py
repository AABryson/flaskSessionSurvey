from flask import Flask, redirect, session, flash, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app=Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#the root page
@app.route('/')
def show_surveyTitle_Instructions():
    #show first page with title and directions which are attributes of survey object
    return render_template('mysurvey_start.html', survey=survey)
#review post
@app.route('/begin', methods=['POST'])
def now_for_questions():
    #session is dict like; so setting value of key to empty array
#initially forgot
    session[RESPONSES_KEY] = []
    #a.b. use redirect b/c not going to html file; going to other route
    return redirect('/questions/0')


@app.route('/questions/<int:num>')
#?????
def ask_question(num):
    #get the responses associated with key; is it an array?
#if from /begin redirect, session should be empty?
#remember, value of responseKey is a list; why () instead of[]?
    responses_so_far = session.get(RESPONSES_KEY)
#but isn't it none first time redirected from /begin?
#get the question to pass; from survey object
    question = survey.quesitons[num]
#originally tried to increment num
    # num += 1

#but isn't it none first time redirected from /begin?
#theirs: if (responses is None):
    if len(responses_so_far) is None:
        return redirect('/')
    # elif len(survey.questions) != len(responses_so_far):
    #    
    elif len(survey.questions) == len(responses_so_far):
        return redirect('/done')
    
    elif len(responses_so_far) != num:
# Trying to access questions out of order.
#forgot to use flash at first
        flash ('you cannot do the questions out of order')
        return redirect(f"/questions/{len(responses_so_far)}")
        

    #not sure why it question_num needed; doesn't seem to be used in myquestion.html
    return render_template('myquestion.htmml', question_num=num, question=question)
#mine: return render_template('myquestion.htmml', question=question)
    
    
@app.route('/answers', methods=['POST'])
def handle_answer():
# get the response choice; answer is value for name attribute in input
    form_answer = request.form['choice']
    responses = session[RESPONSES_KEY]
    responses.append(form_answer)
    # session[RESPONSES_KEY] = form_answer
    #I don't think I can do the above b/c would replace previous values in 
    # responseskey
    # responses_so_far = session[RESPONSES_KEY]
    #need to rebind I think.  Is responses array being added as value for key?
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/done")
    else:
    #remember to use f string
        return redirect(f'/questions/{len(responses)}')

@app.route('/done')
def you_finished():
    return render_template('mydone.html')

    

