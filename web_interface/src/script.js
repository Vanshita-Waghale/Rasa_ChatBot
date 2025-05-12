function turnOffReminder() {
  // Implement logic to turn off the reminder
  alert("Reminder turned off.");
}

function snoozeReminder() {
  // Implement logic to snooze the reminder
  alert("Reminder snoozed.");
}

function setTimedReminder() {
  var reminderName = document.getElementById("reminderName").value;
  var reminderTime = document.getElementById("reminderTime").value;
  
  // Play the reminder sound
  var reminderSound = new Audio('C:\Users\ASUS\PycharmProjects\Chat_bot\reminder.mp3');
  reminderSound.play();
  
  // Implement logic to set a timed reminder with reminderName and reminderTime
  alert("Reminder '" + reminderName + "' set for " + reminderTime);
}

