// scripts.js

// 假設這裡是你爬取和更新指標數據的代碼，這裡我們用一個假的示例
const mockIndicatorData = {
    crypto: [
        { name: "BTC/USD", value: "32000" },
        { name: "ETH/USD", value: "2000" },
        { name: "XRP/USD", value: "0.75" }
    ],
    forex: [
        { name: "EUR/USD", value: "1.18" },
        { name: "GBP/USD", value: "1.38" },
        { name: "USD/JPY", value: "110.5" }
    ],
    commodities: [
        { name: "Gold", value: "1800" },
        { name: "Silver", value: "25.50" },
        { name: "Crude Oil", value: "70.25" }
    ],
    'taiwan-stocks': [
        { name: "台積電", value: "600" },
        { name: "鴻海", value: "120" },
        { name: "台塑", value: "100" }
    ],
    'us-stocks': [
        { name: "AAPL", value: "140" },
        { name: "AMZN", value: "3500" },
        { name: "GOOGL", value: "2500" }
    ]
};

// 更新指標數據到頁面
function updateIndicatorData(market) {
    const indicatorContainer = document.getElementById("indicator-data");
    indicatorContainer.innerHTML = ""; // 清空舊數據
    const data = mockIndicatorData[market];
    data.forEach(indicator => {
        const indicatorElement = document.createElement("div");
        indicatorElement.textContent = `${indicator.name}: ${indicator.value}`;
        indicatorContainer.appendChild(indicatorElement);
    });
}

// 初始化加載預設市場的指標數據
document.addEventListener("DOMContentLoaded", function() {
    const marketSelect = document.getElementById("market-select");
    marketSelect.addEventListener("change", function() {
        const selectedMarket = marketSelect.value;
        updateIndicatorData(selectedMarket);
    });

    // 初始化時加載加密貨幣的指標數據
    updateIndicatorData("crypto");
});
