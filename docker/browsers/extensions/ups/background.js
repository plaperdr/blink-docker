var callback = function () {
   console.log("Browsing data cleared")
};

chrome.browsingData.remove({}, {
    "appcache": true,
    "cache": true,
    "cookies": true,
    "downloads": true,
    "fileSystems": true,
    "indexedDB": true,
    "localStorage": true,
    "serverBoundCertificates": true,
    "pluginData": true,
    "passwords": true,
    "webSQL": true
}, callback);

var port = chrome.runtime.connectNative('com.ups.accessor');

//When the extension receives a message, all opened tabs
//are closed to open the new ones
port.onMessage.addListener(function(data) {
	//Import preferences
	chrome.storage.sync.set({
		passwordEncryption: data["passwordEncryption"],
		passwordStorage: data["passwordStorage"]
	}, function() {
	});
	
	//Clean Open tabs before opening the new ones
	chrome.tabs.query({}, function(tabs){
	    for (var i = 1; i < tabs.length; i++) {
	    	chrome.tabs.remove(tabs[i].id);                         
	    }
	    chrome.tabs.update(tabs[0].id,{"url": data["openTabs"][0].url})
	});
	
	//Open the new tabs
	for(i=1 ; i< data["openTabs"].length ; i++){
		chrome.tabs.create({"url": data["openTabs"][i].url});
	}
  
});
port.onDisconnect.addListener(function() {
  console.log("Disconnected");
});

//Add listeners
chrome.tabs.onCreated.addListener(tabCreated);
function tabCreated(){
	sendOpenTabs();
}

chrome.tabs.onRemoved.addListener(tabRemoved);
function tabRemoved(){
	sendOpenTabs();
}

chrome.tabs.onUpdated.addListener(tabUpdated);
function tabUpdated(){
	sendOpenTabs();
}

chrome.windows.onRemoved.addListener(windowClosed);
function windowClosed(){
	sendOpenTabs();
}

//Send open tabs and user preferences 
//to the native application
function sendOpenTabs(){
	chrome.tabs.query({}, function(tabs){
		trimmedTabs = [];
		var i;
		for(i=0;i<tabs.length;i++){
			trimmedTabs.push({url:tabs[i].url});
		}
		chrome.storage.sync.get({
			  passwordEncryption: false,
			  passwordStorage: false
		}, function(items) {
			port.postMessage({openTabs: trimmedTabs, passwordStorage: items.passwordStorage,
					passwordEncryption:items.passwordEncryption
			});
		});
		
	});
}



