IBKR Python WebAPI Samples


Author - 
John Cazel / jcazelib  |  https://github.com/jcazelib 

Documentation - 
https://ibkrcampus.com/ibkr-api-page/cpapi-v1/

Purpose -
The content included here demonstrates Python implementations for either Client Portal Gateway authentication or through OAuth 1.0a. This should not be used as an example of a perfect trading system, but a means of implementing our RESTful API with standard Python libraries.

Note about OAuth 1.0a Implementation -
For users looking to use utilize the OAuth 1.0a implementation, please be aware that you must have a funded ORG or Institutional account through Interactive Brokers, with approved access for the OAuth self-service portal, provided by the IBKR API Support team for qualified accounts.

OAuth 1.0a flow: <br>
1. POST https://api.ibkr.com/oauth/live_session_token        (when using your own custom 9-charcater Consumer Key, start with the Live Session Token request) <br>
2. POST https://api.ibkr.com/v1/api/iserver/auth/ssodh/init     <br>
3. time.sleep(X) for 3-5 seconds <br>
4. GET https://api.ibkr.com/v1/api/iserver/accounts <br>
5. Access any other non-/iserver or /iserver endpoints in the Web API as needed <br>
6. POST https://api.ibkr.com/v1/api/tickle                 
7. POST https://api.ibkr.com/v1/api/logout      <br>              
