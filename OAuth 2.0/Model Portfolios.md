<b> FA Model Portfolios Documentation <b/> <br>
Swagger - https://api.ibkr.com/gw/swagger-ui.html#/Trading%20FA%20Model%20Portfolios <br>
Long form docs - https://www.interactivebrokers.com/docs/web-api/trading/financial-advisors/model-portfolios <br>
Overview - https://www.interactivebrokers.com/campus/trading-lessons/tws-model-portfolios/ | https://www.ibkrguides.com/traderworkstation/model-portfolios.htm <br>

<b> FA Pre-trade Allocations Documentation <b/> <br>
Swagger - https://api.ibkr.com/gw/swagger-ui.html#/Trading%20FA%20Allocation%20Management <br>
Inline allocations - https://www.interactivebrokers.com/docs/web-api/trading/orders/new-order-example#advisor-order-allocation <br>
Overview - https://www.interactivebrokers.com/en/software/pdfhighlights/PDF-AdvisorAllocations.php | https://www.ibkrguides.com/traderworkstation/pre-trade-allocations.htm <br> <br>

<b> Phase 1 <b/> <br>
GET /iserver/account/allocation/models      (GET IServer models, query this prior to other /fa/model requests below) <br>
POST /fa/fa-preset/get                      (Get Model Presets) <br>
POST /fa/fa-preset/save                     (Set Model Presets) <br>
POST /fa/model/accounts-details             (Get Models Accounts)       
POST /fa/model/invest-divest                (Invest Account Into Model) <br>
POST /fa/model/invest-divest-positions      (Summary Of Accounts Invested In The Model) <br>
POST /fa/model/list                         (Request All Models) <br>
POST /fa/model/positions                    (Get Model Positions) <br>
POST /fa/model/save                         (Set Model Allocations) <br>
POST /fa/model/submit-transfers             (Submit Transfers) <br>
POST /fa/model/summary                      (Request Model Summary) <br>
POST /iserver/account/{modelCode}/orders    (Place Order) <br>

<b> Phase 2 <b/> <br>
POST /fa/model/rebalance/to-existing-targets (Rebalance to existing targets) <br>
POST /fa/model/rebalance/to-new-targets      (Rebalance to new targets) <br>
POST /fa/model/rebalance/to-specific-targets (Rebalance to specific targets) <br>
POST /fa/model/tws-invest-divest             (TWS-style invest divest) <br>
POST /fa/is-full-master                      (Check if full master or partial master) <br>
POST /fa/model/cash-analyzer                 (Cash analyzer, used with multi-currency models) <br> 

<b> Example /portfolio requests <b/> <br>
GET /portfolio/{accountId}/positions/{pageId}?model=MP.{modelCode} <br>
GET /portfolio2/{accountId}/positions?model=MP.{modelCode} <br>
GET /portfolio/{accountId}/summary?model=MP.{modelCode} <br>
GET /portfolio/{accountId}/ledger?model=MP.{modelCode} <br>

<b> Example pnl requests <b/> <br>
GET /iserver/account/pnl/partitioned <br>
POST /fa/model/accounts-details <br>
