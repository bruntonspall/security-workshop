# Security Workshop

This is a collection of docker based python applications designed to demonstrate two levels of security testing

Note that the code in here is deliberately hacky and bad, it has security vulnerabilities by design.  Don't copy this style of coding

To test out the app, do the following (each in a new shell, the debug.sh continues running in the foreground):

```
cd userapi
./build.sh && ./debug.sh

cd paymentapi
./build.sh && ./debug.sh

cd web
./build.sh && ./debug.sh
```

You can then access the webapp on http://localhost:8080

You will first need to create some test user accounts, by visiting http://localhost:8081/setup

This will create:

|Username|Password|
|--------|--------|
|anna|12345678|
|admin|123456|

You can verify that claims have created a payment by visiting http://localhost:8082/payments