var currentStep = 0;

const START_SCREEN = 'start';
const CONVERSATION_SCREEN = 'conversation';
const REASON_SCREEN = 'reason';
const END_SCREEN = 'end';
const ERROR_SCREEN = 'error';
var timeCountdown = null;

$(document).ready(function () {
    surveyStep = steps[currentStep];
    showContent(surveyStep);
   
});

function getUserCode(){
    return code;
}

function startSurvey(){
    timeNow = new Date().getTime()
    steps[currentStep]['end_time'] = timeNow
    steps[currentStep+1]['start_time'] = timeNow
    conversationScreenEndTime = new Date(timeNow + (SECONDS_PER_CONVERSATION * 1000))
    
    showNextSurveyScreen();
    callStartSurvey(timeNow, conversationScreenEndTime.getTime());

}

function callStartSurvey(time, conversationScreenEndTime){
    $.ajax({
        url: 'start-survey/',
        data: JSON.stringify({
            'start_time': time,
            'conversation_end_time': conversationScreenEndTime,
            'user_code': getUserCode()
        }),
        contentType:'application/json; charset=utf-8',
        dataType: 'json',
        type: 'POST',
        success: function(data){},
        error: function(error){},
        complete: function(){}

    });
}

function showNextSurveyScreen(){
    currentStep += 1;
    surveyStep = steps[currentStep];
    showContent(surveyStep);
}  

function showContent(surveyStep){
    screenType = surveyStep['type'];

    switch(screenType){
        case START_SCREEN:
            showStartTemplate(surveyStep)
            break;
        case CONVERSATION_SCREEN:
            showConversationTemplate(surveyStep);
            break;
        case REASON_SCREEN:
            showGiveReasonTemplate(surveyStep);
            break;
        case END_SCREEN:
            showEndTemplate();
            break;
        case ERROR_SCREEN:
            showErrorTemplate();
        default:
            break;
    }
}

function showStartTemplate(surveyStepData){
    var template = $.templates('#start-survey-template');
    renderContentTemplate(template, surveyStepData)

    $('#start-survey-btn').click(function(){
        startSurvey();
    });
}

function showConversationTemplate(surveyStepData){
    var template = $.templates('#rating-conversation-template');
    renderContentTemplate(template, surveyStepData)

    conversationScreenEndTime = new Date(surveyStepData['start_time'] + SECONDS_PER_CONVERSATION * 1000);
    showTimeCountdownUntil(conversationScreenEndTime);

    $('#finish-rating-btn').click(function(){
        finishRating();
    });
}

function showTimeCountdownUntil(end_time){
    timeCountdown = setInterval(function () {
        var now = new Date()
        var distance = end_time.getTime() - now.getTime();
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        if (seconds == 30 && minutes == 0){
            $('#countdown-alert').css('visibility', 'visible');
        }
        
        if (distance <= 0){
            $('#countdown-timer').text('00:00');
            endConversationScreenAfterCountdown();
            return;
        }
        var minutesLeft = '0' + minutes;
        var secondsLeft = seconds > 9? seconds : '0' + seconds;
        $('#countdown-timer').text(minutesLeft + ':' + secondsLeft);

    }, 1000);
    $('#countdown-content').css('visibility', 'visible');
}

function endConversationScreenAfterCountdown(){
    clearTimeCountdown();
    showNextSurveyScreen();
}

function showGiveReasonTemplate(){
    var template = $.templates('#give-reason-template');
    renderContentTemplate(template, null)

    $('#next-conversation-btn').click(function(){
        giveReason();
    });
}

function renderContentTemplate(template, surveyStepData){
    var renderedHtml = template.render(surveyStepData);
    var contentDiv = $('#content');
    contentDiv.html(renderedHtml);
}

function finishRating(){
    rating = $('input[name=rating]:checked').val()
    if(rating === undefined)
        return;
    
    clearTimeCountdown();
    
    timeNow = new Date().getTime();
    steps[currentStep]['end_time'] = timeNow;
    steps[currentStep+1]['start_time'] = timeNow;

    showNextSurveyScreen();
    callRateConversation(steps[currentStep-1]['conversation_code'], timeNow, rating)
}

function callRateConversation(conversationCode, timeNow, rating){
    $.ajax({
        url: 'rate-conversation/',
        data: JSON.stringify({
            'end_time': timeNow,
            'rating': rating,
            'conversation_code': conversationCode,
            'user_code': getUserCode()
        }),
        contentType:'application/json; charset=utf-8',
        dataType: 'json',
        type: 'POST',
        success: function(data){},
        error: function(error){},
        complete: function(){}

    });
}

function giveReason(){
    timeNow = new Date().getTime();
    steps[currentStep]['end_time'] = timeNow;

    var [startedConversationCode, startedConversationEndTime] = startNextConversation()

    reason = $('#reason-text').val();
    showNextSurveyScreen();
    callGiveReason(timeNow, reason, steps[currentStep-1]['conversation_code'], startedConversationEndTime, startedConversationCode);

}

function startNextConversation(){
    if(steps[currentStep+1]['type'] !== CONVERSATION_SCREEN){
        return [null, null];
    }

    startedConversationCode = steps[currentStep+1]['conversation_code'];
    steps[currentStep+1]['start_time'] = timeNow;
    startedConversationEndTime = new Date(steps[currentStep+1]['start_time'] + SECONDS_PER_CONVERSATION * 1000).getTime();

    return [startedConversationCode, startedConversationEndTime];
}

function callGiveReason(timeNow, reason, conversationCode, conversationEndTime, startedConversationCode){
    $.ajax({
        url: 'give-reason/',
        data: JSON.stringify({
            'conversation_start_time': timeNow,
            'conversation_end_time': conversationEndTime,
            'reason': reason,
            'started_conversation_code': startedConversationCode,
            'conversation_code': conversationCode,
            'user_code': getUserCode()
        }),
        contentType:'application/json; charset=utf-8',
        dataType: 'json',
        type: 'POST',
        success: function(data){},
        error: function(error){},
        complete: function(){}

    });
}

function showEndTemplate(){
    template = $('#end-survey-template');
    renderContentTemplate(template, null);
    callEndSurvey();
}


function callEndSurvey(){
    $.ajax({
        url: 'end-survey/',
        data: JSON.stringify({
            'user_code': getUserCode()
        }),
        contentType:'application/json; charset=utf-8',
        dataType: 'json',
        type: 'POST',
        success: function(data){},
        error: function(error){},
        complete: function(){}

    });
}


function clearTimeCountdown(){
    $('#countdown-timer').text('');
    clearInterval(timeCountdown);
    $('#countdown-content').css('visibility', 'hidden');
}

function showErrorTemplate(){
    var template = $.templates('#error-template');
    renderContentTemplate(template, null);
}