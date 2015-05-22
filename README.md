# Security Workshop

This is a collection of docker based python applications designed to demonstrate two levels of security testing

Note that the code in here is deliberately hacky and bad, it has security vulnerabilities by design.  Don't copy this style of coding

# Getting started

## OSX

```
brew install boot2docker
boot2docker init
```

This should install boot2docker, so that you can work with the docker image that this tutorial defines.

## Linux

install vagrant from http://www.vagrantup.com/

```
vagrant up
vagrant ssh
```

# Running the app

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

# Troubleshooting

## boot2docker init failures

```
error in run: Failed to get latest release: Error getting releases: API
rate limit exceeded for an.ip.addr.ess. (But here's the good news:
Authenticated requests get a higher rate limit. Check out the
documentation for more details.)
```

Try using the `-v` option to see what `boot2docker` is doing. It is
typically github.com that is rate-limiting attempts to download the
boot2docker ISO image. See https://github.com/boot2docker/boot2docker/issues/481

You can get around this by:

```
pushd ~/.boot2docker
wget https://github.com/boot2docker/boot2docker/releases/download/v1.6.2/boot2docker.iso
popd
boot2docker init -v
```
