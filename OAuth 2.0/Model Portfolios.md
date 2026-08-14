Documentation - https://api.ibkr.com/gw/swagger-ui.html#/Trading%20FA%20Allocation%20Management <br>

Phase 1 <br>
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
POST /iserver/account/{modelCode}/orders    (Place Order) <br> <br>

Phase 2 <br>
POST /fa/model/rebalance/to-existing-targets (Rebalance to existing targets, not yet documented on IBKR) <br>
POST /fa/model/rebalance/to-new-targets      (Rebalance to new targets, not yet documented on IBKR) <br>
POST /fa/model/rebalance/to-specific-targets (Rebalance to specific targets, not yet documented on IBKR) <br>
POST /fa/model/tws-invest-divest             (TWS-style invest divest, not yet documented on IBKR) <br>
POST /fa/is-full-master                      (Check if full master or partial master, not yet documented on IBKR) <br>
POST /fa/model/cash-analyzer                 (Cash analyzer, used with multi-currency models not yet documented on IBKR) <br> 

Example /portfolio requests <br>
GET /portfolio/{accountId}/positions/{pageId}?model=MP.{modelCode} <br>
GET /portfolio2/{accountId}/positions?model=MP.{modelCode} <br>
GET /portfolio/{accountId}/summary?model=MP.{modelCode} <br>
GET /portfolio/{accountId}/ledger?model=MP.{modelCode} <br>

Example pnl requests <br>
GET /iserver/account/pnl/partitioned <br>
POST /fa/model/accounts-details <br>
