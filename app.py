import os,flask
from flask import request, jsonify,json
from operator import itemgetter

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.

postfilename = os.path.join(app.static_folder, 'data', 'post.json')
with open(postfilename) as post_file:
    postsdata = json.load(post_file)

commentfilename = os.path.join(app.static_folder, 'data', 'comment.json')
with open(commentfilename) as comment_file:
    comments = json.load(comment_file)
@app.route('/api/v1/resources/posts', methods=['GET'])
def posts():
    post_data = []
    for post in postsdata:
        #data_disc = {"post_id":post["id"],"post_title":post["title"],"post_body":post["body"],"total_number_of_comments":0,"comments":[]}
        data_disc = {"post_id":post["id"],"post_title":post["title"],"post_body":post["body"],"total_number_of_comments":0}
        for comment in comments:
            if comment["postId"] == post["id"]:
                data_disc["total_number_of_comments"] = data_disc["total_number_of_comments"] + 1
                #data_disc["comments"].append(comment)
        post_data.append(data_disc)

    post_data = sorted(post_data,key=itemgetter('total_number_of_comments'),reverse=False)
    return jsonify(post_data)

@app.route('/api/v1/resources/getComment', methods=['GET'])
def getComment():
    reqargs = request.args
    name =  reqargs.get('name')
    email = reqargs.get('email')
    body = reqargs.get('body')
    if not name and not email and not body:
        return "error parameter not passed"
    else:
        if name and email and body:
            resultlist = [comment    for comment in comments     if comment.get('name', '') == name or comment.get('email', '') == email or comment.get('body', '') == body]
        elif name and email:
            resultlist = [comment    for comment in comments     if comment.get('name', '') == name or comment.get('email', '') == email]
        elif name and body:
            resultlist = [comment    for comment in comments     if comment.get('name', '') == name or comment.get('body', '') == body]
        elif body and email:
            resultlist = [comment    for comment in comments     if comment.get('email', '') == email or comment.get('body', '') == body]
        elif name:
            resultlist = [comment    for comment in comments     if comment.get('name', '') == name]
        elif body:
            resultlist = [comment    for comment in comments     if comment.get('body', '') == body]
        elif email:
            resultlist = [comment    for comment in comments     if comment.get('email', '') == email]
        return jsonify(resultlist)
app.run()