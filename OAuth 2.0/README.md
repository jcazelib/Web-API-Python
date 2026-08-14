Example OAuth 2.0 implementation with IBKR

Example auth flow:
1. POST https://api.ibkr.com/oauth2/api/v1/token    (scope = sso-sessions.write)                   
2. POST https://api.ibkr.com/gw/api/v1/sso-sessions (credential = the IBKR username | IP = the user's source IP Address)                
3. POST https://api.ibkr.com/v1/api/tickle                                  
4. POST https://api.ibkr.com/v1/api/iserver/auth/ssodh/init   
5. Sleep for 3-5 seconds
6. GET https://api.ibkr.com/v1/api/iserver/accounts
7. Access any other non-/iserver or /iserver endpoints in the Web API as needed
8. POST https://api.ibkr.com/v1/api/tickle                                  
9. POST https://api.ibkr.com/v1/api/logout                                 
