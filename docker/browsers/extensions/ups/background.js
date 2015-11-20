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
	for(var i=1 ; i< data["openTabs"].length ; i++){
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


//Management of Tor proxy
function toggleTorProxy(){
	chrome.browserAction.getTitle({},function(res){

		if(res == "Tor disabled"){
			//Enabling Tor proxy (use of SOCKS5 proxy)
			var torConfig = {
				mode: "fixed_servers",
				rules: {
					singleProxy: {
						scheme: "socks5",
						host: "localhost",
						port: 9050
					},
					bypassList: ["localhost", "127.0.0.1"]
				}
			};
			chrome.proxy.settings.set(
					{value: torConfig, scope: 'regular'},
					function() {
						//Change icon and title
						chrome.browserAction.setIcon({path:"imgs/tor-enabled-24.png"});
						chrome.browserAction.setTitle({title:"Tor enabled"});
					}
			);
		} else {
			//Disabling Tor proxy
			chrome.proxy.settings.clear(
					{scope: 'regular'},
					function() {
						//Change icon and title
						chrome.browserAction.setIcon({path:"imgs/tor-disabled-24.png"});
						chrome.browserAction.setTitle({title:"Tor disabled"});
					}
			);

		}
	});
}

chrome.browserAction.onClicked.addListener(toggleTorProxy);

