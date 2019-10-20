faqs = [{
    answer: 'How can I help you?'
}];

reloadChat();

function getToken() {
    generateToken();
    setInterval(() => generateToken(), 3500000)
}

function generateToken() {
    var orgId = "e2242208-c200-4b57-af40-9e855461cec7";
    var secretKey = "11b1af90-7ebf-4418-a3eb-7e34ba756c84";

    var xhr = new XMLHttpRequest();

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            var res = JSON.parse(this.responseText);
            console.log(res);
            localStorage.setItem('token', res.token);
        }
    });
    xhr.open("POST", "https://api.genesysappliedresearch.com/v2/knowledge/generatetoken");
    xhr.setRequestHeader("organizationid", "e2242208-c200-4b57-af40-9e855461cec7");
    xhr.setRequestHeader("secretkey", "11b1af90-7ebf-4418-a3eb-7e34ba756c84");
    xhr.send();

}

function submitQuestion() {
    if ($('#question').val() !== '') {
        faq = {
            question: $('#question').val()
        }
        faqs.push(faq);
        reloadChat();
        $('#question').val('');
        searchKnowledgeBase(faq.question);
    }
}

function searchKnowledgeBase(question) {
    console.log(question);
    var xhr = new XMLHttpRequest();
    var answer = "";
    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            res = JSON.parse(this.responseText);
            console.log(res);
            console.log(localStorage.getItem('token'));
            console.log(JSON.stringify(res));
            answer = res.results[0].faq.answer;
            faqs.filter(faq => faq.question === question)[0].answer = answer;
            reloadChat();
        }
    });
    xhr.open("POST", "https://api.genesysappliedresearch.com/v2/knowledge/knowledgebases/6f1d63c3-1da0-4a1f-b94f-6e6a412987ed/search");
    xhr.setRequestHeader("organizationid", "e2242208-c200-4b57-af40-9e855461cec7");
    xhr.setRequestHeader("token", localStorage.getItem('token'));
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send('{ "query":"' + question + '", "pageSize": 5, "pageNumber": 1, "sortOrder": "string", "sortBy": "string", "languageCode": "en-US", "documentType": "Faq"}');

}

function reloadChat() {
    $('#chat-container').empty();
    faqs.forEach(faq => {
        if (faq.hasOwnProperty('question')) {
            $('#chat-container').append('<ul class="p-0"> <li>' +
                '<div class = "row comments mb-2 ml-2" >' +
                '<div class = "col-md-9 col-sm-9 col-9 comment rounded mb-2 offset-md-2">' +
                '<h4 class = "m-0" > <a href = "#"> User </a></h4 >' +
                '<p class = "mb-0 text-white" >' + faq.question + '</p>' +
                '</div>' +
                '</div>' +
                '</li>' +
                '</ul>');
        }
        if(faq.hasOwnProperty('answer')) {
            $('#chat-container').append('<ul class="p-0"> <li>' +
                '<div class = "row comments mb-2 ml-2 answer" >' +
                '<div class = "col-md-9 col-sm-9 col-9 comment rounded mb-2">' +
                '<h4 class = "m-0" > <a href = "#"> Elections Canada </a></h4 >' +
                '<p class = "mb-0 text-white" >' + faq.answer + '</p>' +
                '</div>' +
                '</div>' +
                '</li>' +
                '</ul>')
        }
    });
}