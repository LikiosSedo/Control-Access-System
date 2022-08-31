from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template #渲染
import function
app = Flask(__name__)
@app.route('/') #主页地址,“装饰器”
def news():
    context = {
        'match': 1,
    }
    return render_template('homepage.html',context=context) #把index.html⽂件读进来，再交给浏览器


@app.route("/submit", methods=["GET", "POST"])
# 从这里定义具体的函数 返回值均为json格式
def submit():
    # 由于POST、GET获取数据的方式不同，需要使用if语句进行判断
    if request.method == "POST":
        data_set_doc, vocabulary = function.load_file("document.txt")
        method=request.form.get("method")
        if method=="bool":
            query1 = request.form.get("query1")
            fileName = 'q1.txt'
            with open(fileName, 'w', encoding='UTF-8')as file:
                file.write("q1：")
                file.write(query1);
                file.write('\n')
            data_set_query, vocabulary_query = function.load_file("q1.txt")
            match_set=function.retrieve_by_boolean(data_set_doc, vocabulary, data_set_query['q1'])
            result=[]
            for item in match_set:
                line= [str(item), function.get_content()[item]]
                result.append(line)
            return {'result':result}




        if method=="vec":
            query2 = request.form.get("query2")
            print("query2",query2)
            fileName = 'q2.txt'
            with open(fileName, 'w', encoding='UTF-8')as file:
                file.write("q2：")
                file.write(query2);
                file.write('\n')
            data_set_query, vocabulary_query = function.load_file("q2.txt")
            ni = function.find_ni(data_set_doc, vocabulary)
            sim_set=function.retrieve_by_vector(data_set_query['q2'], data_set_doc, vocabulary, ni, len(data_set_doc))
            result = []
            for item in sim_set.keys():
                line = [str(item), function.get_content()[item], str(sim_set[item])]
                result.append(line)
            return {'result': result}



        if method=="invert":
            query3 = request.form.get("query3")
            print("query3",query3)
            fileName = 'q3.txt'
            with open(fileName, 'w', encoding='UTF-8')as file:
                file.write("q3：")
                file.write(query3)
                file.write('\n')
            data_set_query, vocabulary_query = function.load_file("q3.txt")
            ni = function.find_ni(data_set_doc, vocabulary)
            invert_index = function.get_voc_with_index("document.txt", vocabulary, ni)
            match_set=function.retrieve_by_invert(data_set_query['q3'], invert_index, data_set_doc)
            result = []
            for item in match_set:
                line = [str(item), function.get_content()[item]]
                result.append(line)
            print(result)
            return {'result': result}

        if method == "invert_visual":
            ni = function.find_ni(data_set_doc, vocabulary)
            invert_index = function.get_voc_with_index("document.txt", vocabulary, ni)
            result = []
            for word in invert_index:
                line = [str(word), str(ni[word]), str(invert_index[word])]
                result.append(line)
            print(result)
            return {'result': result}

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80) #127.0.0.1 回路⾃⼰返回⾃⼰
