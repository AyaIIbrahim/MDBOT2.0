    // Javascript code for the bot ui

var botui = new BotUI('pan-bot-ui');
        botui.message.add({
            delay: 1000,
            loading: true,
            content: 'يومك سعيد, أنا هبقى مساعدك الشخصي النهاردة'
        }).then(function() {
            botui.message.add({ // show a message
                delay: 1000,
                loading: true,
                content: 'اسمك ايه؟'
            }).then(function() { // wait till its shown
                return botui.action.text({ // show 'text' action
                    action: {
                        placeholder: 'Your name'
                    }
                });
            }).then(function(res) { // get the result
                botui.message.add({
                    content: 'اتمنالك يوم كويس يا ' + res.value + ', ' +
                        'اساعدك ازاي؟'
                });
            })
            
            
            .then(function() { // The questions the bot can answer, set 1
                return botui.action.button({
                    delay: 1000,
                    loading: true,
                    action: [{
                        text: 'فحص أسنان',
                        value: 'dent'
                    }, {
                        text: 'فحص طبي عام',
                        value: 'symp'
                    }]
                });
            })          
                        
            .then(function(res) { //the answer to bot questions
                var message;
                
                if (res.value === "dent") {
                    window.location.href = "/dent";
                }
                
                if (res.value === "symp") {
                    window.location.href = "/info";
                } else if (res.value == "newbie") {
                    message =
                        ' fill<br>' +
                        ' fill' +
                        ' fill';
                } else if (res.value === "join") {
                    message =
                        'fill ' +
                        'fill';
                } else if (res.value === "free") {
                    message =
                        'fill';
                } else if (res.value === "support") {
                    message =
                        'fill' +
                        'fill';
                } else if (res.value === "need") {
                    message =
                        'fill' +
                        'fill';
                } else if (res.value === "medical") {
                    message =
                        'fill' +
                        'fill' +
                        'Backend Development <br> Machine Learning' ;
                } else if (res.value === "doc_job") {
                    message =
                        'fill ' +
                        'fill ' +
                        'fill' ;
                }
                return botui.message.add({
                    type: 'html',
                    delay: 1000,
                    loading: true,
                    content: message
                });
            })
   
            .then(function() { //confirm if user has more questions
               return botui.action.button({
                   delay: 1000,
                   loading: true,
                   action: [{
                       text: "No! I don't have any more questions",
                       value: 'noquestion'
                   }, {
                       text: 'Yes! I have more questions',
                       value: 'question'
                   }]
               });
           })
             
           .then(function(res) { // responses to question confirmation
               var message;

               if (res.value === "noquestion") {
                   message =
                       'I wish you all the best';
               } else if (res.value === "question") {
                   message =
                       'For more questions, please visit our github project link ' +
                       '<a href="https://github.com/eris-ez/Medical-Chatbot">HERE</a>';
               }
               return botui.message.add({
                   type: 'html',
                   delay: 1000,
                   loading: true,
                   content: message
               });
           }).then(function(res) { //farewell button
                return botui.action.button({
                    action: [{
                        delay: 3000,
                        loading: true,
                        text: 'This has been very enlightening, thank you!',
                        value: 'cool'
                    }]
                });
            }).then(function(index) {
                return botui.message.add({
                    delay: 2000,
                    loading: true,
                    content: 'You are welcome'
                });
            }).then(function(index) {
                return botui.action.button({
                    action: [{
                        delay: 1000,
                        loading: true,
                        text: 'Goodbye',
                        value: 'bye'
                    }]
                });
            }).then(function(index) { //closing message
                return botui.message.add({
                    delay: 1000,
                    loading: true,
                    content: 'Bye, hope to see you again.'
                });
            });

        });
