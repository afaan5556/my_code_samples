function getTrackerSheet(sheet_id, tab_name){
  // Get the g-sheet in which the data from emails needs to be tracked
  // sheet_id: The string sheet_id in the g-sheet url
  // tab_name: The name of the tab within the sheet where the data needs to be appended
  // return: The sheet
  var trackerSpreadSheet = SpreadsheetApp.openById(sheet_id)
  var trackerSheet = trackerSpreadSheet.getSheetByName(tab_name)
  return trackerSheet
}

function getThreads() {
  // Search the inbox for particular email threads
  // This example assumed unread threads with a specific string in the subject are needed
  // return: An array of the threads returned by the search
  var targetThreads = GmailApp.search('in:inbox is:unread subject:"mentioned you in a note about"')
  return targetThreads
}

function getSubject(thread){
  // Get the subject of a single email thread
  // thread: The email thread for which the subject needs to be extracted
  // return: The subject of the email
  var threadSubject = thread.getFirstMessageSubject()
  return threadSubject
}

function getTagger(thread_subject){
  // Get the name of the person that tagged you in an email
  // This example assumes the first and last names of the tagger are the first 2 words in the thread subject
  // thread_subject: The subject of the thread
  // return: The first and last name of the tagger as a single string
  var threadSubjectArray = thread_subject.split(" ")
  var tagger = threadSubjectArray.slice(0,2).join(" ")
  return tagger
}

function getSubjectField(thread_subject){
  // Get a particular field from the thread subject
  // This example assumes the field needed is after the word "about " in the thread subject
  // thread_subject: The subject of the thread
  // return: The text of interest, called subjectField here
  var subjectField = thread_subject.split("about ")[1]
  return subjectField
}

function getFirstMessage(thread){
  // Get the first email message in a thread
  // thread: A single thread returned by the search function
  // return: The first email message in the thread
  var firstMessage = thread.getFirstMessage()
  return firstMessage
}

function getBodyField(message){
  // Get a particular portion of text from an email body
  // This example assumes the text needed is between a ":" character and the word "View"
  // message: A first email in a search thread
  // return: The text of interest, called bodyField here
  var messageBody = message.getPlainBody()
  var bodyField = messageBody.split("View")[0]
  bodyField = bodyField.split(":")[1]
  return bodyField
}

function getMessageDate(message){
  // Get the date on which the first email in the thread was senet
  // message: A first email in a search thread
  // return: The date of the first email
  var date = message.getDate()
  return date
}

function addToTrackerSheet(sheet, data){
  // Add the parsed data to the tracker g-sheet
  // This example assumes the tracker sheet tab has the following column headers:
    // Date
    // Tagger
    // subjectField
    // bodyField
  // sheet: The tab within the tracker g-sheet where data should be appended
  // return: None
  var lastRowNumber = sheet.getLastRow() + 1
  sheet.getRange(lastRowNumber,1,1,4).setValues(data)
}

function updateTracker(){
  // Get the tracker sheet tab
  var trackerSheet = getTrackerSheet('<Enter tracker sheet id here>', '<Enter tracker sheet tab neame here>')
  // Get the target unread threads
  var threads = getThreads()
  // Set up empty arrays for data
  var taggers = []
  var subjectFields = []
  var bodyFields = []
  var dates = []
  // Iterate over target unread threads to populate data arrays
  for (var i = 0; i < threads.length; i++){
    var threadSubject = getSubject(threads[i])
    var message = getFirstMessage(threads[i])
    var bodyField = getBodyField(message)
    var date = getMessageDate(message)
    taggers.push(getTagger(threadSubject))
    subjectFields.push(getSubjectField(threadSubject))
    bodyFields.push(bodyField)
    dates.push(date)
    // Mark target unread thread as read
    threads[i].markRead()
  }
  // Iterate over data arrays to update tracker sheet
  for (var i = 0; i < taggers.length; i++){
    var payLoad = [[dates[i], subjectFields[i], taggers[i], bodyFields[i]]]
    addToTrackerSheet(trackerSheet, payLoad)
  }
}