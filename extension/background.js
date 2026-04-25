chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    const threadId = message.threadId;
    const tabId = sender.tab.id;
    analyseEmail(threadId,tabId)
    return true;
});

function getAuthToken() {
    return new Promise(function (resolve, reject) {
        chrome.identity.getAuthToken({ interactive: true }, function (token) {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                resolve(token);
            }
        });
    });
}

async function analyseEmail(threadId, tabId) {
    const token = await getAuthToken();
    const url = `https://gmail.googleapis.com/gmail/v1/users/me/threads/${threadId}`;
    try {
        const response = await fetch(url, {
            headers: { "Authorization": "Bearer " + token }
        });

        if (!response.ok) {
            console.log(await response.json());
            return;
        }

        const data = await response.json();
        const headers = data.messages[0].payload.headers;
        const from = headers.find(h => h.name === "From").value;
        const subject = headers.find(h => h.name === "Subject").value;
        const body = data.messages[0].snippet;

        const analysisResponse = await fetch("http://127.0.0.1:8000/analysis", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: from, subject: subject, body: body })
        });

        const analysis = await analysisResponse.json();
        chrome.tabs.sendMessage(tabId, { analysis: analysis });

    } catch (error) {
        console.error(error);
    }
}