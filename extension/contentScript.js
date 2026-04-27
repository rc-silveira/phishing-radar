let currentUrl = window.location.href
const targetNode = document.body

function callback() {
    if (currentUrl != window.location.href) {
        currentUrl = window.location.href
        if (window.location.hash.includes('/')) {
            setTimeout(() => {
                const threadId = document.querySelector('h2[data-legacy-thread-id]')?.getAttribute('data-legacy-thread-id')
                chrome.runtime.sendMessage({ threadId: threadId })
            }, 2000)
        }
    }
}

const observer = new MutationObserver(callback)
observer.observe(targetNode, { childList: true, subtree: true })

chrome.runtime.onMessage.addListener(function (message) {
    if (message.analysis) {
        const el = document.createElement("div")
        el.id = "phishing-radar-banner"

        const banner = document.createElement("div")
        banner.style.cssText = `
            position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
            background-color: ${message.analysis.is_a_threat ? '#d93025' : '#1e8e3e'};
            color: white; padding: 12px 20px; font-family: Arial, sans-serif;
            font-size: 14px; display: flex; align-items: center; justify-content: space-between;
        `

        const text = document.createElement("span")
        text.textContent = message.analysis.is_a_threat ? '⚠️ Phishing detected' : '✅ Safe email'

        const detailsDiv = document.createElement("div")
        detailsDiv.style.cssText = `
            display: none; position: fixed; top: 48px; left: 0; right: 0; z-index: 9999;
            background-color: ${message.analysis.is_a_threat ? '#b31412' : '#137333'};
            color: white; padding: 12px 20px; font-family: Arial, sans-serif; font-size: 13px;
        `
        detailsDiv.innerHTML = `
            <p style="margin: 0 0 8px 0"><strong>Explanation:</strong> ${message.analysis.explanation}</p>
            <p style="margin: 0"><strong>Signals:</strong> ${message.analysis.signals}</p>
        `

        const btnDetails = document.createElement("button")
        btnDetails.textContent = "Details"
        btnDetails.style.cssText = `
            background: rgba(255,255,255,0.2); border: none; color: white;
            padding: 6px 12px; margin-right: 8px; border-radius: 4px; cursor: pointer; font-size: 13px;
        `
        btnDetails.addEventListener("click", function () {
            detailsDiv.style.display = detailsDiv.style.display === 'none' ? 'block' : 'none'
        })

        const btnOk = document.createElement("button")
        btnOk.textContent = "OK"
        btnOk.style.cssText = `
            background: rgba(255,255,255,0.2); border: none; color: white;
            padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px;
        `
        btnOk.addEventListener("click", function () {
            el.remove()
        })

        const btns = document.createElement("div")
        btns.appendChild(btnDetails)
        btns.appendChild(btnOk)

        banner.appendChild(text)
        banner.appendChild(btns)
        el.appendChild(banner)
        el.appendChild(detailsDiv)
        document.body.appendChild(el)
    }
    if (message.error) {
        const el = document.createElement("div")
        el.style.cssText = `
        position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
        background-color: #f29900; color: white; padding: 12px 20px;
        font-family: Arial, sans-serif; font-size: 14px;
    `
        el.textContent = "🛠️ Fixing some issues..."
        document.body.appendChild(el)
    }
})