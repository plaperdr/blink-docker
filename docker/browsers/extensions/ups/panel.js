document.addEventListener('DOMContentLoaded', function() {

    $('#check').change(function() {
        if(this.checked) {
            activateTorProxy();
        } else {
            deactivateTorProxy();
        }
    });

    $('#refreshFingerprint').click(function() {
        chrome.runtime.getBackgroundPage(function(background){
            background.refreshFingerprint();
        });
    });

    $('#viewFingerprint').click(function() {
        chrome.tabs.create({ url: "https://amiunique.org/viewFP" });
    });

    chrome.storage.sync.get({
        proxy: false,
        connected: false,
        errorConnection: false
    }, function(items) {
        if(items.proxy && items.connected){
            $('#check').prop('checked',true);
        } else if(items.proxy){
            $('#check').click();
        } else if(items.errorConnection){
            $('#connDiv').fadeIn(500);
            $('#error').show();
        }
    });

});


//Management of Tor proxy
function activateTorProxy(){
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
        function() {}
    );
    verifyTor();
}

function deactivateTorProxy(){
    //Disabling Tor proxy
    chrome.proxy.settings.clear(
        {scope: 'regular'},
        function() {}
    );
    chrome.storage.sync.set(
        {proxy: false,
        connected: false},
        function() {}
    );

    $('#connected').prop('checked',false);
}

function verifyTor(){
    $('#loader').fadeIn(500);
    $('#connDiv').fadeIn(500);
    $.ajax({
        url: "https://antani.tor2web.org/checktor",
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            if(data.IsTor){
                $('#connected').prop('checked',true);
                $('#connDiv').delay(2000).fadeOut(500);
                chrome.storage.sync.set({
                    connected: true,
                    proxy: true,
                    errorConnection: false
                },function() {
                });

            }
            $('#loader').hide();
            $('#error').hide();

        },
        error : function(){
            $('#loader').hide();
            $('#error').show();
            $('#check').click();
            chrome.storage.sync.set({
                errorConnection: true
            },function() {
            });
        }
    });
}
