chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "startSwapping") {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            chrome.scripting.executeScript({
                target: {tabId: tabs[0].id},
                files: ["content/facewapper.js"],
            });
        });
    }
});
