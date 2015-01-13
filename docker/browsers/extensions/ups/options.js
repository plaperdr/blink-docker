// Saves options to localStorage.
function save_options() {
  var encryptionCheckbox = document.getElementById("passwordEncryption");
  var encryptionValue = encryptionCheckbox.checked;
  
  var storageCheckbox = document.getElementById("passwordStorage");
  var storageValue = storageCheckbox.checked;

  chrome.storage.sync.set({
	  passwordEncryption: encryptionValue,
	  passwordStorage: storageValue
  }, function() {
	  // Update status to let user know options were saved.
	  var status = document.getElementById("status");
	  status.innerHTML = "Options Saved.";
	  setTimeout(function() {
		  status.innerHTML = "";
	  }, 750);
  });
}

// Restores select box state to saved value from localStorage.
function restore_options() {
  chrome.storage.sync.get({
	  passwordEncryption: false,
	  passwordStorage: false
  }, function(items) {
	    document.getElementById('passwordEncryption').checked = items.passwordEncryption;
	    document.getElementById('passwordStorage').checked = items.passwordStorage;
  });
}

document.addEventListener('DOMContentLoaded', restore_options);
document.querySelector('#save').addEventListener('click', save_options);
