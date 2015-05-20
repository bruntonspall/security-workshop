Steal banking creds

Narrative: 
In order to steal banking credentials
As a hacker who has owned the web server
I want to be able to collect other users bank details

Meta: @story steal-bank-creds

Scenario: Bank credentials should be accessible to all
Meta: @id bank-creds-open
Given a new browser instance
When the user logs in from a fresh login page
And the user has made a claim
And a hacker requests from the payments api: /account/admin
Then the users bank details should not be returned

Scenario: Bank credentials should be updatable with just username
Meta: @id bank-creds-open
Given a new browser instance
When the user logs in from a fresh login page
And the user has made a claim
And a hacker posts their bank details to the payments api: /account/admin
Then the payment should not be sent to the criminal
