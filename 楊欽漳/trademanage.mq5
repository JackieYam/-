  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
// 部分平倉功能
void ClosePartial(double percentage, string symbol)
  {
   int totalOrders = PositionsTotal();
   for (int i = 0; i < totalOrders; i++)
     {
      ulong ticket = PositionGetTicket(i);
      if (PositionSelectByTicket(ticket))
        {
         if (PositionGetString(POSITION_SYMBOL) == symbol)
           {
            double lotSize = PositionGetDouble(POSITION_VOLUME);
            double closeLots = lotSize * percentage / 100.0;
            // 平倉手數必須在最小手數和當前手數之間
            if (closeLots >= SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN) && closeLots <= lotSize)
              {
              trade.PositionClosePartial(ticket, closeLots);
               // 使用 trade.PositionClosePartial 來平倉指定的手數
               if (!trade.PositionClosePartial(ticket, closeLots))
                 {
                  Print("部分平倉失敗: ", ticket, " - Error: ", GetLastError());
                 }
              }
            else
              {
               Print("平倉手數不在有效範圍內: ", closeLots, " (最小: ", SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN), ", 當前: ", lotSize, ")");
              }
           }
        }
     }
  }

void SetSLTP(ulong ticket)
{
               Print("訂單號: ", ticket, " 沒有設置SL 或 TP.");
               double stopLoss = 0, takeProfit = 0;
               double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
               long minStopLevelPoints = SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);
               if (minStopLevelPoints < 0)
               {
                  minStopLevelPoints = 10;
               }
               double minStopLevel = minStopLevelPoints * _Point;
               if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
               {
                  stopLoss = openPrice - 200 * _Point; 
                  takeProfit = openPrice + 300 * _Point; 
                  if (stopLoss > openPrice - minStopLevel)
                     stopLoss = openPrice - minStopLevel;
                     trade.PositionModify(ticket, stopLoss, takeProfit);

                  if (takeProfit < openPrice + minStopLevel)
                     takeProfit = openPrice + minStopLevel;
                     trade.PositionModify(ticket, stopLoss, takeProfit);
               }
               else if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
               {
                  stopLoss = openPrice + 200 * _Point;
                  takeProfit = openPrice - 300 * _Point;
                  if (stopLoss < openPrice + minStopLevel)
                     stopLoss = openPrice + minStopLevel;
                     trade.PositionModify(ticket, stopLoss, takeProfit);
                  if (takeProfit > openPrice - minStopLevel)
                     takeProfit = openPrice - minStopLevel;
                     trade.PositionModify(ticket, stopLoss, takeProfit);
               }              
               if (!trade.PositionModify(ticket, stopLoss, takeProfit))
               {
                  Print("設置SL和TP失敗: ", ticket, " - Error: ", GetLastError());
               }
            }
int inprofits(ulong ticket) {
    // Select the position by its ticket
    if (PositionSelectByTicket(ticket)) {
        double openPrice = PositionGetDouble(POSITION_PRICE_OPEN);
        double currentPrice = PositionGetDouble(POSITION_PRICE_CURRENT);
        double takeProfit = 0;
        double secured = 0;

        if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) {
            if (currentPrice >= openPrice + 100 * _Point) {
                takeProfit = openPrice + 300 * _Point;
                trade.PositionModify(ticket, 0, takeProfit); // Modify the take profit
                ClosePartial(50, "XAUUSD"); // Close partial position
                secured = 1;
            }
        } else if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL) {
            if (currentPrice <= openPrice - 100 * _Point) {
                takeProfit = openPrice - 300 * _Point;
                trade.PositionModify(ticket, 0, takeProfit); // Modify the take profit
                ClosePartial(50, "XAUUSD"); // Close partial position
                secured = 1;
            }
        }
        return secured;
    } else {
        Print("Position not found for ticket: ", ticket);
        return 0;
    }
}

void Check(){
int totalOrders = PositionsTotal();
double secured=0;
   for (int i = 0; i < totalOrders; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if (PositionSelectByTicket(ticket))
      {
         if (PositionGetString(POSITION_SYMBOL) == _Symbol) // 檢查當前symbol的訂單
         {
            if (PositionGetDouble(POSITION_SL) == 0 || PositionGetDouble(POSITION_TP) == 0)
            {
            SetSLTP(ticket);//沒有止損先設一下
            }
            else if(secured==0){
            secured=inprofits(ticket);
            }
}}
}
Print(secured);
}


void ManageOrders()
  {
  Check();
  }

void OnTick()
  {
   ManageOrders();
  }


