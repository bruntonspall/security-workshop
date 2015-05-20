Steal banking creds

Narrative: 
In order to steal banking credentials
As a hacker
I want to be able to collect other users bank details

Meta: @story steal-bank-creds

Scenario: Bank credentials should be accessible to all
Meta: @id bank-creds-open
Given a new browser instance
When the user logs in from a fresh login page
And the user has made a claim
And a hacker requests from the payments api: /account/admin
Then the users bank details should be returned

