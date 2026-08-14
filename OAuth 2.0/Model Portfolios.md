Documentation - https://api.ibkr.com/gw/swagger-ui.html#/Trading%20FA%20Allocation%20Management 

- Endpoints - 
Phase 1
GET /iserver/account/allocation/models      (GET IServer models, query this prior to other /fa/model requests below)
POST /fa/fa-preset/get                      (Get Model Presets)
POST /fa/fa-preset/save                     (Set Model Presets)
POST /fa/model/accounts-details             (Get Models Accounts)           
POST /fa/model/invest-divest                (Invest Account Into Model)
POST /fa/model/invest-divest-positions      (Summary Of Accounts Invested In The Model)
POST /fa/model/list                         (Request All Models)
POST /fa/model/positions                    (Get Model Positions)
POST /fa/model/save                         (Set Model Allocations)
POST /fa/model/submit-transfers             (Submit Transfers)
POST /fa/model/summary                      (Request Model Summary)
POST /iserver/account/{modelCode}/orders    (Place Order)

Phase 2
POST /fa/model/rebalance/to-existing-targets (Rebalance to existing targets, not yet documented on IBKR)
POST /fa/model/rebalance/to-new-targets      (Rebalance to new targets, not yet documented on IBKR)
POST /fa/model/rebalance/to-specific-targets (Rebalance to specific targets, not yet documented on IBKR)
POST /fa/model/tws-invest-divest             (TWS-style invest divest, not yet documented on IBKR)
POST /fa/is-full-master                      (Check if full master or partial master, not yet documented on IBKR)
POST /fa/model/cash-analyzer                 (Cash analyzer, used with multi-currency models not yet documented on IBKR)

Example /portfolio requests
GET /portfolio/{accountId}/positions/{pageId}?model=MP.{modelCode}
GET /portfolio2/{accountId}/positions?model=MP.{modelCode}
GET /portfolio/{accountId}/summary?model=MP.{modelCode}
GET /portfolio/{accountId}/ledger?model=MP.{modelCode}

Example pnl requests
GET /iserver/account/pnl/partitioned
POST /fa/model/accounts-details
