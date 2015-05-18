# Security Workshop

This is a collection of docker based python applications designed to demonstrate two levels of security testing

Note that the code in here is deliberately hacky and bad, it has security vulnerabilities by design.  Don't copy this style of coding

To test out the app, do the following: 

```
./start.sh
```

You can then access the webapp on http://localhost/

This will build and start each of the docker containers for you.

The users created for testing are:

|Username|Password|
|--------|--------|
|anna|letmein|
|admin|password1|

You can verify that claims have created a payment by visiting http://localhost:8082/payments
