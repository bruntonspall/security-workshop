Steal banking creds

Narrative: 
In order to steal banking credentials
As a hacker who has owned the web server
I want to be able to collect other users bank details

Meta: @story steal-bank-creds

Scenario: Bank credentials should be accessible to all
Meta: @id bank-creds-open
Given the system contains a claim
When a hacker requests data from the payments api using a username
Then the users bank details should not be returned


Scenario: Bank credentials should be updatable with just username
Meta: @id bank-creds-open
Given the system contains a claim
When a hacker posts their bank details to the payments api using a username
Then the payment should not be sent to the criminal


Scenario: A fraudster cannot use the same bank account for multiple claims
Meta: @id bank-creds-open
Given the system contains a claim
When a fraudster posts a duplicate bank details claim
Then the second claim should not be paid
