var currentStep = 0;

const START_SCREEN = 'start';
const CONVERSATION_SCREEN = 'conversation';
const REASON_SCREEN = 'reason';
const END_SCREEN = 'end';
const SECONDS_PER_CONVERSATION = 300;

$(document).ready(function () {
    console.log(steps);
    surveyStep = steps[currentStep];
    showContent(surveyStep);
   
});

function getUserCode(){
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
    return params.code;
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
    screen_type = surveyStep['type'];

    switch(screen_type){
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
    var timer_countdown = setInterval(function () {
        var now = new Date()
        var distance = end_time.getTime() - now.getTime();
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        
        if (distance <= 0){
            clearInterval(timer_countdown);
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
    $('#countdown-content').css('visibility', 'hidden');
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
    $('#countdown-content').css('visibility', 'hidden');
    timeNow = new Date().getTime();
    steps[currentStep]['end_time'] = timeNow;
    steps[currentStep+1]['start_time'] = timeNow;
    showNextSurveyScreen();
    callRateConversation(steps[currentStep]['conversation_code'], timeNow, rating)
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
    reason = $('#reason-text').val();
    // TODO call /give-reason, record reason, conversation=steps[currentStep]['conversation_code'], update start_time for next conv.
    timeNow = new Date();
    steps[currentStep]['end_time'] = timeNow;
    if(steps[currentStep+1]['type'] === CONVERSATION_SCREEN){
        steps[currentStep+1]['start_time'] = timeNow;
    }
    showNextSurveyScreen();
}

function showEndTemplate(){
    template = $('#end-survey-template');
    renderContentTemplate(template, null);
    // TODO call /end-survey, update user survey_done
}
