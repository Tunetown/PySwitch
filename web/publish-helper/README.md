# PySwitch Emulator Publisher

This project can publish multiple versions of PySwitch Emulator. It is a standalone project, coming with its own docker configuration, bound to port 8080 on the host machine. Run the container with ./docker-run and you will get a terminal login directly, to test the create/update scripts.

## How to install on a web server
Copy everything in the web/publish-helper/htdocs to your web root.

## Create Versions

Log in to your web server, cd to the versions folder in the web root, and run the create script with the name of the version to be created.

The update script is called at the end of create, but can also be called independently to update the .htaccess file to the current available versions.

## For the End User

Calling the web root will always redirect to the latest version.
Calling /versions will show a page linking to all available versions.
