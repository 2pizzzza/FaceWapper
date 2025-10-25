document.getElementById("startSwap").addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "startSwapping" });
});
